#!/usr/bin/env python3
"""
趣选职场效率工具箱 - 简历优化/商务邮件/Excel公式/合同模板 4合1
Version: 2.1.0 (Enterprise)
"""

import argparse
import json
import os
import sys

from enterprise import (
    InputSanitizer, RateLimiter, SecurityHeaders, CrossPromotionEngine,
    LLMCaller, LLMCallError, QuxuanLogger, AtomicFileWriter, ErrorCode
)

logger = QuxuanLogger.setup("quxuan-workplace")

SYSTEM_PROMPT = "你是职场效率专家，精通简历优化、商务写作、Excel和合同法。输出Markdown格式。"


def build_resume_prompt(input_text: str, target: str = "") -> str:
    target_text = f"目标岗位：{target}" if target else ""
    return f"""你是一位拥有15年经验的资深HR顾问和简历优化专家，熟悉ATS（Applicant Tracking System）系统筛选机制。

请对以下工作经历进行专业优化：

【原始内容】
{input_text}

{target_text}

【优化要求】
1. 使用STAR法则（Situation-Task-Action-Result）重构每段经历
2. 量化所有成果（用数字、百分比、金额）
3. 使用强力动词开头（主导、推动、实现、优化、提升...）
4. 确保ATS友好：使用标准标题、关键词匹配
5. 输出格式：

## 📄 优化后简历内容

### 个人简介
（2-3行精炼总结）

### 工作经历
（STAR法则重构，每条含量化成果）

### 核心技能
（关键词列表，ATS友好）

## 📊 优化对比
| 优化前 | 优化后 | 改进点 |
|--------|--------|--------|

## 💡 优化建议
（3-5条针对性的改进建议）"""


def build_email_prompt(scenario: str, details: str, language: str, tone: str) -> str:
    lang_map = {"zh": "中文", "en": "English", "both": "中英双语（先中文后英文）"}
    return f"""你是一位商务沟通专家，擅长撰写各类商务邮件。

请根据以下需求撰写一封专业的商务邮件：

【邮件场景】{scenario}
【具体信息】{details}
【语言】{lang_map.get(language, "中文")}
【语气】{tone}

【输出格式】
## ✉️ 邮件

**主题行：** ...

**正文：**
（完整邮件内容）

---

## 💡 写作说明
- 关键策略解释
- 发送时机建议
- 跟进建议"""


def build_excel_prompt(query: str) -> str:
    return f"""你是一位Excel专家，擅长将自然语言需求转化为精确的Excel公式。

【用户需求】
{query}

【输出格式】
## 🔢 Excel公式方案

### 方案一（推荐）
**公式：** `=...`
**解释：** 逐步解释公式每部分的含义
**适用版本：** Excel 2019+ / Office 365

### 方案二（备选）
**公式：** `=...`
**解释：** ...
**适用场景：** 旧版Excel兼容

### 📋 示例数据与结果
（用表格展示示例输入和预期输出）

### 💡 注意事项
- 常见错误及解决方法
- 性能优化建议（大数据量时）"""


def build_contract_prompt(contract_type: str, party_a: str, party_b: str, details: str) -> str:
    return f"""你是一位有20年执业经验的商业律师，擅长起草各类商务合同。

请生成以下合同的标准模板：

【合同类型】{contract_type}
【甲方】{party_a}
【乙方】{party_b}
【补充信息】{details if details else "无特殊要求"}

【输出格式】
## 📋 {contract_type}

（完整合同模板，包含标准条款）

---

## ⚠️ 关键条款提醒
（列出需要特别注意的条款和潜在风险点）

## 📝 填写指南
（需要双方协商填写的关键字段说明）

---
**免责声明：** 本模板仅供参考，不构成法律建议。正式使用前请咨询专业律师。"""


class FriendlyParser(argparse.ArgumentParser):
    """友好错误提示 - 双语输出"""
    def error(self, message):
        print(f"❌ 参数错误 / Argument Error: {message}\n", file=sys.stderr)
        print(f"💡 使用 --help 查看完整用法 / Use --help for usage", file=sys.stderr)
        sys.exit(2)


def main():
    parser = FriendlyParser(description="趣选职场效率工具箱")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式: text(默认文本) / json(结构化输出)")
    parser.add_argument("--version", action="version", version=f"趣选职场效率 AI Workplace Tools v2.1.0")
    parser.add_argument("--mode", required=True, choices=["resume", "email", "excel", "contract"],
                        help="功能模式")
    # 简历相关
    parser.add_argument("--input", type=str, help="简历原始内容")
    parser.add_argument("--target", type=str, default="", help="目标岗位")
    # 邮件相关
    parser.add_argument("--scenario", type=str, help="邮件场景")
    parser.add_argument("--details", type=str, default="", help="具体信息")
    parser.add_argument("--language", choices=["zh", "en", "both"], default="zh", help="输出语言")
    parser.add_argument("--tone", type=str, default="professional", help="语气（professional/friendly/urgent）")
    # Excel
    parser.add_argument("--query", type=str, help="Excel需求描述")
    # 合同
    parser.add_argument("--type", type=str, help="合同类型")
    parser.add_argument("--party-a", type=str, default="甲方", help="甲方名称")
    parser.add_argument("--party-b", type=str, default="乙方", help="乙方名称")
    # 通用
    parser.add_argument("--output", type=str, default=None, help="输出文件路径")
    parser.add_argument("--provider", choices=["dashscope", "openai", "deepseek"], default="dashscope")
    args = parser.parse_args()

    # === 企业级限流检查 ===
    rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)
    user_key = SecurityHeaders.hash_content(os.getenv("USER", "anonymous"))
    if not rate_limiter.is_allowed(user_key):
        print("⚠️ 请求频率过高，请稍后再试 / Rate limit exceeded, please try again later", file=sys.stderr)
        sys.exit(1)

    # === 模式必要参数校验 ===
    if args.mode == "resume" and (not args.input or not args.input.strip()):
        print("❌ 简历优化模式需要提供 --input 参数 / Resume mode requires --input", file=sys.stderr)
        sys.exit(1)
    if args.mode == "email" and (not args.scenario or not args.scenario.strip()):
        print("❌ 邮件生成模式需要提供 --scenario 参数 / Email mode requires --scenario", file=sys.stderr)
        sys.exit(1)
    if args.mode == "excel" and (not args.query or not args.query.strip()):
        print("❌ Excel公式模式需要提供 --query 参数 / Excel mode requires --query", file=sys.stderr)
        sys.exit(1)
    if args.mode == "contract" and (not args.type or not args.type.strip()):
        print("❌ 合同模式需要提供 --type 参数 / Contract mode requires --type", file=sys.stderr)
        sys.exit(1)

    # === 企业级输入清洗 ===
    if args.input:
        args.input = InputSanitizer.sanitize(args.input)
    if args.scenario:
        args.scenario = InputSanitizer.sanitize(args.scenario)
    if args.query:
        args.query = InputSanitizer.sanitize(args.query)
    if args.target:
        args.target = InputSanitizer.sanitize(args.target)
    if args.type:
        args.type = InputSanitizer.sanitize(args.type)
    if args.party_a:
        args.party_a = InputSanitizer.sanitize(args.party_a)
    if args.party_b:
        args.party_b = InputSanitizer.sanitize(args.party_b)
    if args.details:
        args.details = InputSanitizer.sanitize(args.details)

    prompts = {
        "resume": lambda: build_resume_prompt(args.input or "", args.target),
        "email": lambda: build_email_prompt(args.scenario or "", args.details, args.language, args.tone),
        "excel": lambda: build_excel_prompt(args.query or ""),
        "contract": lambda: build_contract_prompt(args.type or "合作协议", args.party_a, args.party_b, args.details)
    }

    mode_names = {"resume": "简历优化", "email": "邮件生成", "excel": "Excel公式", "contract": "合同模板"}
    logger.info(f"[{mode_names[args.mode]}] 开始处理")
    print(f"💼 [{mode_names[args.mode]}] 正在处理...", file=sys.stderr)

    prompt = prompts[args.mode]()

    try:
        result = LLMCaller.call(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            provider=args.provider,
            temperature=0.6,
            max_tokens=6000
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
        if getattr(args, "format", "text") == "text":
            print(result)
            print(CrossPromotionEngine.get_recommendation("quxuan-workplace"))
            print(CrossPromotionEngine.get_closing_banner("quxuan-workplace"))
        else:
            output_data = {
                "status": "success",
                "skill": "quxuan-workplace",
                "mode": getattr(args, "mode", None),
                "content": result,
                "metadata": {"provider": getattr(args, "provider", "dashscope"), "version": "2.1.0"}
            }
            print(json.dumps(output_data, ensure_ascii=False, indent=2))

    print("✅ 处理完成！", file=sys.stderr)


if __name__ == "__main__":
    main()
