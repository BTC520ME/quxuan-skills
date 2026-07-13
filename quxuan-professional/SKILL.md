---
name: quxuan-professional
description: "Legal & tax advisor assistant 专业法律顾问与财税助手 - Legal info organizer (law references + rights protection guide), tax filing procedures, contract risk review, labor arbitration guide. All outputs include disclaimers. 提供法律信息整理(法条引用+维权指引)、报税流程指引、合同风险审核、劳动仲裁指南，所有输出带免责声明。"
version: "2.1.0"
---

# 趣选专业法律顾问 ⚖️ | Quxuan Professional Legal & Tax Advisor

## 概述 Overview

专业级法律信息整理与财税指引技能，为用户提供结构化的法律知识参考、报税流程指引、合同风险审核和劳动仲裁指南。

Professional-grade legal information and tax guidance skill. Provides structured legal references, tax filing guidance, contract risk review, and labor arbitration guides.

## 功能模块 Features

### 1. 法律信息整理 Legal Information 📚
- 法条精准引用 / Precise legal article references
- 司法解释关联 / Judicial interpretation linkage
- 维权途径指引 / Rights protection guidance
- 证据清单生成 / Evidence checklist generation
- 诉讼流程说明 / Litigation process explanation

### 2. 报税指引 Tax Filing Guide 💰
- 个人所得税计算与申报流程 / Personal income tax calculation and filing
- 企业税务指引 / Corporate tax guidance
- 税收优惠政策梳理 / Tax incentive policy review
- 专项附加扣除指导 / Special additional deduction guidance

### 3. 合同审核 Contract Review 🔍
- 风险条款检测 / Risk clause detection
- 不公平条款标注 / Unfair clause highlighting
- 缺失条款提醒 / Missing clause alerts
- 修改建议 / Modification suggestions

### 4. 劳动仲裁指南 Labor Arbitration Guide ⚖️
- 仲裁条件判断 / Arbitration eligibility assessment
- 赔偿金额计算 / Compensation calculation
- 仲裁流程指引 / Arbitration process guidance
- 申请书模板 / Application template

## ⚠️ 免责声明 Disclaimer

**本工具提供的所有内容仅供参考，不构成法律或税务建议。具体情况请咨询专业律师或税务师。**

**All content provided by this tool is for reference only and does not constitute legal or tax advice. Please consult a qualified lawyer or tax advisor for specific situations.**

## 使用方式 Usage

```bash
# 法律信息查询 Legal query
python scripts/main.py --mode legal --query "公司拖欠工资3个月怎么办"

# 报税指引 Tax filing guide
python scripts/main.py --mode tax --query "自由职业者如何缴纳个人所得税"

# 合同审核 Contract review
python scripts/main.py --mode contract_review --file contract.txt

# 劳动仲裁 Labor arbitration
python scripts/main.py --mode labor --query "被公司无故辞退，工作了3年，月薪15000"
```

## 参数说明 Parameters

| 参数 Parameter | 必填 Required | 说明 Description |
|------|------|------|
| `--mode` | 是 Yes | legal/tax/contract_review/labor |
| `--query` | 条件 Condition | 查询内容 Query content |
| `--file` | 条件 Condition | 合同文件路径 Contract file path |
| `--output` | 否 No | 输出文件路径 Output file path |
| `--provider` | 否 No | dashscope/openai/deepseek |

## 依赖要求 Requirements

- Python 3.8+
- LLM API access (DashScope / OpenAI / DeepSeek)
