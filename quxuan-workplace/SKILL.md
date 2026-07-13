---
name: quxuan-workplace
description: "Workplace productivity suite 职场效率工具箱 - All-in-one toolkit: resume optimization (STAR method), bilingual business email generator, natural language to Excel formula converter, and contract template builder. 集成简历优化(STAR法则)、商务邮件生成(中英双语)、Excel公式转换、合同模板生成四大职场核心功能。"
version: "2.1.0"
---

# 趣选职场效率工具箱 💼 | Quxuan Workplace Productivity Suite

## 概述 Overview

4合1 职场效率工具，覆盖简历、邮件、Excel、合同四大核心场景，让职场工作更高效。

4-in-1 workplace productivity toolkit covering resumes, emails, Excel formulas, and contracts — making work more efficient.

## 功能模块 Features

### 1. 简历优化 Resume Optimization 📄
- STAR法则重构项目经历 / STAR method for project experience
- 量化工作成果 / Quantify work achievements
- ATS系统友好格式 / ATS-friendly format
- 优化前后对比展示 / Before & after comparison

### 2. 商务邮件 Business Email ✉️
- 多场景模板（客户跟进、合作邀约、催款、致谢、拒绝等）/ Multi-scenario templates (follow-up, partnership, payment reminder, thanks, rejection, etc.)
- 中英双语支持 / Bilingual Chinese-English support
- 语气调节（正式/友好/紧急）/ Tone adjustment (formal/friendly/urgent)

### 3. Excel公式 Excel Formula 🔢
- 自然语言描述 → Excel公式 / Natural language → Excel formula
- 公式解释与示例 / Formula explanation and examples
- 支持复杂嵌套公式 / Support complex nested formulas

### 4. 合同模板 Contract Templates 📋
- 标准合同模板生成 / Standard contract template generation
- 常见合同类型（劳动合同、保密协议、合作协议等）/ Common types (labor contract, NDA, cooperation agreement, etc.)
- 关键条款提醒 / Key clause reminders

## 使用方式 Usage

```bash
# 简历优化 Resume optimization
python scripts/main.py --mode resume --input "我的工作经历..." --target "高级产品经理 Senior PM"

# 邮件生成 Email generation
python scripts/main.py --mode email --scenario "合作邀约" --language en

# Excel公式 Excel formula
python scripts/main.py --mode excel --query "根据A列日期找出B列对应的最大值"

# 合同模板 Contract template
python scripts/main.py --mode contract --type "保密协议" --party_a "公司A" --party_b "公司B"
```

## 参数说明 Parameters

| 参数 Parameter | 必填 Required | 说明 Description |
|------|------|------|
| `--mode` | 是 Yes | resume/email/excel/contract |
| `--input` | 条件 Condition | 输入内容（简历模式）Input content (resume mode) |
| `--target` | 否 No | 目标职位 Target position |
| `--scenario` | 条件 Condition | 邮件场景（邮件模式）Email scenario |
| `--language` | 否 No | 邮件语言 Email language (zh/en) |
| `--query` | 条件 Condition | Excel问题（Excel模式）Excel query |
| `--type` | 条件 Condition | 合同类型（合同模式）Contract type |
| `--output` | 否 No | 输出文件路径 Output file path |
| `--provider` | 否 No | dashscope/openai/deepseek |

## 依赖要求 Requirements

- Python 3.8+
- LLM API access (DashScope / OpenAI / DeepSeek)
