# AI Travel Planner 使用示例

## 基础示例

### 示例 1：国内经典游
```bash
python scripts/main.py --destination "成都" --days 4 --budget "舒适" --companions 2
```

### 示例 2：出境自由行
```bash
python scripts/main.py --destination "东京" --days 7 --budget "经济" --interests "动漫,美食,购物"
```

### 示例 3：英文输出
```bash
python scripts/main.py --destination "Bali" --days 5 --budget "luxury" --language en
```

### 示例 4：中英对照
```bash
python scripts/main.py --destination "Paris" --days 6 --budget "豪华" --language both
```

### 示例 5：穷游模式
```bash
python scripts/main.py --destination "云南大理" --days 5 --budget "穷游" --interests "摄影,徒步,民族文化" --output dali_guide.md
```

---

## 进阶场景

### 多人家庭游
```bash
python scripts/main.py --destination "三亚" --days 5 --budget "舒适" --companions 4 --interests "亲子,海滩,海鲜"
```

### 蜜月旅行
```bash
python scripts/main.py --destination "马尔代夫" --days 7 --budget "豪华" --companions 2 --interests "浮潜,SPA,日落晚餐"
```

### 文化深度游
```bash
python scripts/main.py --destination "西安" --days 3 --budget "经济" --interests "历史,考古,面食"
```

---

## 输出文件示例

```bash
# 生成并保存为Markdown文件
python scripts/main.py --destination "北海道" --days 6 --budget "舒适" --output hokkaido_guide.md

# 使用不同LLM后端
python scripts/main.py --destination "曼谷" --days 4 --budget "穷游" --provider deepseek
```
