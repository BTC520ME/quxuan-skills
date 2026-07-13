# AI Recipe & Life Assistant 使用示例

## 菜谱生成示例

### 示例 1：经典家常菜
```bash
python scripts/main.py --dish "红烧肉" --servings 4
```

### 示例 2：带饮食限制
```bash
python scripts/main.py --dish "宫保鸡丁" --diet "无辣" --allergies "花生"
```

### 示例 3：素食菜谱
```bash
python scripts/main.py --dish "麻婆豆腐" --diet "素食" --servings 3
```

### 示例 4：新手友好
```bash
python scripts/main.py --dish "可乐鸡翅" --difficulty "入门" --servings 2
```

### 示例 5：保存为文件
```bash
python scripts/main.py --dish "水煮鱼" --servings 4 --output recipe_shuizhuyu.md
```

---

## 生活助手示例

### 清洁类
```bash
python scripts/main.py --lifestyle-query "白衣服染上了酱油怎么洗掉"
python scripts/main.py --lifestyle-query "不锈钢锅底烧焦了怎么清洁"
```

### 收纳类
```bash
python scripts/main.py --lifestyle-query "衣柜空间太小怎么高效收纳"
```

### 健康类
```bash
python scripts/main.py --lifestyle-query "经常对电脑眼睛干涩怎么办"
```

### 食物保存类
```bash
python scripts/main.py --lifestyle-query "买多了新鲜蔬菜怎么保存更久"
```
