# ✍️ AI Marketing Copy Engine | 趣选AI营销文案引擎

> **多平台内容工厂** · 一个产品，N种爆款文案

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)]()
[![Price](https://img.shields.io/badge/price-$9.99-blue.svg)](pricing)

---

## 🎯 覆盖平台 & 场景

| 平台 | 内容类型 | 特色能力 |
|------|---------|---------|
| 📕 小红书 | 种草笔记/测评/合集 | emoji密度、分段节奏、标签策略 |
| 🎵 抖音 | 短视频脚本/口播文案 | 前3秒hook、节奏感、话题标签 |
| 💬 朋友圈 | 营销/品牌/日常 | 人格化、场景化、克制感 |
| 📰 信息流 | 头条/腾讯广告 | 标题党技巧、转化导向 |
| 🔍 SEO | 长文章/博客 | 关键词密度、H标签结构 |
| 🏷️ 产品描述 | 电商详情页/品牌故事 | 卖点提炼、FABE法则 |

---

## 🚀 安装与使用

```bash
openclaw install quxuan-copywriter
```

### 小红书种草笔记
```bash
python scripts/main.py --mode xiaohongshu \
  --product "XX防晒霜" \
  --selling_points "SPF50+ PA++++,不油腻不假白,添加养肤精华,百元价位" \
  --style "真实测评"
```

**输出示例（节选）：**
```
🌞 姐妹们！今年夏天终于找到本命防晒了！！！

先说结论：无限回购 💯

用了一个多月来交作业📝
先说说我的肤质：混油皮，T区出油王者

✅ 优点：
1. 质地像乳液一样轻薄，上脸完全不油腻
2. 不假白！这点太重要了（之前用XX防晒白的像艺伎）
3. SPF50+日常通勤绰绰有余
4. 添加了养肤精华，卸妆后皮肤状态反而更好

❌ 小缺点：
防水力一般，海边暴晒场景建议补涂

性价比绝了姐妹们冲！

#防晒霜推荐 #夏日防晒 #平价防晒 #油皮防晒 #护肤好物
```

### 抖音短视频脚本
```bash
python scripts/main.py --mode douyin \
  --product "降噪耳机" \
  --style "测评" \
  --ab_test true
```

### SEO文章
```bash
python scripts/main.py --mode seo \
  --keyword "2024年最佳项目管理工具推荐" \
  --word_count 2500
```

### 广告文案 + A/B测试
```bash
python scripts/main.py --mode ad \
  --product "在线英语课程" \
  --platform "信息流" \
  --selling_points "外教1v1,25分钟/节课,随时约课" \
  --ab_test true
```

**A/B测试输出：**
```markdown
## 🧪 A/B测试方案

### 版本A（痛点切入）
**标题：** 学了10年英语还是哑巴？这个方法让你30天开口说
**正文：** ...
**CTA：** 免费领取1对1体验课 →

### 版本B（效果展示）
**标题：** 从不敢开口到全英文面试，她只用了60天
**正文：** ...
**CTA：** 看看她是怎么做到的 →

### 📊 测试建议
- 建议投放周期：7天
- 核心观测指标：点击率、转化率
- 样本量：每组≥1000次曝光
```

---

## 💡 CTA优化原则

内置CTA优化策略：
- **紧迫感**：限时/限量/倒计时
- **低门槛**：免费/试用/0元体验
- **社交证明**：XX人已领取/加入
- **好奇心**：点击查看/解锁/揭秘
- **具体化**：数字 > 形容词

---

## 💰 定价

**一次性购买 $9.99**，终身使用，免费更新。

## 📝 License

MIT License
## 🛡️ Enterprise Features
- Input sanitization & injection protection 输入清洗防注入
- Rate limiting & DDoS protection 限流保护
- Auto-retry with exponential backoff 自动重试
- Connection pooling for high performance 连接池高性能
- Cross-skill recommendations 交叉推荐引流