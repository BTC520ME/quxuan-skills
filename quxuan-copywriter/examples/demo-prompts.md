# AI Marketing Copy Engine 使用示例

## 📕 小红书

### 种草笔记
```bash
python scripts/main.py --mode xiaohongshu \
  --product "花西子蜜粉" \
  --selling_points "定妆持久12小时,轻薄不厚重,适合油皮" \
  --style "真实测评"
```

### 合集笔记
```bash
python scripts/main.py --mode xiaohongshu \
  --product "秋冬护肤合集" \
  --selling_points "保湿面霜,精华液,面膜" \
  --style "好物合集"
```

---

## 🎵 抖音

### 产品测评
```bash
python scripts/main.py --mode douyin \
  --product "空气炸锅" \
  --style "测评" \
  --ab_test true
```

### 种草视频
```bash
python scripts/main.py --mode douyin \
  --product "瑜伽裤" \
  --style "穿搭分享"
```

---

## 💬 朋友圈

```bash
python scripts/main.py --mode moments \
  --product "手冲咖啡豆" \
  --selling_points "埃塞俄比亚耶加雪菲,新鲜烘焙,果香浓郁" \
  --style "生活分享"
```

---

## 📰 信息流广告

### 带A/B测试
```bash
python scripts/main.py --mode ad \
  --product "在线编程课" \
  --platform "今日头条" \
  --selling_points "零基础入门,3个月就业,年薪15万+" \
  --ab_test true
```

---

## 🔍 SEO文章

```bash
python scripts/main.py --mode seo \
  --keyword "家用净水器哪个牌子好2024" \
  --word_count 3000 \
  --output seo_article.md
```

---

## 🏷️ 产品描述

```bash
python scripts/main.py --mode product \
  --product "智能手表Pro" \
  --selling_points "心率血氧监测,14天续航,100+运动模式,NFC支付" \
  --style "科技感"
```

---

## 📖 品牌故事

```bash
python scripts/main.py --mode story \
  --product "精品咖啡品牌" \
  --brand "晨雾咖啡" \
  --details "创始人在云南普洱发现优质咖啡庄园，决心把中国好咖啡带给更多人"
```
