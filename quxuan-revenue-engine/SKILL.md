---
name: quxuan-revenue-engine
description: "Enterprise-grade AI revenue optimization engine 企业级AI收益优化引擎 - dynamic pricing, user behavior analysis, conversion funnel optimization, A/B testing, retention scoring, and LTV prediction. 动态定价、用户行为分析、转化漏斗、A/B测试、留存评分与LTV预测。"
version: "2.1.0"
---

# Quxuan Revenue Engine 趣选收益引擎 🚀

## Overview 概述

Enterprise-grade AI revenue optimization engine that provides dynamic pricing strategies, user behavior analysis, conversion funnel optimization, A/B testing frameworks, retention scoring, and LTV prediction.

企业级AI收益优化引擎，提供动态定价策略、用户行为分析、转化漏斗优化、A/B测试框架、留存评分和LTV预测。

## Features 功能模块

### 1. Dynamic Pricing Engine 动态定价引擎 💰
- Time-based pricing coefficients (hourly/weekend/holiday)
- Demand-based price adjustment algorithms
- Off-peak discount strategies / Peak-time premium pricing
- Price elasticity modeling and optimization
- 基于时段的定价系数（小时/周末/节假日）
- 需求驱动的价格调整算法
- 闲时折扣策略 / 热门时段溢价定价
- 价格弹性建模与优化

### 2. Conversion Funnel Analyzer 转化漏斗分析 📊
- Multi-stage funnel tracking and analysis
- Drop-off point identification and optimization suggestions
- Revenue-per-session optimization
- First-order conversion rate boosters
- 多阶段漏斗追踪与分析
- 流失节点识别与优化建议
- 单次会话收益优化
- 首单转化率提升策略

### 3. A/B Testing Framework A/B测试框架 🧪
- Experiment design and sample size calculation
- Statistical significance validation
- Multi-metric comparison (revenue, retention, satisfaction)
- Automated winner selection and rollout
- 实验设计与样本量计算
- 统计显著性验证
- 多指标对比（收入、留存、满意度）
- 自动胜出方选择与上线

### 4. Retention Scoring & LTV Prediction 留存评分与LTV预测 📈
- User lifecycle stage classification
- Churn risk scoring with early warning
- Lifetime value prediction model
- Personalized retention strategy recommendations
- 用户生命周期阶段分类
- 流失风险评分与预警
- 终身价值预测模型
- 个性化留存策略推荐

### 5. Revenue Dashboard Generator 收益仪表盘 📋
- Daily/weekly/monthly revenue reports
- Key metrics: ARPU, LTV, CAC, churn rate
- Trend analysis and forecasting
- Actionable insights and recommendations
- 日/周/月收益报告
- 关键指标：ARPU、LTV、CAC、流失率
- 趋势分析与预测
- 可执行的洞察与建议

## Usage 使用方式

```bash
# Dynamic pricing analysis 动态定价分析
python scripts/main.py --mode pricing --data revenue_data.json --output pricing_strategy.json

# Conversion funnel analysis 转化漏斗分析
python scripts/main.py --mode funnel --data user_journey.json --output funnel_report.json

# A/B test design A/B测试设计
python scripts/main.py --mode ab_test --metric revenue --baseline 100 --effect_size 0.15

# Retention scoring 留存评分
python scripts/main.py --mode retention --data users.json --output retention_scores.json

# Revenue dashboard 收益仪表盘
python scripts/main.py --mode dashboard --period monthly --format markdown
```

## Parameters 参数说明

| Parameter 参数 | Required 必填 | Description 说明 | Default 默认值 |
|------|------|------|--------|
| `--mode` | Yes 是 | pricing/funnel/ab_test/retention/dashboard | - |
| `--data` | Yes 是 | Input data file path (JSON/CSV) | - |
| `--output` | No 否 | Output file path | stdout |
| `--period` | No 否 | daily/weekly/monthly | monthly |
| `--format` | No 否 | markdown/json/csv | markdown |
| `--provider` | No 否 | dashscope/openai/deepseek | dashscope |

## Output Format 输出格式

Markdown / JSON format, including:
- Executive summary 执行摘要
- Key metrics breakdown 关键指标拆解
- Trend analysis 趋势分析
- Actionable recommendations 可执行建议
- Risk warnings 风险预警

## Requirements 依赖要求

- Python 3.8+
- LLM API access (DashScope / OpenAI / DeepSeek)
- User behavioral data in JSON/CSV format

## Disclaimer 免责声明

This tool provides AI-generated insights and recommendations based on data patterns. All business decisions should be validated with real-world testing. Past performance does not guarantee future results.

本工具提供基于数据模式的AI分析洞察和建议。所有商业决策应通过实际测试验证。过往表现不保证未来结果。
