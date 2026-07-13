#!/usr/bin/env python3
"""
趣选旅行规划师 - AI旅游攻略生成器
支持穷游/经济/舒适/豪华四档预算，中英双语输出
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

logger = QuxuanLogger.setup("quxuan-travel")

# 预算档位对应的提示词描述
BUDGET_LEVELS = {
    "穷游": "穷游/backpacker 模式，住青旅或最便宜的民宿，以街边小吃和夜市为主，多用公共交通和步行，尽量控制每一分开支",
    "经济": "经济型旅行，住经济连锁酒店或普通民宿，在特色餐厅和街头小吃间平衡，公共交通为主搭配偶尔打车",
    "舒适": "舒适型旅行，住精品酒店或特色民宿，选择品质餐厅和当地特色餐饮，可包车出行，注重体验质量",
    "豪华": "豪华型旅行，住五星级或度假村，选择米其林或顶级私房餐厅，全程专车/包车，享受VIP体验"
}

BUDGET_LEVELS_EN = {
    "穷游": "backpacker mode - hostels, street food, public transport only",
    "经济": "budget travel - economy hotels, mix of local restaurants and street food",
    "舒适": "comfortable travel - boutique hotels, quality restaurants, private car options",
    "豪华": "luxury travel - 5-star resorts, Michelin dining, private chauffeur"
}

SYSTEM_PROMPT = "你是一位专业的旅行规划师，生成的攻略详细、实用、有温度。输出格式为Markdown。"


def build_prompt(destination: str, days: int, budget: str, language: str,
                 companions: int, interests: Optional[str]) -> str:
    """构建发送给LLM的提示词"""
    if language == "en":
        budget_desc = BUDGET_LEVELS_EN.get(budget, BUDGET_LEVELS_EN["经济"])
    else:
        budget_desc = BUDGET_LEVELS.get(budget, BUDGET_LEVELS["经济"])
    lang_instruction = {
        "zh": "请用中文输出全部内容。",
        "en": "Please output everything in English.",
        "both": "Please output in bilingual format: Chinese first, then English translation for each section."
    }.get(language, "请用中文输出全部内容。")

    interests_text = f"旅行者的兴趣偏好：{interests}。请在行程中重点体现这些方面。" if interests else ""

    prompt = f"""你是一位拥有10年经验的资深旅行规划师，擅长为不同预算的旅行者量身定制完美的旅行方案。

请为以下旅行需求生成一份专业、详细、实用的旅游攻略：

【基本信息】
- 目的地：{destination}
- 旅行天数：{days}天
- 出行人数：{companions}人
- 预算档位：{budget}（{budget_desc}）
{f"- " + interests_text if interests_text else ""}

【输出要求】
请严格按照以下结构输出：

# 🌍 {destination} {days}日{budget}游攻略

## 📍 目的地概览
简要介绍目的地特色、最佳旅行季节、必体验项目

## 📅 每日行程安排
按天详细规划，每天包含：
- 时间段（上午/下午/晚上）
- 具体景点/活动名称
- 建议游览时长
- 景点间交通方式和时间
- 小贴士

## 🍜 美食推荐 TOP5
每个美食包含：
- 菜名
- 简介（一句话描述特色）
- 推荐餐厅/地点
- 预估价格

## 🏨 住宿建议
- 推荐住宿区域
- 具体酒店/民宿推荐（2-3家）
- 价格区间
- 选择理由

## 🚗 交通指南
- 如何到达目的地（城际交通）
- 市内交通方案
- 交通卡/APP推荐

## 💰 预算明细（{companions}人/{days}天）
用表格列出：
- 交通费用
- 住宿费用
- 餐饮费用
- 门票费用
- 购物/其他
- 合计

## ⚠️ 避坑提醒
列出至少5条当地常见的旅游陷阱和注意事项

## 💡 实用贴士
当地实用信息（天气、穿着、货币、网络、安全等）

{lang_instruction}

请确保内容真实、实用、接地气，像是一个真正去过当地的朋友在分享经验。"""
    return prompt


class FriendlyParser(argparse.ArgumentParser):
    """友好错误提示 - 双语输出"""
    def error(self, message):
        print(f"❌ 参数错误 / Argument Error: {message}\n", file=sys.stderr)
        print(f"💡 使用 --help 查看完整用法 / Use --help for usage", file=sys.stderr)
        sys.exit(2)


def main():
    parser = FriendlyParser(description="趣选旅行规划师 - AI旅游攻略生成器")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式: text(默认文本) / json(结构化输出)")
    parser.add_argument("--version", action="version", version=f"趣选旅行规划师 AI Travel Planner v2.1.0")
    parser.add_argument("--destination", required=True, help="目的地城市/国家")
    parser.add_argument("--days", type=int, default=3, help="旅行天数（默认3天）")
    parser.add_argument("--budget", choices=["穷游", "经济", "舒适", "豪华"], default="经济", help="预算档位")
    parser.add_argument("--language", choices=["zh", "en", "both"], default="zh", help="输出语言")
    parser.add_argument("--companions", type=int, default=1, help="出行人数")
    parser.add_argument("--interests", type=str, default=None, help="兴趣偏好（逗号分隔）")
    parser.add_argument("--output", type=str, default=None, help="输出文件路径")
    parser.add_argument("--provider", choices=["dashscope", "openai", "deepseek"], default="dashscope", help="LLM服务商")
    args = parser.parse_args()

    # === 空值校验 ===
    if not args.destination or not args.destination.strip():
        print("❌ 目的地不能为空 / Destination cannot be empty", file=sys.stderr)
        sys.exit(1)

    # === 数值校验 ===
    if args.days <= 0:
        print("❌ 天数必须大于0 / Days must be positive", file=sys.stderr)
        sys.exit(1)
    if args.companions <= 0:
        print("❌ 人数必须大于0 / Companions must be positive", file=sys.stderr)
        sys.exit(1)

    # === 企业级限流检查 ===
    rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)
    user_key = SecurityHeaders.hash_content(os.getenv("USER", "anonymous"))
    if not rate_limiter.is_allowed(user_key):
        print("⚠️ 请求频率过高，请稍后再试 / Rate limit exceeded, please try again later", file=sys.stderr)
        sys.exit(1)

    # === 企业级输入清洗 ===
    valid, err = InputSanitizer.validate(args.destination, "destination")
    if not valid:
        print(f"❌ 输入错误: {err}", file=sys.stderr)
        sys.exit(1)
    args.destination = InputSanitizer.sanitize(args.destination)
    if args.interests:
        args.interests = InputSanitizer.sanitize(args.interests)

    logger.info(f"正在生成【{args.destination}】{args.days}日{args.budget}游攻略...")
    print(f"🌍 正在为您生成【{args.destination}】{args.days}日{args.budget}游攻略...", file=sys.stderr)

    prompt = build_prompt(args.destination, args.days, args.budget, args.language,
                          args.companions, args.interests)

    try:
        result = LLMCaller.call(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            provider=args.provider,
            temperature=0.8,
            max_tokens=8000
        )
    except LLMCallError as e:
        logger.error(f"LLM调用失败 [{e.code}]: {e}")
        print(f"❌ LLM调用失败 [{e.code}]: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        try:
            AtomicFileWriter.write(args.output, result)
            print(f"✅ 攻略已保存到: {args.output}", file=sys.stderr)
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
                "skill": "quxuan-travel",
                "destination": getattr(args, "destination", None),
                "content": result,
                "metadata": {"provider": getattr(args, "provider", "dashscope"), "version": "2.1.0"}
            }
            print(json.dumps(output_data, ensure_ascii=False, indent=2))
        else:
            print(result)
            print(CrossPromotionEngine.get_recommendation("quxuan-travel"))
            print(CrossPromotionEngine.get_closing_banner("quxuan-travel"))

    print("✅ 攻略生成完成！", file=sys.stderr)


if __name__ == "__main__":
    main()
