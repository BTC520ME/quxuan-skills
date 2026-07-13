# 💼 Workplace Productivity Suite | 趣选职场效率工具箱

> **4合1职场神器** · 简历·邮件·Excel·合同 一站搞定

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)]()
[![Price](https://img.shields.io/badge/price-$4.99-blue.svg)](pricing)

---

## 🎯 四大核心模块

| 模块 | 功能 | 痛点解决 |
|------|------|---------|
| 📄 简历优化 | STAR法则重构 + 量化成果 + ATS友好 | 投100份没回音 |
| ✉️ 商务邮件 | 多场景模板 + 中英双语 + 语气调节 | 邮件写了删删了写 |
| 🔢 Excel公式 | 自然语言→公式 + 详细解释 | 搜半天公式还不对 |
| 📋 合同模板 | 标准模板 + 条款提醒 | 合同不知怎么写 |

---

## 🚀 安装与使用

```bash
openclaw install quxuan-workplace
```

### 📄 简历优化

```bash
python scripts/main.py --mode resume \
  --input "负责公司App产品，用户从10万增长到100万，主导了3次大版本迭代" \
  --target "高级产品经理"
```

**效果对比：**
```
❌ 优化前：负责公司App产品
✅ 优化后：主导核心App产品从0到100万用户增长（+900%），
    规划并交付3次重大版本迭代，用户留存率提升35%，
    带动营收增长¥200万/季度
```

### ✉️ 商务邮件

```bash
# 英文合作邀约
python scripts/main.py --mode email \
  --scenario "合作邀约" \
  --details "我们是做AI翻译的公司，想找一家做跨境电商的公司合作" \
  --language en \
  --tone "professional"
```

### 🔢 Excel公式

```bash
python scripts/main.py --mode excel \
  --query "根据A列的日期，找出对应B列中的最大值，返回C列的人名"
```

**输出示例：**
```
📌 公式：
=INDEX(C:C,MATCH(MAXIFS(B:B,A:A,">="&DATE(2024,1,1)),B:B,0))

📖 解释：
- MAXIFS：找出A列日期>=2024-01-01中，B列的最大值
- MATCH：定位最大值的位置
- INDEX：返回该位置对应的C列人名

💡 示例数据：
| A列(日期) | B列(分数) | C列(姓名) |
|-----------|-----------|-----------|
| 2024-03-01 | 85 | 张三 |
| 2024-03-15 | 92 | 李四 |
→ 结果：李四
```

---

## 💰 定价

**一次性购买 $4.99**，终身使用，免费更新。

## 📝 License

MIT License
## 🛡️ Enterprise Features
- Input sanitization & injection protection 输入清洗防注入
- Rate limiting & DDoS protection 限流保护
- Auto-retry with exponential backoff 自动重试
- Connection pooling for high performance 连接池高性能
- Cross-skill recommendations 交叉推荐引流