#!/usr/bin/env python3
"""
趣选AI营销文案引擎 - 多平台内容创作/A/B测试/CTA优化
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

logger = QuxuanLogger.setup("quxuan-copywriter")

SYSTEM_PROMPT = "你是一位顶级营销文案专家，精通各平台内容创作。你的文案既有创意又有转化力。输出Markdown格式。"


def build_xiaohongshu_prompt(product: str, selling_points: str, style: str) -> str:
    return f"""你是一位小红书百万粉丝博主，擅长写出让人忍不住点赞收藏的种草笔记。

请为以下产品写一篇小红书种草笔记：

【产品】{product}
【核心卖点】{selling_points}
【笔记风格】{style or "真实测评"}

【写作要求】
1. 标题：用emoji + 悬念/数字/痛点，≤20字
2. 开头：3秒内抓住注意力（疑问/痛点/惊叹）
3. 正文：分段短句、emoji点缀、口语化、真实感
4. 结构：先说结论 → 优点 → 小缺点（增加真实感）→ 总结推荐
5. 结尾：互动引导（提问/投票）+ 话题标签5-8个
6. 字数：300-500字

请直接输出笔记内容，不需要额外说明。"""


def build_douyin_prompt(product: str, style: str, ab_test: bool) -> str:
    ab_text = "请同时生成2个不同风格的脚本版本（A版：故事型，B版：测评型），方便A/B测试。" if ab_test else ""
    return f"""你是一位抖音千万播放量的短视频编导，擅长写出让人停不下来的短视频脚本。

请为以下产品写一个抖音短视频脚本：

【产品】{product}
【视频风格】{style or "种草推荐"}

{ab_text}

【脚本格式】
## 🎬 短视频脚本

**视频时长：** XX秒
**BGM建议：** ...

### 画面 | 口播/字幕 | 时长
（按时间线逐镜头描述）

### 📌 前3秒Hook
（开头抓人的关键设计）

### #话题标签
（推荐5-8个话题标签）

### 💡 拍摄建议
（场景、道具、表演要点）"""


def build_seo_prompt(keyword: str, word_count: int) -> str:
    return f"""你是一位SEO内容专家，擅长写出既对搜索引擎友好、又让读者愿意读完的高质量文章。

请围绕以下关键词写一篇SEO优化文章：

【目标关键词】{keyword}
【目标字数】{word_count}字

【SEO要求】
1. 标题(H1)：包含核心关键词，有吸引力
2. 副标题(H2/H3)：覆盖长尾关键词
3. 关键词密度：2%-3%，自然融入
4. 段落：短段落，每段不超过4行
5. 包含：列表、表格、FAQ等结构化内容
6. 开头100字内出现核心关键词
7. 结尾有总结和行动号召

【文章结构】
# 标题（含关键词）
## 引言（痛点/场景引入）
## 主体内容（分H2/H3小节）
## 总结
## FAQ（3-5个相关问题）"""


def build_ad_prompt(product: str, platform: str, selling_points: str, ab_test: bool) -> str:
    ab_text = """
请生成A/B两个版本：
- 版本A：痛点切入（从用户困扰引入）
- 版本B：效果展示（从成功案例/数据引入）
每个版本包含：标题、正文(≤100字)、CTA按钮文案
""" if ab_test else "请生成1个版本，包含：标题、正文(≤100字)、CTA按钮文案"

    return f"""你是一位转化率极高的广告文案专家，精通各大信息流平台的广告创作。

请为以下产品写信息流广告文案：

【产品】{product}
【投放平台】{platform or "信息流广告"}
【核心卖点】{selling_points}

{ab_text}

【CTA优化原则】
- 紧迫感（限时/限量）
- 低门槛（免费/0元）
- 具体化（数字优于形容词）

【输出格式】
## 📢 广告文案

### 版本A
**标题：** ...
**正文：** ...
**CTA按钮：** ...

### 版本B（如需要）
...

## 📊 投放建议
- 目标人群画像
- 最佳投放时段
- 落地页建议"""


def build_product_prompt(product: str, selling_points: str, style: str) -> str:
    return f"""你是一位资深品牌文案，擅长用文字打动消费者。

请为以下产品撰写专业的产品描述：

【产品名称】{product}
【核心卖点】{selling_points}
【描述风格】{style or "专业商务"}

【输出内容】
## 🏷️ 产品描述

### 一句话描述
（电梯演讲版本，20字内）

### 产品简介
（100字，突出核心价值）

### 核心卖点（FABE法则）
（Feature-Advantage-Benefit-Evidence 每个卖点展开）

### 适用人群
（精准画像）

### 使用场景
（3-5个具体场景）

### 品牌故事
（200字品牌/产品故事）"""


def build_story_prompt(product: str, brand: str, details: str) -> str:
    return f"""你是一位品牌故事专家，擅长用情感化叙事建立品牌与消费者的连接。

请为以下品牌/产品撰写品牌故事：

【品牌/产品】{product}
【品牌名】{brand}
【背景信息】{details}

【要求】
1. 真实感：有具体的时间、地点、人物
2. 情感共鸣：触动目标受众的内心
3. 价值传递：自然传递品牌价值观
4. 字数：500-800字
5. 风格：温暖、真诚、有力量"""


class FriendlyParser(argparse.ArgumentParser):
    """友好错误提示 - 双语输出"""
    def error(self, message):
        print(f"❌ 参数错误 / Argument Error: {message}\n", file=sys.stderr)
        print(f"💡 使用 --help 查看完整用法 / Use --help for usage", file=sys.stderr)
        sys.exit(2)


def main():
    parser = FriendlyParser(description="趣选AI营销文案引擎")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式: text(默认文本) / json(结构化输出)")
    parser.add_argument("--version", action="version", version=f"趣选文案引擎 AI Copywriting Engine v2.1.0")
    parser.add_argument("--mode", required=True,
                        choices=["xiaohongshu", "douyin", "moments", "ad", "seo", "product", "story"],
                        help="文案模式")
    parser.add_argument("--product", type=str, default="", help="产品/服务名称")
    parser.add_argument("--selling_points", type=str, default="", help="核心卖点（逗号分隔）")
    parser.add_argument("--platform", type=str, default="", help="投放平台")
    parser.add_argument("--keyword", type=str, default="", help="SEO关键词")
    parser.add_argument("--word_count", type=int, default=1500, help="目标字数")
    parser.add_argument("--style", type=str, default="", help="文案风格")
    parser.add_argument("--ab_test", type=str, default="false", help="是否A/B测试（true/false）")
    parser.add_argument("--tone", type=str, default="", help="语气风格")
    parser.add_argument("--brand", type=str, default="", help="品牌名")
    parser.add_argument("--details", type=str, default="", help="补充信息")
    parser.add_argument("--output", type=str, default=None, help="输出文件路径")
    parser.add_argument("--provider", choices=["dashscope", "openai", "deepseek"], default="dashscope")
    args = parser.parse_args()

    # === 必要参数校验 ===
    needs_product = ["xiaohongshu", "douyin", "moments", "ad", "product", "story"]
    needs_selling = ["xiaohongshu", "ad", "product"]
    needs_keyword = ["seo"]
    if args.mode in needs_product and (not args.product or not args.product.strip()):
        print(f"❌ {args.mode} 模式需要提供 --product 参数 / {args.mode} mode requires --product", file=sys.stderr)
        sys.exit(1)
    if args.mode in needs_selling and (not args.selling_points or not args.selling_points.strip()):
        print(f"❌ {args.mode} 模式需要提供 --selling_points 参数 / {args.mode} mode requires --selling_points", file=sys.stderr)
        sys.exit(1)
    if args.mode in needs_keyword and (not args.keyword or not args.keyword.strip()):
        print("❌ SEO模式需要提供 --keyword 参数 / SEO mode requires --keyword", file=sys.stderr)
        sys.exit(1)

    # === 数值校验 ===
    if args.word_count <= 0:
        print("❌ 字数必须大于0 / Word count must be positive", file=sys.stderr)
        sys.exit(1)

    ab = args.ab_test.lower() == "true"

    # === 企业级限流检查 ===
    rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)
    user_key = SecurityHeaders.hash_content(os.getenv("USER", "anonymous"))
    if not rate_limiter.is_allowed(user_key):
        print("⚠️ 请求频率过高，请稍后再试 / Rate limit exceeded, please try again later", file=sys.stderr)
        sys.exit(1)

    # === 企业级输入验证+清洗 ===
    if args.product:
        valid, err = InputSanitizer.validate(args.product, "product")
        if not valid:
            print(f"❌ 输入错误: {err}", file=sys.stderr)
            sys.exit(1)
    if args.selling_points:
        valid, err = InputSanitizer.validate(args.selling_points, "selling_points")
        if not valid:
            print(f"❌ 输入错误: {err}", file=sys.stderr)
            sys.exit(1)
    if args.keyword:
        valid, err = InputSanitizer.validate(args.keyword, "keyword")
        if not valid:
            print(f"❌ 输入错误: {err}", file=sys.stderr)
            sys.exit(1)

    args.product = InputSanitizer.sanitize(args.product)
    args.selling_points = InputSanitizer.sanitize(args.selling_points)
    args.keyword = InputSanitizer.sanitize(args.keyword)
    args.style = InputSanitizer.sanitize(args.style)
    args.brand = InputSanitizer.sanitize(args.brand)
    args.details = InputSanitizer.sanitize(args.details)

    prompt_builders = {
        "xiaohongshu": lambda: build_xiaohongshu_prompt(args.product, args.selling_points, args.style),
        "douyin": lambda: build_douyin_prompt(args.product, args.style, ab),
        "moments": lambda: build_product_prompt(args.product, args.selling_points, args.style or "朋友圈风格"),
        "ad": lambda: build_ad_prompt(args.product, args.platform, args.selling_points, ab),
        "seo": lambda: build_seo_prompt(args.keyword, args.word_count),
        "product": lambda: build_product_prompt(args.product, args.selling_points, args.style),
        "story": lambda: build_story_prompt(args.product, args.brand, args.details),
    }

    mode_names = {
        "xiaohongshu": "小红书种草笔记", "douyin": "抖音短视频脚本",
        "moments": "朋友圈文案", "ad": "广告文案", "seo": "SEO文章",
        "product": "产品描述", "story": "品牌故事"
    }
    logger.info(f"[{mode_names[args.mode]}] 开始创作")
    print(f"✍️ [{mode_names[args.mode]}] 正在创作...", file=sys.stderr)

    prompt = prompt_builders[args.mode]()

    try:
        result = LLMCaller.call(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            provider=args.provider,
            temperature=0.85,
            max_tokens=6000
        )
    except LLMCallError as e:
        logger.error(f"LLM调用失败 [{e.code}]: {e}")
        print(f"❌ LLM调用失败 [{e.code}]: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        try:
            AtomicFileWriter.write(args.output, result)
            print(f"✅ 文案已保存到: {args.output}", file=sys.stderr)
        except PermissionError:
            print(f"❌ 无权限写入文件 / Permission denied: {args.output}", file=sys.stderr)
            sys.exit(1)
        except OSError as e:
            print(f"❌ 写入失败 / Write failed: {str(e)[:100]}", file=sys.stderr)
            sys.exit(1)
    else:
        if getattr(args, "format", "text") == "text":
            print(result)
            print(CrossPromotionEngine.get_recommendation("quxuan-copywriter"))
            print(CrossPromotionEngine.get_closing_banner("quxuan-copywriter"))
        else:
            output_data = {
                "status": "success",
                "skill": "quxuan-copywriter",
                "product": getattr(args, "product", None),
                "content": result,
                "metadata": {"provider": getattr(args, "provider", "dashscope"), "version": "2.1.0"}
            }
            print(json.dumps(output_data, ensure_ascii=False, indent=2))

    print("✅ 文案创作完成！", file=sys.stderr)


if __name__ == "__main__":
    main()
