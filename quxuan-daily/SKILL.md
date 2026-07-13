---
name: quxuan-daily
description: "AI recipe & life assistant AI菜谱与生活助手 - Smart recipe generator (ingredients, steps, nutrition analysis) and daily life tips, perfect for home cooking and daily life queries. 智能生成详细菜谱（含食材用量、步骤、营养分析）和生活技巧建议，适合家庭烹饪和日常生活咨询。"
version: "2.1.0"
---

# 趣选生活助手 🍳 | Quxuan Daily Life Assistant

## 概述 Overview

智能菜谱生成与生活助手技能。基于营养学和烹饪专业知识，为用户生成详细的菜谱方案和生活建议。

Smart recipe and life assistant skill. Generates detailed recipes and life tips based on nutrition science and culinary expertise.

## 功能 Features

- **菜谱生成 Recipe Generation**：菜名简介、食材清单（含精确用量）、详细步骤、烹饪技巧 / Dish intro, ingredient list (with precise amounts), step-by-step instructions, cooking tips
- **营养分析 Nutrition Analysis**：每道菜的营养成分估算 / Nutrition estimation for each dish
- **替换建议 Substitutions**：食材替代方案（过敏/素食/口味调整） / Ingredient alternatives (allergies/vegetarian/taste adjustments)
- **难度标注 Difficulty Level**：入门/进阶/高手三级 / Beginner / Intermediate / Advanced
- **时间预估 Time Estimate**：准备时间 + 烹饪时间 / Prep time + Cook time
- **过敏原提示 Allergen Warning**：自动标注常见过敏原 / Auto-detect common allergens
- **生活助手 Life Assistant**：日常生活中的各类实用建议 / Practical tips for daily life

## 使用方式 Usage

```bash
# 基础菜谱 Basic recipe
python scripts/main.py --dish "红烧肉" --servings 4

# 素食+过敏原 Vegetarian + allergens
python scripts/main.py --dish "西红柿炒鸡蛋" --diet "素食 vegetarian" --allergies "花生 peanuts"

# 新手友好 Beginner friendly
python scripts/main.py --dish "糖醋排骨" --difficulty "入门 beginner"

# 生活助手模式 Life assistant mode
python scripts/main.py --lifestyle-query "如何去除衣服上的油渍 How to remove oil stains from clothes"
```

## 参数说明 Parameters

| 参数 Parameter | 必填 Required | 说明 Description | 默认值 Default |
|------|------|------|--------|
| `--dish` | 是 Yes | 菜名或饮食需求 Dish name or dietary requirement | - |
| `--servings` | 否 No | 用餐人数 Number of servings | 2 |
| `--diet` | 否 No | 饮食偏好 Dietary preference (vegetarian/no-spicy/low-salt) | - |
| `--allergies` | 否 No | 过敏原 Allergens (comma-separated) | - |
| `--difficulty` | 否 No | 难度偏好 Difficulty (beginner/intermediate/any) | 不限 Any |
| `--lifestyle-query` | 否 No | 生活助手问题 Life query (mutually exclusive with --dish) | - |
| `--output` | 否 No | 输出文件路径 Output file path | stdout |
| `--provider` | 否 No | dashscope/openai/deepseek | dashscope |

## 依赖要求 Requirements

- Python 3.8+
- LLM API access (DashScope / OpenAI / DeepSeek)
