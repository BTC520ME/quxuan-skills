#!/usr/bin/env python3
"""
趣选专业法律顾问 - 法律信息整理/报税指引/合同审核/劳动仲裁指南
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

logger = QuxuanLogger.setup("quxuan-professional")

SYSTEM_PROMPT = "你是一位专业的法律/税务信息顾问。你提供的信息仅供学习参考，不是法律建议。输出Markdown格式，所有分析必须引用具体法条。每条输出末尾必须附带免责声明。"

DISCLAIMER = """
---
> ⚠️ **免责声明：** 以上内容仅供参考和学习目的，不构成法律或税务建议。每个案件/情况都有其特殊性，建议在做出重要决定前咨询持有执业资格的专业律师或税务师。"""


def build_legal_prompt(query: str) -> str:
    return f"""你是一位精通中国法律的法律信息整理专家（注意：你提供的是法律信息参考，不是法律建议）。

请对以下法律问题进行分析：

【用户问题】{query}

【输出格式】
## 📚 法律分析

### 🔖 相关法律条款
（引用具体法条，包含法律名称、条号、原文要点）

### 📖 司法解释/指导案例
（如有相关司法解释或典型案例，请引用）

### 🛤️ 维权途径
（按推荐优先级列出可行的维权方式，每条含操作步骤）

### 📋 证据清单
（列出维权所需的证据材料，用checkbox格式）

### ⏰ 时效提醒
（相关诉讼时效、申请期限等）

### 💡 实用建议
（3-5条操作层面的具体建议）
{DISCLAIMER}"""


def build_tax_prompt(query: str) -> str:
    return f"""你是一位专业的税务顾问，擅长个人所得税和企业税务规划（注意：你提供的是税务信息参考，不是税务建议）。

请对以下税务问题进行解答：

【用户问题】{query}

【输出格式】
## 💰 税务指引

### 📋 适用税种与税率
（列出可能涉及的税种、税率表）

### 📝 申报流程
（按步骤说明申报流程）

### 🎯 可享受的优惠政策
（列出适用的税收优惠政策）

### 🧮 计算示例
（用具体数字演示计算过程）

### ⏰ 重要时间节点
（申报期限、汇算清缴时间等）

### 💡 节税建议
（合法合规的税务优化建议）
{DISCLAIMER}"""


def build_contract_review_prompt(query: str, file_content: str = "") -> str:
    content = file_content if file_content else query
    return f"""你是一位有20年执业经验的合同法律师，擅长合同审核和风险提示（注意：你提供的是参考意见，不是法律建议）。

请审核以下合同/合同条款：

【合同内容】
{content}

【审核要点】
1. 🔴 高风险条款：可能导致重大损失的条款
2. 🟡 中风险条款：存在模糊或不利表述的条款
3. 🟢 建议优化：可以改进的表述
4. ❌ 缺失条款：应当包含但未出现的条款

【输出格式】
## 🔍 合同审核报告

### 总体风险评估：🟢低/🟡中/🔴高风险

### 🔴 高风险条款
| 条款位置 | 原文摘录 | 风险说明 | 修改建议 |
|---------|---------|---------|---------|

### 🟡 中风险条款
| 条款位置 | 原文摘录 | 风险说明 | 修改建议 |
|---------|---------|---------|---------|

### ❌ 缺失条款
- 列出应当补充的条款及建议内容

### ✅ 修改建议汇总
（完整的修改建议文本）
{DISCLAIMER}"""


def build_labor_prompt(query: str) -> str:
    return f"""你是一位精通劳动法的法律顾问，擅长处理劳动争议和劳动仲裁案件（注意：你提供的是法律信息参考，不是法律建议）。

请对以下劳动争议情况进行分析：

【情况描述】{query}

【输出格式】
## ⚖️ 劳动仲裁分析

### 📋 情况评估
- 争议类型判定
- 是否构成违法（引用具体法条）
- 劳动者权益分析

### 💰 赔偿金额计算
| 项目 | 金额 | 计算依据 | 法律依据 |
|------|------|---------|---------|
| ... | ... | ... | ... |
| **合计** | **¥XXX** | | |

### 🛤️ 维权路径
1. 协商（建议话术）
2. 劳动监察投诉（流程）
3. 劳动仲裁（流程+时间线）
4. 法院诉讼（如仲裁不服）

### 📋 所需证据清单
- [ ] ...

### 📝 仲裁申请书要点
（关键陈述要点）

### ⏰ 时效提醒
（仲裁时效、关键期限）
{DISCLAIMER}"""


class FriendlyParser(argparse.ArgumentParser):
    """友好错误提示 - 双语输出"""
    def error(self, message):
        print(f"❌ 参数错误 / Argument Error: {message}\n", file=sys.stderr)
        print(f"💡 使用 --help 查看完整用法 / Use --help for usage", file=sys.stderr)
        sys.exit(2)


def main():
    parser = FriendlyParser(description="趣选专业法律顾问")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式: text(默认文本) / json(结构化输出)")
    parser.add_argument("--version", action="version", version=f"趣选专业顾问 AI Professional Advisor v2.1.0")
    parser.add_argument("--mode", required=True,
                        choices=["legal", "tax", "contract_review", "labor"],
                        help="功能模式")
    parser.add_argument("--query", type=str, default="", help="问题描述")
    parser.add_argument("--file", type=str, default=None, help="合同文件路径")
    parser.add_argument("--output", type=str, default=None, help="输出文件路径")
    parser.add_argument("--provider", choices=["dashscope", "openai", "deepseek"], default="dashscope")
    args = parser.parse_args()

    # === 必要参数校验 ===
    if not args.query or not args.query.strip():
        print(f"❌ {args.mode} 模式需要提供 --query 参数 / {args.mode} mode requires --query", file=sys.stderr)
        sys.exit(1)

    # === 企业级限流检查 ===
    rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)
    user_key = SecurityHeaders.hash_content(os.getenv("USER", "anonymous"))
    if not rate_limiter.is_allowed(user_key):
        print("⚠️ 请求频率过高，请稍后再试 / Rate limit exceeded, please try again later", file=sys.stderr)
        sys.exit(1)

    # === 企业级输入清洗 ===
    if args.query:
        args.query = InputSanitizer.sanitize(args.query)

    mode_names = {"legal": "法律信息", "tax": "报税指引", "contract_review": "合同审核", "labor": "劳动仲裁"}
    logger.info(f"[{mode_names[args.mode]}] 开始分析")
    print(f"⚖️ [{mode_names[args.mode]}] 正在分析...", file=sys.stderr)

    # 构建提示词
    prompt = None
    if args.mode == "legal":
        prompt = build_legal_prompt(args.query)
    elif args.mode == "tax":
        prompt = build_tax_prompt(args.query)
    elif args.mode == "contract_review":
        file_content = ""
        if args.file:
            if not os.path.exists(args.file):
                print(f"❌ 文件不存在: {args.file} / File not found: {args.file}", file=sys.stderr)
                sys.exit(1)
            if os.path.getsize(args.file) > 1024 * 1024:  # 1MB limit
                print(f"❌ 文件过大(>1MB)，请压缩后重试 / File too large (>1MB)", file=sys.stderr)
                sys.exit(1)
            try:
                with open(args.file, "r", encoding="utf-8") as f:
                    file_content = InputSanitizer.sanitize(f.read())
            except UnicodeDecodeError:
                print(f"❌ 文件编码错误，请使用UTF-8格式 / File encoding error, please use UTF-8", file=sys.stderr)
                sys.exit(1)
            except PermissionError:
                print(f"❌ 无权限读取文件 / Permission denied: {args.file}", file=sys.stderr)
                sys.exit(1)
        prompt = build_contract_review_prompt(args.query, file_content)
    elif args.mode == "labor":
        prompt = build_labor_prompt(args.query)

    try:
        result = LLMCaller.call(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            provider=args.provider,
            temperature=0.4,
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
            print(CrossPromotionEngine.get_recommendation("quxuan-professional"))
            print(CrossPromotionEngine.get_closing_banner("quxuan-professional"))
        else:
            output_data = {
                "status": "success",
                "skill": "quxuan-professional",
                "mode": getattr(args, "mode", None),
                "content": result,
                "metadata": {"provider": getattr(args, "provider", "dashscope"), "version": "2.1.0"}
            }
            print(json.dumps(output_data, ensure_ascii=False, indent=2))

    print("✅ 处理完成！", file=sys.stderr)


if __name__ == "__main__":
    main()
