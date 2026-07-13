# 🍳 AI Recipe & Life Assistant | 趣选生活助手

> **免费开源** · 想吃什么问一句，秒出专业菜谱

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)]()

---

## ✨ 核心能力

| 功能 | 说明 |
|------|------|
| 🍲 菜谱生成 | 精确到克的食材用量，分步烹饪指导 |
| 📊 营养分析 | 热量、蛋白质、脂肪、碳水一目了然 |
| ⚠️ 过敏原提示 | 自动标注常见过敏原 |
| 🔄 替换建议 | 买不到/不能吃？提供替代方案 |
| ⏱️ 时间预估 | 准备时间 + 烹饪时间精确标注 |
| 🏷️ 难度等级 | 入门🟢 / 进阶🟡 / 高手🔴 |

---

## 🚀 快速开始

### 安装
```bash
openclaw install quxuan-daily
```

### 使用示例

```bash
# 经典红烧肉，4人份
python scripts/main.py --dish "红烧肉" --servings 4

# 素食友好，排除过敏原
python scripts/main.py --dish "咖喱鸡" --diet "素食" --allergies "花生,海鲜"

# 新手友好
python scripts/main.py --dish "糖醋排骨" --difficulty "入门"

# 生活助手模式
python scripts/main.py --lifestyle-query "如何去除衣服上的油渍"
```

---

## 📊 效果展示

### 输入
```
--dish "番茄牛腩" --servings 3 --difficulty "入门"
```

### 输出（节选）
```markdown
# 🍅 番茄牛腩

> 酸甜开胃的经典家常菜，汤汁浓郁，牛肉软烂，老少皆宜

| 难度 | 🟢 入门 | 准备时间 | 20分钟 | 烹饪时间 | 90分钟 |
|------|---------|---------|---------|---------|--------|

## 🛒 食材清单（3人份）
| 食材 | 用量 | 备注 |
|------|------|------|
| 牛腩 | 500g | 选肥瘦相间的 |
| 番茄 | 4个（约600g） | 熟透的多汁番茄 |
| 洋葱 | 半个 | 增香 |
| 姜片 | 5片 | |
| 料酒 | 2汤匙 | |
| 番茄酱 | 3汤匙 | 增色增味 |
| 盐 | 适量 | 最后调味 |
| 糖 | 1茶匙 | 提鲜 |

## 👨‍🍳 烹饪步骤
1. **牛腩焯水**：冷水下锅，加姜片、料酒，大火煮开撇去浮沫，捞出切3cm方块
2. **番茄处理**：顶部划十字，开水烫30秒去皮，切块备用
3. **炒香底料**：锅中少许油，小火炒洋葱至透明，加入一半番茄炒出汁
4. **炖煮**：加入牛腩翻炒均匀，加番茄酱、热水没过食材，大火煮开转小火炖80分钟
5. **收汁**：加入剩余番茄，加盐、糖调味，中火收汁至浓稠

## ⚠️ 过敏原提示
- 本品不含常见过敏原 ✅

## 🔄 替换建议
- 牛腩 → 牛腱子（更瘦，需延长炖煮时间）
- 番茄酱 → 新鲜番茄多加2个
- 洋葱 → 可用大葱白替代

## 📊 营养成分（每份估算）
| 项目 | 含量 |
|------|------|
| 热量 | ~380 kcal |
| 蛋白质 | 32g |
| 脂肪 | 18g |
| 碳水化合物 | 22g |
```

---

## 📝 License

MIT License
## 🛡️ Enterprise Features
- Input sanitization & injection protection 输入清洗防注入
- Rate limiting & DDoS protection 限流保护
- Auto-retry with exponential backoff 自动重试
- Connection pooling for high performance 连接池高性能
- Cross-skill recommendations 交叉推荐引流