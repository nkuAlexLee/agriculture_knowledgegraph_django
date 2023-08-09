from py2neo import Graph, Node, Relationship, ClientError
import openpyxl
import re
import base64
import csv

# 连接到Neo4j数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))


# ency_content存储
_str = """
- 界面配置（没啥用了）
ENTITY 必须要有ENTITY或者是RELATION
= 
- 实体对外展示内容（没啥用了）
NAME=
IMG=
CONTENT=
TITLE=
- 实体界面信息"""
"""
data_list格式
[
    {
        "title":"标题，默认都是二级标题，如果你不希望这段话有标题，就不需要这个字段，或者留空",
        "level":"几级标题，int，2~6，虽然我觉得这个用不到（，用不到就不要这个字段就行，是不需要！！",
        "content":"对应的文本,这个文本需要换行的话必须用<br>，分段落需要\n\n，要不然前端是无法换行（段落）的"
    }
]
"""


def encyInit(data_list, name):
    _str = """
- 界面配置（没啥用了）
ENTITY 必须要有ENTITY或者是RELATION
= 
- 实体对外展示内容（没啥用了）
NAME=
IMG=
CONTENT=
TITLE=
- 实体界面信息
    """
    temp = _str
    temp += "\n\n" + f"= {name} ="
    for data in data_list:
        if data.get("title") != None and data.get("title") != "":
            if data.get("level") == None:
                title = f"== {data.get('title')} =="
            else:
                title = "="
                title = title * data.get("level")
                title = title + " " + data.get('title') + " " + title
            temp += "\n\n" + title
        temp += "\n\n" + data.get("content")

    return temp


# 公司
test = [
    {
        "title": "简介",
        "content": "今天是个好天气"
    },
    {
        "title": "历史",
        "content": "今天是个好天气"
    },
    {
        "title": "百度百科",
        "content": "今天是个好天气"
    },
]

# 人物
test = [
    {
        "title": "简介",
        "content": "今天是个好天气"
    },

]


# print(encyInit(_str, test))


str_table = """{{表格|font-size:20;min-width:200px;width:100%"""

table_list = [
    {
        "title": "属性名字",
        "content": "属性内容"
    },
    {
        "title": "属性名字",
        "content": "属性内容"
    },
    {
        "title": "属性名字",
        "content": "属性内容"
    },
    {
        "title": "属性名字",
        "content": "属性内容"
    },
    {
        "title": "属性名字",
        "content": "属性内容"
    },
    {
        "title": "属性名字",
        "content": "属性内容"
    },
    {
        "title": "属性名字",
        "content": "属性内容"
    },
    {
        "title": "属性名字",
        "content": "属性内容"
    },
    {
        "title": "属性名字",
        "content": "属性内容"
    }
]


def tableInit(table_list, name):
    str_table = """{{表格|font-size:20;min-width:200px;width:100%"""
    temp = str_table
    temp += "\n" + f"|+ {name} c=6/t |"
    i = int(len(table_list) / 6)
    j = int(len(table_list) % 6)
    if j != 0:
        i = i + 1
    for k in range(0, i):
        t = []
        c = []
        for l in range(0, 6):
            if l + k * 6 >= len(table_list):
                t.append("")
                c.append("")
            else:
                t.append(table_list[l + k * 6]["title"])
                c.append(table_list[l + k * 6]["content"])
        t_s = f"| {t[0]} t| {t[1]} t| {t[2]} t| {t[3]} t| {t[4]} t| {t[5]} t|"
        c_s = f"| {c[0]} | {c[1]} | {c[2]} | {c[3]} | {c[4]} | {c[5]} |"
        temp += "\n" + t_s
        temp += "\n" + c_s
    temp += "\n" + "}}"
    return temp


def set_encycontent_for_company():
    i = 0
    nodes = graph.run(
        "MATCH (node:Company) RETURN node.name AS node_name, node.establishmentDate AS node_establishmentDate, node.resumme AS node_resume,node.history AS node_history,node.baike AS node_baike,"
        "node.officeAddress AS node_officeAddress, node.leadUnderwriter AS node_leadUnderwriter,"
        "node.actualController AS node_actualController, node.secretary AS node_secretary,"
        "node.registrationCapital AS node_registrationCapital, node.employeeNumber AS node_employeeNumber,"
        "node.industry AS node_industry, node.productName AS node_productName,"
        "node.stockName AS node_stockName, node.stockCode AS node_stockCode,"
        "node.website AS node_website"
    ).data()
    for node in nodes:
        if not node['node_stockName']:
            continue
        i = i+1
        table_list = []
        if node['node_establishmentDate']:
            table_list.append({
                "title": "创建时间",
                "content": node['node_establishmentDate']
            })
        if node['node_officeAddress']:
            table_list.append({
                "title": "办公地点",
                "content": node['node_officeAddress']
            })
        if node['node_leadUnderwriter']:
            table_list.append({
                "title": "主承销商",
                "content": node['node_leadUnderwriter']
            })
        if node['node_actualController']:
            table_list.append({
                "title": "董事长",
                "content": node['node_actualController']
            })
        if node['node_secretary']:
            table_list.append({
                "title": "董秘",
                "content": node['node_secretary']
            })
        if node['node_registrationCapital']:
            table_list.append({
                "title": "注册资金",
                "content": node['node_registrationCapital']
            })
        if node['node_employeeNumber']:
            table_list.append({
                "title": "员工数量",
                "content": node['node_employeeNumber']
            })
        if node['node_industry']:
            table_list.append({
                "title": "产业",
                "content": node['node_industry']
            })
        if node['node_productName']:
            table_list.append({
                "title": "产品名称",
                "content": node['node_productName']
            })
        if node['node_stockName']:
            table_list.append({
                "title": "股票名称",
                "content": node['node_stockName']
            })
        if node['node_stockCode']:
            table_list.append({
                "title": "股票代码",
                "content": node['node_stockCode']
            })
        if node['node_website']:
            table_list.append({
                "title": "公司网址",
                "content": node['node_website']
            })

        node_list = []
        if table_list:
            node_list.append({
                "title": "公司信息",
                "content": tableInit(table_list, node['node_name']),
            })

        if node['node_resume']:
            node_list.append({
                "title": "公司简介",
                "content": node['node_resume'].replace('\n', '\n\n')
            })

        if node['node_history']:
            node_list.append({
                "title": "公司历史",
                "content": node['node_history'].replace('\n', '\n\n')
            })

        if node['node_baike']:
            node_list.append({
                "title": "百度百科",
                "content": node['node_baike'].replace('\n', '\n\n')
            })

        ency_content = encyInit(node_list, node['node_name'])
        set_encycontent(node['node_name'], ency_content.replace('\'', ''))
        print('进度: '+str(i)+'/107090')

# print(tableInit(str_table, table_list, "测试"))


def set_encycontent_for_Person():
    i = 0
    nodes = graph.run(
        "MATCH (node:Person) RETURN node.name AS node_name,node.resume AS node_resume"
    ).data()
    for node in nodes:
        if not node['node_resume']:
            i = i+1
            node_list = []
            ency_content = encyInit(node_list, node['node_name'])
            # print(ency_content)
            set_encycontent(node['node_name'].replace(
                '\'', ''), ency_content.replace('\'', ''))
            print('进度: '+str(i)+'/72019')


def set_encycontent(name, encycontent_value):
    query = f"""
        MATCH (node:Company {{name: '{name}'}})
        SET node.encycontent = '{encycontent_value}'
    """
    graph.run(query)


set_encycontent_for_company()

