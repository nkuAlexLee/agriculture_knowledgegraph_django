from py2neo import Graph, Node, Relationship, ClientError
from agriculture_knowledgegraph_django.utils import base64Decode, base64Encode
import openpyxl
import re
import sqlite3
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from datetime import date
import json
import time
import random


# 连接到Neo4j数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "xy639a58"))


# 解析文本内容，获取需要的参数
def parse(input_str):
    """
    解析文本内容，获取需要的参数

    参数：
    input_str: 输入的文本字符串

    返回值：
    如果匹配成功，返回元组 (a, b, friend, description, has_ai)，否则返回 None。
    """
    # 正则表达式模式
    pattern = r'\[\[([^]]+)\]\]--\[\[([^]]+)\]\]=([^=]+)={{([^{}]+)}}(=AI)?'

    input_str = base64Decode(input_str)

    # 使用正则表达式进行匹配
    match = re.search(pattern, input_str)

    if match:
        a = match.group(1)
        b = match.group(2)
        friend = match.group(3)
        description = match.group(4)
        has_ai = True if match.group(5) else False

        return a, b, friend, description, has_ai
    else:
        return None


# 实体信息直接查询接口
@csrf_exempt
def searchNode(request):
    """
    实体信息查询

    方式:
    实体的查询根据NAME匹配>OTHER_NAME匹配>ENCY_CONTENT匹配

    返回值：
    查询到的节点数据，如果没有找到则返回空数组
    """
    if request.method == 'POST':
        search_name = request.POST.get('search_name')
    else:
        return json_response({'success': False, 'content': []})

    try:
        query = f"""
            MATCH (node)
            WHERE node.name =~ '.*{search_name}.*' OR node.stockName =~ '.*{search_name}.*' OR node.resume =~ '.*{search_name}.*'
            RETURN node
            ORDER BY
            CASE
                WHEN node.name = '{search_name}' THEN 1
                WHEN node.name =~ '.*{search_name}.*' THEN 2
                WHEN node.stockName =~ '.*{search_name}.*' THEN 3
                WHEN node.resume =~ '.*{search_name}.*' THEN 4
                ELSE 5
            END;
         """
        result = graph.run(query)

        nodes = result.data()
        nodes_list = []
        index = 1
        for node in nodes:
            node_dict = {
                "id": node['node'].identity,
                "name": base64Encode(str(node["node"]["name"]).replace(search_name, '<span style="color: #822296; font-weight: 600">'+search_name+'</span>')),
                "abstract": base64Encode(str(node["node"]["resume"]).replace(search_name, '<span style="color: #822296; font-weight:600">'+search_name+'</span>')),
                "index": index
            }
            index = index + 1
            nodes_list.append(node_dict)

        return json_response({'success': True, 'content': {'result': nodes_list}})

    except ClientError as e:
        print(f"Error searching node: {e}")
        return None


# 实体识别接口
@csrf_exempt
def recognizeNode(request):

    if request.method == 'POST':
        text = request.POST.get('content')
    else:
        return json_response({'success': False, 'content': []})

    nodes = graph.run(
        "MATCH (node:Company) RETURN node.name AS node_name").data()

    # 用于跟踪已经替换过的节点名称及其替代文本
    replaced_nodes = {}

    for node in nodes:
        node_name = node["node_name"]

        # 如果节点名称还没有替代文本，则执行替换
        if node_name not in replaced_nodes:
            tagged_node = "[[" + node_name + "]]"
            text = text.replace(node_name, tagged_node)

            # 将节点名称及其替代文本添加到字典中
            replaced_nodes[node_name] = node_name

    print(base64Encode(text))
    return json_response({'success': True, 'content': {'result': base64Encode(text)}})


# 实体百科接口
@csrf_exempt
def getNodeDetail(request):

    if request.method == 'POST':
        id = int(request.POST.get('id'))
    else:
        return json_response({'success': False, 'content': []})

    # 节点ency_content返回
    nodes = graph.run(
        f"MATCH (node)-[r]-() WHERE id(node)={id} RETURN node.name AS node_name,node.encycontent AS node_encycontent").data()
    node = nodes[0]

    name = node['node_name']
    ency_content = node['node_encycontent']

    # 节点map_content返回
    nodes = graph.run(
        f"MATCH (node) -[r]- (related) WHERE id(node)={id} RETURN type(r) AS relationship,STARTNODE(r).name AS start_name,ENDNODE(r).name AS end_name").data()

    map_content = f"""- 界面配置
- 关系
[[{name}]]
"""
    for record in nodes:
        relationship = record['relationship']
        start_name = record['start_name']
        end_name = record['end_name']

        if relationship == "INVESTED_BY":
            relationship = "被投资"
            relationship_desc = f"{start_name}是被{end_name}所投资的"
        elif relationship == "BELONGS_TO_INDUSTRY":
            relationship = "所属产业"
            relationship_desc = f"{start_name}的所属产业是{end_name}"
        elif relationship == "OFFERS_PRODUCT":
            relationship = "提供业务"
            relationship_desc = f"{end_name}是{start_name}的其中一个提供业务"
        elif relationship == "WORKS_FOR":
            relationship = "就职于"
            relationship_desc = f"{start_name}就职于{end_name}"

        output = f"[[{start_name}]]--[[{end_name}]]={relationship}={relationship_desc}"
        map_content += (output + '\n')

    if ency_content == None:
        ency_content = ""
    if map_content == None:
        map_content = ""
    print(ency_content)
    print(map_content)

    return json_response({'success': True, 'content': {
        'name': base64Encode(name),
        'encycontent': base64Encode(ency_content),
        'mapcontent': base64Encode(map_content)

    }})


# # 单实体直接关系查询
# @csrf_exempt
# def searchNodeRelationship(node_name):
#     """
#     实体直接关系查询

#     参数：
#     node_name: 节点名称

#     返回值：
#     查询到的关系数据，如果没有找到则返回None
#     """
#     try:
#         query = """
#             MATCH (node {name: $node_name}) -[r]- (related)
#             RETURN related.name AS related_node_name, type(r) AS relationship_type;
#         """
#         result = graph.run(query, node_name=node_name)
#         return result.data()
#     except ClientError as e:
#         print(f"Error searching node relationship: {e}")
#         return None


# # 单实体多层嵌套关系查询
# @csrf_exempt
# def searchNodeNestedRelationship(node_name, depth):
#     """
#     实体多层嵌套关系查询

#     参数：
#     node_name: 节点名称
#     depth: 查询深度

#     返回值：
#     查询到的嵌套关系数据，如果没有找到则返回None
#     """
#     try:
#         query = """
#             MATCH (node {name: $node_name})-[*..""" + str(depth) + """]-(related)
#             RETURN related.name AS related_node_name;
#         """
#         result = graph.run(query, node_name=node_name)
#         return [record['related_node_name'] for record in result if record['related_node_name'] != None]
#     except ClientError as e:
#         print(f"Error searching nested relationship: {e}")
#         return None


# 实体间关系查询接口
@csrf_exempt
def searchRelationshipBetween(request):
    """
    实体间关系查询

    参数：
    start_node_name: 起始节点名称
    end_node_name: 终止节点名称
    method: 查询方式，"1"为最短关系，"2"为最长关系，"3"为最短的十条关系

    返回值：
    查询到的关系数据，如果没有找到则返回None
    """
    if request.method == "POST":
        start_node_name = request.POST.get('start_node_name')
        end_node_name = request.POST.get('end_node_name')
        method = request.POST.get('method')
    else:
        return json_response({'success': False, 'content': []})
    print(start_node_name)
    print(end_node_name)
    print(method)
    try:
        if method == "1":
            query = """
                MATCH (startNode {name: $start_name}), (endNode {name: $end_name})
                MATCH path = shortestPath((startNode)-[*]-(endNode))
                UNWIND relationships(path) AS r
                RETURN type(r) AS relationship,STARTNODE(r).name AS start_name,ENDNODE(r).name AS end_name;
            """
        elif method == "2":
            query = """
                MATCH (startNode {name: $start_name}), (endNode {name: $end_name})
                MATCH path = (startNode)-[*]-(endNode)
                UNWIND relationships(path) AS r
                RETURN type(r) AS relationship,STARTNODE(r).name AS start_name,ENDNODE(r).name AS end_name 
                ORDER BY length(path) DESC LIMIT 1;
            """
        else:
            raise ValueError(
                "Invalid method value. Supported values are '1', '2', and '3'.")

        result = graph.run(query, start_name=start_node_name,
                           end_name=end_node_name)
        # 逐条打印返回的关系信息，按照指定格式输出
        output_list = ""
        for record in result:
            relationship = record['relationship']
            start_name = record['start_name']
            end_name = record['end_name']

            if relationship == "INVESTED_BY":
                relationship = "被投资"
                relationship_desc = f"{start_name}是被{end_name}所投资的"
            elif relationship == "BELONGS_TO_INDUSTRY":
                relationship = "所属产业"
                relationship_desc = f"{start_name}的所属产业是{end_name}"
            elif relationship == "OFFERS_PRODUCT":
                relationship = "提供业务"
                relationship_desc = f"{end_name}是{start_name}的其中一个提供业务"
            elif relationship == "WORKS_FOR":
                relationship = "就职于"
                relationship_desc = f"{start_name}就职于{end_name}"

            output = f"[[{start_name}]]--[[{end_name}]]={relationship}={relationship_desc}"
            output_list += (output + '\n')
        print(output_list)

        return json_response({'success': True, 'content': {'result': base64Encode(output_list)}})

    except ClientError as e:
        print(f"Error searching relationship: {e}")
        return None


@csrf_exempt
def json_response(answer):
    print(answer)
    return HttpResponse(json.dumps(answer, ensure_ascii=False))
