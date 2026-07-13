# ClawHub 发布全流程指南

**更新日期**：2026-07-09
**适用版本**：趣选 v2.1.0 企业级终极版

---

## 1. 发布前准备

### 1.1 环境检查

**🖥️ 电脑操作**

```bash
# 1. 检查Node.js版本（需>=16）
node --version

# 2. 安装ClawHub CLI（如未安装）
npm install -g @clawhub/cli

# 3. 检查版本
clawhub --version
```

### 1.2 文件准备

**确认文件完整性**

```bash
# 进入Skill目录
cd /path/to/quxuan-travel

# 检查文件结构
tree -L 2

# 应包含：
# ├── SKILL.md
# ├── clawhub.json
# ├── README.md
# ├── requirements.txt
# ├── scripts/
# │   ├── main.py
# │   └── enterprise.py
# └── examples/
#     └── demo-prompts.md
```

### 1.3 依赖安装

```bash
# 安装Python依赖
pip install -r requirements.txt

# 验证依赖
python -c "import httpx; print(httpx.__version__)"
```

---

## 2. ClawHub 账号设置

### 2.1 注册/登录

**🖥️ 电脑操作**

```bash
# 1. 登录ClawHub
clawhub login

# 2. 浏览器会自动打开，完成OAuth授权
# 3. 授权成功后，CLI会显示"Login successful"
```

**备选方案（Web端）**
1. 访问 https://clawhub.ai
2. 点击"Login"
3. 使用GitHub/Google账号登录
4. 进入Dashboard

### 2.2 设置收款信息

**🖥️ 电脑操作**

1. 登录 https://clawhub.ai/dashboard
2. 点击"Settings" → "Payments"
3. 连接Stripe Connect：
   - 点击"Connect Stripe"
   - 填写银行账户信息
   - 完成身份验证
4. 设置付款阈值（最低$20）

**📱 手机端查看**
- 登录 clawhub.ai/dashboard
- 可查看：收益、下载量、用户评价

---

## 3. Skill 验证

### 3.1 本地测试

**🖥️ 电脑操作**

```bash
# 1. 验证Skill结构
clawhub validate .

# 应输出：
# ✓ SKILL.md is valid
# ✓ clawhub.json is valid
# ✓ README.md is valid
# ✓ requirements.txt is valid
# ✓ All scripts are valid
# Validation passed!

# 2. 本地测试运行
python scripts/main.py --help

# 3. 测试实际调用（需要API Key）
export DASHSCOPE_API_KEY="your-key"
python scripts/main.py --input "测试输入" --output test_output.md
```

### 3.2 修复验证问题

**如验证失败**

```bash
# 1. 查看错误信息
clawhub validate . 2>&1 | tee validation.log

# 2. 常见问题及修复：
# - SKILL.md格式错误 → 检查frontmatter
# - clawhub.json缺少必填字段 → 补充name/version/description
# - Python语法错误 → python -m py_compile scripts/main.py

# 3. 重新验证
clawhub validate .
```

---

## 4. 发布 Skill

### 4.1 发布单个Skill

**🖥️ 电脑操作**

```bash
# 1. 进入Skill目录
cd /path/to/quxuan-travel

# 2. 发布
clawhub publish .

# 3. 确认发布信息：
# - Name: quxuan-travel
# - Version: 2.1.0
# - Price: FREE
# - Press 'y' to confirm

# 4. 等待上传完成（1-3分钟）
# 5. 发布成功后会显示URL：
# Published: https://clawhub.ai/skills/quxuan-travel
```

### 4.2 批量发布（6个Skill）

**🖥️ 电脑操作**

```bash
#!/bin/bash
# publish_all.sh

SKILLS=(
    "quxuan-travel"
    "quxuan-daily"
    "quxuan-workplace"
    "quxuan-copywriter"
    "quxuan-professional"
    "quxuan-revenue-engine"
)

for skill in "${SKILLS[@]}"; do
    echo "================================"
    echo "Publishing: $skill"
    echo "================================"
    
    cd "/path/to/$skill"
    
    # 验证
    echo "Validating..."
    clawhub validate .
    
    # 发布
    echo "Publishing..."
    clawhub publish . --yes
    
    echo "✓ $skill published successfully"
    echo ""
done

echo "================================"
echo "All skills published!"
echo "================================"
```

**执行脚本**
```bash
chmod +x publish_all.sh
./publish_all.sh
```

### 4.3 Web端发布（备选方案）

**🖥️ 电脑操作**

1. 访问 https://clawhub.ai/upload
2. 拖拽ZIP文件到上传区域
   - ZIP文件包含完整Skill目录
3. 填写元数据：
   - Name: quxuan-travel
   - Version: 2.1.0
   - Description: 专业旅行规划助手
   - Price: FREE
4. 点击"Upload"
5. 等待审核（通常5-10分钟）

---

## 5. 发布后检查

### 5.1 验证发布成功

**🖥️ 电脑操作**

```bash
# 1. 搜索Skill
clawhub search quxuan-travel

# 2. 查看详情
clawhub info quxuan-travel

# 3. 测试安装
clawhub install quxuan-travel
```

**📱 手机端查看**
1. 访问 https://clawhub.ai/skills/quxuan-travel
2. 检查：
   - 页面是否正常显示
   - 描述是否完整
   - 定价是否正确
   - 示例是否可用

### 5.2 收集初始反馈

**发布后24小时**

```bash
# 1. 查看下载量
clawhub stats quxuan-travel

# 2. 查看评价
clawhub reviews quxuan-travel

# 3. 查看使用数据
clawhub analytics quxuan-travel
```

**📱 手机端查看**
- 登录 https://clawhub.ai/dashboard
- 查看：Downloads、Ratings、Revenue

---

## 6. 推广策略

### 6.1 首发推广（第1周）

**📱 手机操作**

**1. Product Hunt发布**
```
时间：周二/周三 12:01 AM PST
标题：Quxuan - Enterprise-grade AI Skills at Personal Prices
描述：6 AI skills for developers, content creators, and teams. 
      Enterprise architecture, 60% cheaper than competitors.
标签：AI, Developer Tools, Productivity
```

**2. Hacker News发布**
```
标题：Show HN: Quxuan – Enterprise-grade AI skills at personal prices
链接：https://clawhub.ai/skills/quxuan-travel
```

**3. V2EX/掘金/知乎**
```
标题：【开源】趣选：企业级AI Skill套件，个人价格
内容：
- 介绍产品定位
- 展示技术架构
- 对比竞品（Jasper/Copy.ai）
- 提供试用链接
```

### 6.2 社区运营（持续）

**📱 手机操作**

**1. 建立Discord社群**
- 创建服务器：Quxuan Community
- 频道：#general、#support、#feature-requests、#showcase
- 邀请链接：https://discord.gg/xxxxx

**2. 建立微信群**
- 群名：趣选用户交流群
- 群规：禁止广告，鼓励分享
- 定期活动：功能投票、BUG反馈奖励

**3. 推荐奖励计划**
```
推荐1人：送1个月Pro版
推荐5人：送3个月Pro版
推荐10人：送1年Pro版
```

### 6.3 内容营销（持续）

**📱 手机操作**

**1. 技术博客（每周1篇）**
- 主题：企业级架构实践
- 平台：掘金、知乎、Medium
- 示例：《如何用AtomicFileWriter实现原子写入》

**2. 对比视频（每月1个）**
- 主题：趣选 vs Jasper vs Copy.ai
- 平台：B站、YouTube
- 内容：功能对比、性能测试、价格对比

**3. 用户案例（持续收集）**
- 收集用户成功故事
- 制作案例研究
- 在官网展示

---

## 7. 版本更新

### 7.1 更新流程

**🖥️ 电脑操作**

```bash
# 1. 修改代码
vim scripts/main.py

# 2. 更新版本号
vim clawhub.json
# "version": "2.1.1"

# 3. 更新SKILL.md
vim SKILL.md
# 更新版本号和更新日志

# 4. 验证
clawhub validate .

# 5. 发布新版本
clawhub publish . --yes

# 6. 用户会自动收到更新通知
```

### 7.2 更新日志

**在SKILL.md中添加**

```markdown
## Changelog

### v2.1.1 (2026-07-15)
- Fix: 修复XXBUG
- Feat: 新增XX功能
- Perf: 优化XX性能

### v2.1.0 (2026-07-09)
- Initial release
- 6 enterprise modules
- Multi-language support
```

---

## 8. 监控与维护

### 8.1 日常监控

**📱 手机操作（每日）**

1. **查看数据**
   - 登录 https://clawhub.ai/dashboard
   - 检查：Downloads、Ratings、Revenue
   - 时间：每天9:00

2. **回复评价**
   - 查看用户评价
   - 回复负面评价（24小时内）
   - 感谢正面评价

3. **处理工单**
   - 查看支持工单
   - 回复用户问题
   - 优先级：BUG > 功能请求 > 一般咨询

### 8.2 定期维护

**🖥️ 电脑操作（每月）**

1. **性能监控**
   ```bash
   # 查看API调用统计
   clawhub analytics quxuan-travel --period 30d
   
   # 查看错误率
   clawhub errors quxuan-travel --period 30d
   ```

2. **依赖更新**
   ```bash
   # 检查依赖更新
   pip list --outdated
   
   # 更新依赖
   pip install --upgrade httpx
   
   # 测试兼容性
   python scripts/main.py --help
   ```

3. **安全审计**
   ```bash
   # 检查安全漏洞
   pip-audit
   
   # 检查代码质量
   flake8 scripts/
   pylint scripts/
   ```

---

## 9. 常见问题

### 9.1 发布失败

**Q: clawhub publish 失败，提示"Authentication required"**
A: 重新登录：`clawhub login`

**Q: 提示"Validation failed"**
A: 运行 `clawhub validate .` 查看详细错误

**Q: 上传超时**
A: 检查网络连接，或使用Web端上传

### 9.2 收款问题

**Q: 何时收到付款？**
A: 每月15日打款（上月收益），最低$20起提

**Q: 如何查看收益？**
A: 登录 https://clawhub.ai/dashboard → Revenue

**Q: 税率是多少？**
A: 平台抽成20%，税务自理

### 9.3 用户反馈

**Q: 如何处理负面评价？**
A: 
1. 24小时内回复
2. 承认问题，说明修复计划
3. 提供补偿（如免费升级）
4. 修复后邀请用户更新评价

**Q: 如何处理功能请求？**
A:
1. 记录到待办列表
2. 评估可行性和优先级
3. 在社群投票
4. 实现后通知请求者

---

## 10. 检查清单

### 10.1 发布前检查

- [ ] Node.js版本>=16
- [ ] ClawHub CLI已安装
- [ ] 已登录ClawHub账号
- [ ] 已设置Stripe Connect
- [ ] 所有文件完整（SKILL.md、clawhub.json、README.md等）
- [ ] 依赖已安装（requirements.txt）
- [ ] 本地测试通过（clawhub validate .）
- [ ] 版本号已更新

### 10.2 发布后检查

- [ ] Skill已发布成功
- [ ] 页面显示正常
- [ ] 描述完整准确
- [ ] 定价正确
- [ ] 示例可用
- [ ] 已设置推广计划
- [ ] 已建立用户反馈渠道

### 10.3 持续运营检查

- [ ] 每日查看数据
- [ ] 每日回复评价
- [ ] 每周发布内容
- [ ] 每月更新版本
- [ ] 每月安全审计

---

## 11. 联系方式

**ClawHub支持**
- 官网：https://clawhub.ai
- 文档：https://docs.clawhub.ai
- 支持邮箱：support@clawhub.ai
- Discord：https://discord.gg/clawhub

**技术支持**
- 微信：wuxiang-ai
- 邮箱：support@quxuan.ai
- GitHub：https://github.com/BTC520ME

---

**文档版本**：v1.0
**更新日期**：2026-07-09
**适用版本**：趣选 v2.1.0
