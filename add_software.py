#!/usr/bin/env python3
"""Add new 2026 SaaS software products to the geo-workbench index.html"""

NEW_PRODUCTS = """{
        id: "sw013",
        name: "飞书2026",
        category: "协作办公SaaS",
        developer: "字节跳动",
        launchDate: "2026-03-19",
        website: "https://www.feishu.cn",
        productDescription: "AI Agent原生协作平台，从办公协作工具升级为AI原生平台",
        coreFeatures: ["AI Agent智能助手飞书aily", "飞书妙搭低代码平台", "多维表格Agent", "智能文档协作", "视频会议AI总结"],
        pricing: {
          免费版:"基础功能免费",
          企业版:"¥50/人/月",
          旗舰版:"¥99/人/月"
        },
        targetUsers: "互联网/科技公司、追求高效协同的企业",
        adOpportunity: "极高 - 飞书2026大版本升级，市场推广预算充足",
        notes: "2026年3月发布，从协作平台跃迁为AI Agent原生平台，需大量GEO品牌占位"
      },
{
        id: "sw014",
        name: "销售易NeoCRM",
        category: "CRM客户管理",
        developer: "销售易（北京仁科互动）",
        launchDate: "2026-04-01",
        website: "https://www.xiaoshouyi.com",
        productDescription: "新一代智能CRM平台Neo版本，AI全面融入销售管理",
        coreFeatures: ["AI智能销售预测", "商机自动评分", "智能内容生成", "移动端全功能", "企业微信/钉钉深度整合"],
        pricing: {
          基础版:"¥60/人/月",
          企业版:"¥120/人/月",
          旗舰版:"定制报价"
        },
        targetUsers: "20-500人中型企业，制造业、消费品行业",
        adOpportunity: "高 - 国产CRM升级换代窗口期",
        notes: "2026年Neo平台全面升级，AI能力显著提升"
      },
{
        id: "sw015",
        name: "合思·企业费控",
        category: "财务SaaS",
        developer: "合思科技（原易快报）",
        launchDate: "2026-05-01",
        website: "https://www.hescrm.com",
        productDescription: "全链路企业费控与财务SaaS平台",
        coreFeatures: ["移动报销", "AI发票识别与真伪查验", "智能审批", "预算管控", "财务数据分析"],
        pricing: {
          标准版:"¥5万/年",
          专业版:"¥15万/年",
          企业版:"¥30万/年"
        },
        targetUsers: "中大型企业、上市公司",
        adOpportunity: "高 - 品牌升级期，搜索推广预算充足",
        notes: "2026年品牌升级，从费控报销扩展为全链路财务SaaS"
      },
{
        id: "sw016",
        name: "Udesk全渠道客服",
        category: "客服SaaS",
        developer: "沃丰科技",
        launchDate: "2026-04-15",
        website: "https://www.udesk.cn",
        productDescription: "全渠道智能客服平台，内置AI大模型",
        coreFeatures: ["全渠道接入", "AI智能应答", "工单管理", "呼叫中心", "数据分析看板"],
        pricing: {
          标准版:"¥6,000/年起",
          专业版:"¥18,000/年起",
          企业版:"定制报价"
        },
        targetUsers: "电商、零售、金融、教育行业",
        adOpportunity: "高 - 客服AI升级浪潮",
        notes: "2026年接入AI大模型能力，智能客服赛道竞争激烈"
      },
{
        id: "sw017",
        name: "简道云零代码",
        category: "零代码SaaS",
        developer: "帆软软件",
        launchDate: "2026-03-01",
        website: "https://www.jiandaoyun.com",
        productDescription: "零代码企业应用搭建平台",
        coreFeatures: ["表单拖拽搭建", "流程自动化", "数据仪表盘", "跨应用集成", "移动端适配"],
        pricing: {
          免费版:"基础功能免费",
          团队版:"¥2,000/年",
          企业版:"¥8,000/年",
          旗舰版:"¥30,000/年"
        },
        targetUsers: "中小企业、业务部门、IT部门",
        adOpportunity: "中 - 零代码赛道竞争激烈",
        notes: "2026年持续迭代，企业数字化标配工具"
      },
{
        id: "sw018",
        name: "ONES研发管理",
        category: "项目管理SaaS",
        developer: "ONES（深圳）",
        launchDate: "2026-02-01",
        website: "https://www.ones.cn",
        productDescription: "企业级研发项目管理与DevOps平台",
        coreFeatures: ["需求管理", "敏捷看板", "代码仓库集成", "CI/CD流水线", "效能度量"],
        pricing: {
          基础版:"免费",
          团队版:"¥199/人/月",
          企业版:"定制报价"
        },
        targetUsers: "互联网研发团队、软件公司",
        adOpportunity: "高 - 研发管理SaaS赛道快速增长",
        notes: "2026年AI辅助研发功能增强"
      },
{
        id: "sw019",
        name: "Teambition 2026",
        category: "项目管理SaaS",
        developer: "阿里巴巴",
        launchDate: "2026-03-01",
        website: "https://www.teambition.com",
        productDescription: "企业级敏捷项目管理与协作平台",
        coreFeatures: ["敏捷看板", "需求管理", "文档协作", "甘特图", "AI智能排期"],
        pricing: {
          免费版:"基础功能免费",
          专业版:"¥199/人/月",
          企业版:"定制报价"
        },
        targetUsers: "互联网团队、产品研发团队",
        adOpportunity: "中 - 与钉钉深度整合",
        notes: "2026年与钉钉融合更深入，AI排期能力增强"
      },
{
        id: "sw020",
        name: "智齿科技Bot",
        category: "智能客服SaaS",
        developer: "智齿科技",
        launchDate: "2026-05-01",
        website: "https://www.sobot.com",
        productDescription: "AI智能客服机器人平台",
        coreFeatures: ["智能问答机器人", "知识库自动构建", "人工客服工作台", "工单系统", "数据分析"],
        pricing: {
          基础版:"¥3,000/年起",
          专业版:"¥9,000/年起",
          企业版:"定制报价"
        },
        targetUsers: "电商、教育、金融行业",
        adOpportunity: "高 - AI客服赛道爆发",
        notes: "2026年推出新一代AI客服解决方案"
      },
{
        id: "sw021",
        name: "纷享销客CRM",
        category: "CRM客户管理",
        developer: "纷享销客（北京）",
        launchDate: "2026-04-01",
        website: "https://www.fxiaoke.com",
        productDescription: "连接型CRM平台，PaaS高度可定制",
        coreFeatures: ["客户管理", "销售自动化", "PaaS平台定制", "营销一体化", "BI分析"],
        pricing: {
          标准版:"¥99/人/月",
          专业版:"¥159/人/月",
          企业版:"定制报价"
        },
        targetUsers: "快消、IT服务、制造业",
        adOpportunity: "高 - CRM市场份额争夺激烈",
        notes: "2026年连接型CRM持续升级"
      },
{
        id: "sw022",
        name: "金蝶云·星辰",
        category: "小微企业云ERP",
        developer: "金蝶国际",
        launchDate: "2026-01-15",
        website: "https://www.kingdee.com",
        productDescription: "面向小微企业的云端ERP管理系统",
        coreFeatures: ["财务管理", "进销存管理", "智能开票", "报表分析", "多门店管理"],
        pricing: {
          基础版:"¥1,999/年",
          标准版:"¥3,999/年",
          专业版:"¥7,999/年"
        },
        targetUsers: "小微企业、商贸企业、多门店零售",
        adOpportunity: "中 - 小微企业ERP红海市场",
        notes: "2026年深化AI能力，与金蝶云星瀚协同"
      }"""

with open('index.html', 'r') as f:
    content = f.read()

# Find insertion point - after the last software entry before closing
target = '构设云'
pos = content.find(target)
if pos < 0:
    print("ERROR: Could not find target string")
    exit(1)

# Find the end of sw012's section
end_sw012 = content.find('}\n    ],\n    lastUpdated', pos)
if end_sw012 < 0:
    print("ERROR: Could not find end marker")
    exit(1)

# Insert new products before the closing ],\n    lastUpdated
insert_pos = end_sw012 + 1  # after the }
new_content = content[:insert_pos] + ',\n' + NEW_PRODUCTS + content[insert_pos:]

with open('index.html', 'w') as f:
    f.write(new_content)

print("Successfully added 10 new software products (sw013-sw022)")
print(f"File size: {len(new_content)} bytes")
