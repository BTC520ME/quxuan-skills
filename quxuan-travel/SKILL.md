---
name: quxuan-travel
description: "Smart travel guide generator 智能旅游攻略生成器 - Input destination and days to generate professional travel plans with daily itineraries, food recommendations, accommodation, transportation guides, and budget breakdowns. 输入目的地和天数，生成包含每日行程、美食推荐、住宿建议、交通指南、预算明细的专业旅行规划方案。"
version: "2.1.0"
---

# 趣选旅行规划师 🌍 | Quxuan Travel Planner

## 概述 Overview

智能旅游攻略生成技能，基于大语言模型为用户提供专业级旅行规划方案。支持穷游/经济/舒适/豪华四档预算，中英双语输出。

Smart travel guide generator powered by LLM. Supports 4 budget levels (budget/economy/comfort/luxury) and bilingual output (Chinese/English).

## 功能 Features

- **每日行程规划 Daily Itinerary**：按天拆分，含景点、时间、交通 / Day-by-day plan with attractions, timing, and transportation
- **美食 TOP5 Top 5 Local Foods**：当地必吃美食推荐 / Must-try local food recommendations
- **住宿建议 Accommodation**：按预算档位推荐区域和类型 / Area and type recommendations by budget level
- **交通指南 Transportation**：城际+市内交通方案 / Intercity + local transit guide
- **预算明细 Budget Breakdown**：分类费用估算表格 / Categorized cost estimation table
- **避坑提醒 Travel Tips**：常见旅游陷阱与注意事项 / Common tourist traps and precautions
- **双语支持 Bilingual**：中文/英文/中英对照 / Chinese / English / Bilingual

## 使用方式 Usage

```bash
# 中文
python scripts/main.py --destination "京都" --days 5 --budget "经济" --language zh

# English
python scripts/main.py --destination "Kyoto" --days 5 --budget "economy" --language en

# 中英对照 Bilingual
python scripts/main.py --destination "Paris" --days 7 --budget "comfort" --language both
```

## 参数说明 Parameters

| 参数 Parameter | 必填 Required | 说明 Description | 默认值 Default |
|------|------|------|--------|
| `--destination` | 是 Yes | 目的地 Destination | - |
| `--days` | 否 No | 旅行天数 Travel days | 3 |
| `--budget` | 否 No | 穷游/经济/舒适/豪华 Budget/Economy/Comfort/Luxury | 经济 Economy |
| `--language` | 否 No | zh/en/both | zh |
| `--companions` | 否 No | 出行人数 Number of travelers | 1 |
| `--interests` | 否 No | 兴趣偏好 Interests (comma-separated) | - |
| `--output` | 否 No | 输出文件路径 Output file path | stdout |
| `--provider` | 否 No | dashscope/openai/deepseek | dashscope |

## 输出格式 Output Format

Markdown 格式，包含以下章节：
Markdown format with the following sections:

1. 目的地概览 Destination Overview
2. 每日行程安排 Daily Itinerary
3. 美食推荐 TOP5 Top 5 Local Foods
4. 住宿建议 Accommodation Guide
5. 交通指南 Transportation Guide
6. 预算明细表 Budget Breakdown
7. 避坑提醒 Travel Tips
8. 实用贴士 Practical Tips

## 依赖要求 Requirements

- Python 3.8+
- LLM API access (DashScope / OpenAI / DeepSeek)
