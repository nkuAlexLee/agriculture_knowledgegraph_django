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


# 实体信息直接查询
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


# 单实体直接关系查询
@csrf_exempt
def searchNodeRelationship(node_name):
    """
    实体直接关系查询

    参数：
    node_name: 节点名称

    返回值：
    查询到的关系数据，如果没有找到则返回None
    """
    try:
        query = """
            MATCH (node {name: $node_name}) -[r]- (related)
            RETURN related.name AS related_node_name, type(r) AS relationship_type;
        """
        result = graph.run(query, node_name=node_name)
        return result.data()
    except ClientError as e:
        print(f"Error searching node relationship: {e}")
        return None


# 单实体多层嵌套关系查询
@csrf_exempt
def searchNodeNestedRelationship(node_name, depth):
    """
    实体多层嵌套关系查询

    参数：
    node_name: 节点名称
    depth: 查询深度

    返回值：
    查询到的嵌套关系数据，如果没有找到则返回None
    """
    try:
        query = """
            MATCH (node {name: $node_name})-[*..""" + str(depth) + """]-(related)
            RETURN related.name AS related_node_name;
        """
        result = graph.run(query, node_name=node_name)
        return [record['related_node_name'] for record in result if record['related_node_name'] != None]
    except ClientError as e:
        print(f"Error searching nested relationship: {e}")
        return None


# 实体间关系查询
@csrf_exempt
def searchRelationshipBetween(start_node_name, end_node_name, method):
    """
    实体间关系查询

    参数：
    start_node_name: 起始节点名称
    end_node_name: 终止节点名称
    method: 查询方式，"1"为最短关系，"2"为最长关系，"3"为最短的十条关系

    返回值：
    查询到的关系数据，如果没有找到则返回None
    """
    try:
        if method == "1":
            query = """
                MATCH (startNode {name: $start_name}), (endNode {name: $end_name})
                MATCH path = shortestPath((startNode)-[*]-(endNode))
                UNWIND relationships(path) AS r
                RETURN r;
            """
        elif method == "2":
            query = """
                MATCH (startNode {name: $start_name}), (endNode {name: $end_name})
                MATCH path = (startNode)-[*]-(endNode)
                UNWIND relationships(path) AS r
                RETURN r ORDER BY length(path) DESC LIMIT 1;
            """
        elif method == "3":
            query = """
                MATCH (startNode {name: $start_name}), (endNode {name: $end_name})
                MATCH path = allShortestPath((startNode)-[*]-(endNode))
                UNWIND relationships(path) AS r
                RETURN r LIMIT 10;
            """
        else:
            raise ValueError(
                "Invalid method value. Supported values are '1', '2', and '3'.")

        result = graph.run(query, start_name=start_node_name,
                           end_name=end_node_name)
        # 逐条打印返回的关系信息，按照指定格式输出
        output_list = []
        for record in result:
            relationship_data = record['r']
            output = f"[[{start_node_name}]]--[[{end_node_name}]]= {relationship_data['type']}={{ relationship_data['data'] }}"
            output_list.append(output)

        return output_list if output_list else []

    except ClientError as e:
        print(f"Error searching relationship: {e}")
        return None


# print(searchRelationshipBetween('Laurence Fishburne', 'Lana Wachowski', '1'))


@csrf_exempt
def json_response(answer):
    print(answer)
    return HttpResponse(json.dumps(answer, ensure_ascii=False))
