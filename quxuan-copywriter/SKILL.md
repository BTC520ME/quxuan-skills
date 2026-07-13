---
name: quxuan-copywriter
description: "AI marketing copy engine AI营销文案引擎 - Multi-platform content creation (Xiaohongshu/Douyin/WeChat Moments/feed ads), product descriptions, SEO articles, ad copy with A/B testing and CTA optimization. 支持多平台内容创作（小红书/抖音/朋友圈/信息流）、产品描述、SEO文章、广告文案生成，含A/B测试方案和CTA优化。"
version: "2.1.0"
---

# 趣选AI营销文案引擎 ✍️ | Quxuan AI Marketing Copy Engine

## 概述 Overview

专业级AI营销文案生成技能，覆盖社媒内容、产品描述、SEO文章、广告文案等全场景，支持多平台适配和A/B测试方案。

Professional AI marketing copy generation skill covering social media content, product descriptions, SEO articles, ad copy, and more. Supports multi-platform adaptation and A/B testing.

## 功能模块 Features

### 1. 社媒内容 Social Media Content 📱
- **小红书 Xiaohongshu**：种草笔记、测评、合集 / Seeding notes, reviews, collections
- **抖音 Douyin**：短视频脚本、文案、话题标签 / Short video scripts, copy, hashtags
- **朋友圈 WeChat Moments**：营销文案、品牌故事 / Marketing copy, brand stories
- **信息流 Feed Ads**：今日头条/腾讯广告文案 / Toutiao/Tencent Ads copy

### 2. 产品描述 Product Description 🏷️
- 卖点提炼、用户痛点匹配 / Selling point extraction, pain point matching
- 电商详情页文案 / E-commerce detail page copy
- 品牌故事 / Brand stories

### 3. SEO文章 SEO Articles 🔍
- 关键词布局优化 / Keyword layout optimization
- 长尾词覆盖 / Long-tail keyword coverage
- 搜索引擎友好结构 / SEO-friendly structure

### 4. 广告文案 Ad Copy 📢
- 信息流广告 / Feed ads
- 搜索广告 / Search ads
- 品牌广告 / Brand ads
- CTA（行动号召）优化 / CTA optimization

### 5. A/B测试 A/B Testing 🧪
- 自动生成多版本文案 / Auto-generate multiple versions
- 变量标注（标题/正文/CTA）/ Variable annotation (headline/body/CTA)
- 测试建议 / Testing recommendations

## 使用方式 Usage

```bash
# 小红书种草笔记 Xiaohongshu seeding note
python scripts/main.py --mode xiaohongshu --product "防晒霜" --selling_points "SPF50+,不油腻,养肤"

# 抖音短视频脚本 Douyin short video script
python scripts/main.py --mode douyin --product "蓝牙耳机" --style "测评 review"

# SEO文章 SEO article
python scripts/main.py --mode seo --keyword "2024年最佳项目管理工具" --word_count 2000

# 广告文案 + A/B测试 Ad copy + A/B test
python scripts/main.py --mode ad --product "在线英语课" --platform "信息流" --ab_test true
```

## 参数说明 Parameters

| 参数 Parameter | 必填 Required | 说明 Description |
|------|------|------|
| `--mode` | 是 Yes | xiaohongshu/douyin/moments/ad/seo/product/story |
| `--product` | 否 No | 产品/服务名称 Product/service name |
| `--selling_points` | 否 No | 核心卖点（逗号分隔）Key selling points (comma-separated) |
| `--platform` | 否 No | 投放平台 Target platform |
| `--keyword` | 否 No | SEO关键词 SEO keyword |
| `--word_count` | 否 No | 目标字数 Target word count |
| `--style` | 否 No | 文案风格 Copy style |
| `--ab_test` | 否 No | 是否生成A/B测试版本 Generate A/B test version |
| `--tone` | 否 No | 语气风格 Tone style |
| `--output` | 否 No | 输出文件路径 Output file path |
| `--provider` | 否 No | dashscope/openai/deepseek |

## 依赖要求 Requirements

- Python 3.8+
- LLM API access (DashScope / OpenAI / DeepSeek)
