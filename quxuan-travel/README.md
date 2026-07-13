# 🌍 AI Travel Planner | 趣选旅行规划师

> **免费开源** · 输入目的地，秒出专业旅游攻略

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)]()
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue.svg)](https://openclaw.dev)

---

## ✨ 为什么选择 AI Travel Planner？

❌ 传统方式：翻遍小红书、马蜂窝、TripAdvisor，花 3 小时拼凑攻略  
✅ 使用 AI Travel Planner：**10 秒生成**专业级旅行方案，涵盖行程、美食、住宿、交通、预算、避坑全维度

---

## 🚀 快速开始

### 安装

```bash
openclaw install quxuan-travel
```

### 基础使用

```bash
# 生成京都5日经济游攻略
python scripts/main.py --destination "京都" --days 5 --budget "经济"

# 巴黎7日舒适游（英文）
python scripts/main.py --destination "Paris" --days 7 --budget "comfort" --language en

# 带兴趣偏好
python scripts/main.py --destination "成都" --days 4 --interests "美食,历史,熊猫"
```

### 输出到文件

```bash
python scripts/main.py --destination "东京" --days 5 --output tokyo_guide.md
```

---

## 📊 效果展示

### 输入
```
目的地：大理  天数：4天  预算：舒适  2人出行  偏好：摄影、民族文化
```

### 输出（节选）
```markdown
# 🏔️ 大理 4 日舒适游攻略

## Day 1 - 古城漫步·洱海初印象
- 09:00 抵达大理，入住洱海畔精品民宿
- 10:30 大理古城自由漫步（推荐：人民路→洋人街→五华楼）
- 12:00 午餐：段公子·白族主题餐厅
- 14:00 租电动车环洱海（龙龛码头→才村→喜洲）
- 18:00 洱海边摄影 golden hour
- 20:00 古城夜市

## 🍜 美食 TOP5
1. 喜洲粑粑 - 白族传统面食，外酥内软
2. 酸辣鱼 - 洱海鱼现杀现做
3. 乳扇 - 白族特色奶制品
4. 凉鸡米线 - 大理街头经典
5. 生皮 - 勇敢者的美食挑战

## 💰 预算明细（2人/4天）
| 项目 | 预估费用 |
|------|---------|
| 住宿 | ¥1,200 |
| 餐饮 | ¥800 |
| 交通 | ¥400 |
| 门票 | ¥350 |
| 其他 | ¥250 |
| **合计** | **¥3,000** |

## ⚠️ 避坑提醒
- 古城银器店多为义乌货，谨慎购买
- 环洱海电动车续航注意，建议租品牌车
- 雨季（6-9月）备雨具，防晒不分季节
```

---

## 🎛️ 四档预算对比

| 档位 | 住宿标准 | 餐饮标准 | 日均预算（单人） |
|------|---------|---------|----------------|
| 穷游 | 青旅/民宿 | 街边小吃 | ¥150-300 |
| 经济 | 经济酒店 | 特色餐厅 | ¥300-600 |
| 舒适 | 精品酒店 | 品质餐厅 | ¥600-1200 |
| 豪华 | 五星/度假村 | 米其林/私房菜 | ¥1200+ |

---

## 🔧 技术细节

- 支持 DashScope / OpenAI / DeepSeek 三种 LLM 后端
- 环境变量配置 API Key
- 纯 Python 实现，零额外依赖（除 httpx）
- 中英双语输出，支持对照模式

## 📝 License

MIT License
## 🛡️ Enterprise Features
- Input sanitization & injection protection 输入清洗防注入
- Rate limiting & DDoS protection 限流保护
- Auto-retry with exponential backoff 自动重试
- Connection pooling for high performance 连接池高性能
- Cross-skill recommendations 交叉推荐引流