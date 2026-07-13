#!/usr/bin/env python3
"""
趣选生活助手 - AI菜谱生成与生活助手
支持饮食偏好、过敏原标注、营养分析、难度分级
Version: 2.1.0 (Enterprise)
"""

import argparse
import json
import os
import sys
from typing import Optional

from enterprise import (
    InputSanitizer, RateLimiter, SecurityHeaders, CrossPromotionEngine,
    LLMCaller, LLMCallError, QuxuanLogger, AtomicFileWriter, ErrorCode
)

logger = QuxuanLogger.setup("quxuan-daily")

SYSTEM_PROMPT = "你是专业营养师兼大厨（菜谱模式）或生活专家（生活助手模式）。输出格式为Markdown，内容实用、详细、有条理。"


def build_recipe_prompt(dish: str, servings: int, diet: Optional[str],
                        allergies: Optional[str], difficulty: Optional[str]) -> str:
    """构建菜谱生成的提示词"""
    diet_text = f"- 饮食偏好：{diet}" if diet else ""
    allergy_text = f"- 过敏原（需避免）：{allergies}" if allergies else ""
    diff_text = f"- 目标难度：{difficulty}" if difficulty and difficulty != "不限" else ""

    prompt = f"""你是一位专业营养师兼拥有20年经验的大厨，精通中西餐烹饪，同时对营养学有深入研究。

请为以下菜品生成一份详细的菜谱：

【需求信息】
- 菜品：{dish}
- 用餐人数：{servings}人份
{diet_text}
{allergy_text}
{diff_text}

【输出格式要求】
请严格按以下Markdown格式输出：

# 🍽️ {dish}

> 一句话简介（描述这道菜的特色和口感）

| 难度 | 🟢入门/🟡进阶/🔴高手 | 准备时间 | XX分钟 | 烹饪时间 | XX分钟 |

## 🛒 食材清单（{servings}人份）
| 食材 | 用量 | 备注/选购建议 |
|------|------|-------------|
| ... | ... | ... |

## 👨‍🍳 烹饪步骤
（用编号列表，每步包含：动作+时长+火候+状态判断标准）

## 💡 烹饪技巧
（3-5条让菜品更出彩的专业技巧）

## 📊 营养成分（每份估算）
| 项目 | 含量 |
|------|------|
| 热量 | XXX kcal |
| 蛋白质 | XXg |
| 脂肪 | XXg |
| 碳水化合物 | XXg |
| 膳食纤维 | XXg |
| 钠 | XXmg |

## ⚠️ 过敏原提示
（列出菜品中含有的常见过敏原：坚果、海鲜、乳制品、麸质、大豆、蛋类等。若无则标注"不含常见过敏原 ✅"）

## 🔄 替换建议
（提供2-3个食材替换方案，适用于：买不到、过敏、口味偏好等情况）

请确保用量精确、步骤清晰、新手也能看懂。"""
    return prompt


def build_lifestyle_prompt(query: str) -> str:
    """构建生活助手问题的提示词"""
    return f"""你是一位博学的日常生活专家，精通家居清洁、收纳整理、衣物护理、健康养生等生活技能。

请回答以下生活问题，给出实用、具体、可操作的建议：

问题：{query}

请用Markdown格式回答，结构清晰，重点内容加粗标注。如果涉及步骤，请用编号列表。"""


class FriendlyParser(argparse.ArgumentParser):
    """友好错误提示 - 双语输出"""
    def error(self, message):
        print(f"❌ 参数错误 / Argument Error: {message}\n", file=sys.stderr)
        print(f"💡 使用 --help 查看完整用法 / Use --help for usage", file=sys.stderr)
        sys.exit(2)


def main():
    parser = FriendlyParser(description="趣选生活助手 - AI菜谱生成与生活助手")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式: text(默认文本) / json(结构化输出)")
    parser.add_argument("--version", action="version", version=f"趣选生活助手 AI Daily Assistant v2.1.0")
    parser.add_argument("--dish", type=str, help="菜名或饮食需求描述")
    parser.add_argument("--servings", type=int, default=2, help="用餐人数（默认2）")
    parser.add_argument("--diet", type=str, default=None, help="饮食偏好（素食/无辣/低盐等）")
    parser.add_argument("--allergies", type=str, default=None, help="过敏原（逗号分隔）")
    parser.add_argument("--difficulty", type=str, default=None, help="难度偏好（入门/进阶/不限）")
    parser.add_argument("--lifestyle-query", type=str, default=None, help="生活助手问题")
    parser.add_argument("--output", type=str, default=None, help="输出文件路径")
    parser.add_argument("--provider", choices=["dashscope", "openai", "deepseek"], default="dashscope")
    args = parser.parse_args()

    # === 数值校验 ===
    if args.servings <= 0:
        print("❌ 份数必须大于0 / Servings must be positive", file=sys.stderr)
        sys.exit(1)

    if not args.dish and not args.lifestyle_query:
        parser.error("请提供 --dish 或 --lifestyle-query 参数")

    # 空字符串检查
    if args.dish and not args.dish.strip():
        print("❌ 菜名不能为空 / Dish name cannot be empty", file=sys.stderr)
        sys.exit(1)
    if args.lifestyle_query and not args.lifestyle_query.strip():
        print("❌ 问题不能为空 / Query cannot be empty", file=sys.stderr)
        sys.exit(1)

    # === 企业级限流检查 ===
    rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)
    user_key = SecurityHeaders.hash_content(os.getenv("USER", "anonymous"))
    if not rate_limiter.is_allowed(user_key):
        print("⚠️ 请求频率过高，请稍后再试 / Rate limit exceeded, please try again later", file=sys.stderr)
        sys.exit(1)

    # === 企业级输入清洗 ===
    if args.dish:
        valid, err = InputSanitizer.validate(args.dish, "dish")
        if not valid:
            print(f"❌ 输入错误: {err}", file=sys.stderr)
            sys.exit(1)
        args.dish = InputSanitizer.sanitize(args.dish)
    if args.lifestyle_query:
        valid, err = InputSanitizer.validate(args.lifestyle_query, "lifestyle-query")
        if not valid:
            print(f"❌ 输入错误: {err}", file=sys.stderr)
            sys.exit(1)
        args.lifestyle_query = InputSanitizer.sanitize(args.lifestyle_query)
    if args.diet:
        args.diet = InputSanitizer.sanitize(args.diet)
    if args.allergies:
        args.allergies = InputSanitizer.sanitize(args.allergies)

    if args.dish:
        logger.info(f"正在生成【{args.dish}】的详细菜谱...")
        print(f"🍳 正在生成【{args.dish}】的详细菜谱...", file=sys.stderr)
        prompt = build_recipe_prompt(args.dish, args.servings, args.diet,
                                     args.allergies, args.difficulty)
    else:
        logger.info("正在生成生活助手回答...")
        print(f"💡 正在为您解答生活问题...", file=sys.stderr)
        prompt = build_lifestyle_prompt(args.lifestyle_query)

    try:
        result = LLMCaller.call(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            provider=args.provider,
            temperature=0.7,
            max_tokens=4000
        )
    except LLMCallError as e:
        logger.error(f"LLM调用失败 [{e.code}]: {e}")
        print(f"❌ LLM调用失败 [{e.code}]: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        try:
            AtomicFileWriter.write(args.output, result)
            print(f"✅ 结果已保存到: {args.output}", file=sys.stderr)
        except PermissionError:
            print(f"❌ 无权限写入文件 / Permission denied: {args.output}", file=sys.stderr)
            sys.exit(1)
        except OSError as e:
            print(f"❌ 写入失败 / Write failed: {str(e)[:100]}", file=sys.stderr)
            sys.exit(1)
    else:
        if getattr(args, "format", "text") == "json":
            output_data = {
                "status": "success",
                "skill": "quxuan-daily",
                "dish": getattr(args, "dish", None),
                "content": result,
                "metadata": {"provider": getattr(args, "provider", "dashscope"), "version": "2.1.0"}
            }
            print(json.dumps(output_data, ensure_ascii=False, indent=2))
        else:
            print(result)
            print(CrossPromotionEngine.get_recommendation("quxuan-daily"))
            print(CrossPromotionEngine.get_closing_banner("quxuan-daily"))

    print("✅ 生成完成！", file=sys.stderr)


if __name__ == "__main__":
    main()
