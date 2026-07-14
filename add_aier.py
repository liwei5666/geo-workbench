#!/usr/bin/env python3
"""Add 爱尔眼科 as a new potential client"""

NEW_CLIENT = """
{
        id: "pc144",
        company: "爱尔眼科",
        industry: "医疗-眼科连锁",
        estimatedBudget: "200-500万",
        geoNeed: "眼科品牌GEO、全国连锁本地化搜索、AI搜索品牌占位",
        contactPerson: "市场品牌部",
        phone: "400-700-2888",
        website: "https://www.aierchina.com",
        location: "总部长沙，全国连锁",
        potentialScore: 93,
        reason: "中国最大眼科连锁上市公司(300015)，2000+门店覆盖全国，每年巨额营销投入",
        lastContact: null,
        notes: "品牌GEO+全国各门店本地化搜索优化，营收超200亿，市场预算充裕"
      }"""

with open('index.html', 'r') as f:
    content = f.read()

# Find the last potential client entry (pc143)
target = 'pc143'
pos = content.find(target)
if pos < 0:
    print("ERROR: Could not find end of potential clients")
    exit(1)

# Find the actual end of pc143 entry
end_pc143 = content.find('}\n    ],\n    completedBidding', pos)
if end_pc143 < 0:
    print("ERROR: Could not find completedBidding marker")
    exit(1)

# Insert new client
insert_pos = end_pc143 + 1
new_content = content[:insert_pos] + ',\n' + NEW_CLIENT + content[insert_pos:]

with open('index.html', 'w') as f:
    f.write(new_content)

print("Successfully added 爱尔眼科 as pc144")
print(f"File size: {len(new_content)} bytes")
