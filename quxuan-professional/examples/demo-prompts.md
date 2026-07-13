# Legal & Tax Advisor Assistant 使用示例

## 📚 法律信息查询

### 劳动纠纷
```bash
python scripts/main.py --mode legal \
  --query "公司拖欠工资3个月怎么办"
```

### 消费维权
```bash
python scripts/main.py --mode legal \
  --query "网购商品质量问题，商家拒绝退货"
```

### 租房纠纷
```bash
python scripts/main.py --mode legal \
  --query "房东提前收房，不退还押金"
```

---

## 💰 报税指引

### 个人所得税
```bash
python scripts/main.py --mode tax \
  --query "自由职业者年收入30万，如何合理纳税"
```

### 专项附加扣除
```bash
python scripts/main.py --mode tax \
  --query "上有老下有小，哪些专项附加扣除可以享受"
```

### 年终奖
```bash
python scripts/main.py --mode tax \
  --query "年终奖10万，单独计税还是并入综合所得更划算"
```

---

## 🔍 合同审核

### 审核合同条款
```bash
python scripts/main.py --mode contract_review \
  --query "竞业限制条款：离职后2年内不得从事同行业工作，违约金50万，补偿金为月薪的30%"
```

### 从文件审核
```bash
python scripts/main.py --mode contract_review \
  --file lease_agreement.txt \
  --output review_report.md
```

---

## ⚖️ 劳动仲裁

### 被辞退
```bash
python scripts/main.py --mode labor \
  --query "被公司无故辞退，工作3年，月薪15000，没有提前通知"
```

### 加班争议
```bash
python scripts/main.py --mode labor \
  --query "公司强制996，不给加班费，工作2年，月薪12000"
```

### 未缴社保
```bash
python scripts/main.py --mode labor \
  --query "入职1年，公司一直没给我缴纳社保，月薪8000"
```
