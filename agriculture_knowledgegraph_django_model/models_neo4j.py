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


# print(tableInit(str_table, table_list, "测试"))


def set_encycontent_for_company():
    i = 0
    nodes = graph.run(
        "MATCH (node:Company) RETURN node.name AS node_name,node.resume AS node_resume"
    ).data()
    for node in nodes:
        if not node['node_resume']:
            i = i+1
            node_list = []
            ency_content = encyInit(node_list, node['node_name'])
            # print(ency_content)
            set_encycontent(node['node_name'].replace(
                '\'', ''), ency_content.replace('\'', ''))
            print('进度: '+str(i)+'/50000')


def set_encycontent(name, encycontent_value):
    query = f"""
        MATCH (node:Company {{name: '{name}'}})
        SET node.encycontent = '{encycontent_value}'
    """
    graph.run(query)


set_encycontent_for_company()
