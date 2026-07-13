# Workplace Productivity Suite 使用示例

## 📄 简历优化

### 示例 1：产品经理简历
```bash
python scripts/main.py --mode resume \
  --input "负责公司App产品，用户从10万增长到100万，主导了3次大版本迭代，跟开发设计测试协作" \
  --target "高级产品经理"
```

### 示例 2：销售简历
```bash
python scripts/main.py --mode resume \
  --input "做了3年B端销售，年度业绩连续2年第一，管理5人团队，开拓了华东市场" \
  --target "销售总监"
```

---

## ✉️ 商务邮件

### 示例 1：客户跟进
```bash
python scripts/main.py --mode email \
  --scenario "客户跟进" \
  --details "上周给客户发了方案，还没有回复，想跟进一下" \
  --language zh --tone "friendly"
```

### 示例 2：英文合作邀约
```bash
python scripts/main.py --mode email \
  --scenario "合作邀约" \
  --details "We are an AI translation startup looking to partner with cross-border e-commerce companies" \
  --language en --tone "professional"
```

### 示例 3：催款
```bash
python scripts/main.py --mode email \
  --scenario "催款" \
  --details "客户A公司，合同金额50万，已超付款期限30天，之前沟通过一次说月底付" \
  --tone "urgent"
```

---

## 🔢 Excel公式

### 示例 1：查找匹配
```bash
python scripts/main.py --mode excel \
  --query "在A列查找员工工号，返回对应的B列姓名和C列部门"
```

### 示例 2：条件统计
```bash
python scripts/main.py --mode excel \
  --query "统计本月销售额大于10万的客户数量，并按地区分组"
```

### 示例 3：日期计算
```bash
python scripts/main.py --mode excel \
  --query "根据入职日期计算每个员工的工作年限，精确到天"
```

---

## 📋 合同模板

### 示例 1：保密协议
```bash
python scripts/main.py --mode contract \
  --type "保密协议（NDA）" \
  --party-a "北京科技有限公司" \
  --party-b "上海创新工作室"
```

### 示例 2：合作协议
```bash
python scripts/main.py --mode contract \
  --type "项目合作协议" \
  --party-a "甲方公司" \
  --party-b "乙方公司" \
  --details "共同开发AI翻译产品，甲方出技术，乙方出资金，利润分配5:5"
```
