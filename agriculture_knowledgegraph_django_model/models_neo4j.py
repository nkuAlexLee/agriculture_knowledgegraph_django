from py2neo import Graph, Node, Relationship, ClientError
import openpyxl
import re

# 连接到Neo4j数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))


# 解析文本内容，获取需要的参数
def parse(input_str):
    # 正则表达式模式
    
    pattern = r'\[\[([^]]+)\]\]--\[\[([^]]+)\]\]=([^=]+)={{([^{}]+)}}(=AI)?'

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

# input_str1 = "[[a]]--[[b]]=朋友={{连接关系|a不知道和b有啥关系，但是就是有关系}}=AI"
# input_str2 = "[[a]]--[[b]]=朋友={{连接关系|a不知道和b有啥关系，但是就是有关系}}"
# result1 = parse(input_str1)
# result2 = parse(input_str2)
# print(result1)
# print(result2)


# 创建实体节点的方法
def create_entity(name, other_name, label, ency_content, map_content):
    """
        name: 名称
        orther_name: 别名
        label: 标签名
        ency_content: 实体描述或内容
        map_content: 图信息（如果适用）
        relationship_properties: 关系属性
    """
    # 创建实体节点
    entity_node = Node(label, NAME=name, OTHER_NAME=other_name, LABEL=label, ENCY_CONTENT=ency_content, MAP_CONTENT=map_content)

    try:
        # 保存节点到数据库
        graph.create(entity_node)
        return True
    except ClientError:
        # 创建失败，返回False
        return False



# 创建实体关系的方法
def create_relationship(start_node_name, end_node_name, relationship_name, relationship_properties):
    """
        relationship_name: 关系名
        relationship_properties: 关系属性
    """
    start_node = graph.nodes.match(NAME=start_node_name).first()
    end_node = graph.nodes.match(NAME=end_node_name).first()

    if start_node is not None and end_node is not None:
        # Create the relationship with properties
        relationship = Relationship(start_node, relationship_name, end_node, **relationship_properties)

        try:
            graph.create(relationship)
            return True
        except ClientError:
            return False
    else:
        return False


# 实体间直接关系查询
def search_direct_relationship(start_node_name, end_node_name):
    try:
        query ="""
            MATCH (startNode {name: $start_name}) -[r]- (endNode {name: $end_name})
            RETURN r;
         """
        result = graph.run(query, start_name=start_node_name, end_name=end_node_name)
        return result.data()
    except ClientError:
        return None



# 实体间最短关系路径查询
def search_indirect_relationship(start_node_name, end_node_name):
    try:
        query ="""
            MATCH (startNode {name: $start_name}), (endNode {name: $end_name})
            MATCH path = shortestPath((startNode)-[*]-(endNode))
            RETURN path;
         """
        result = graph.run(query, start_name=start_node_name, end_name=end_node_name)
        return result.data()
    except ClientError:
        return None


# 函数的使用实例
# person_name = "Hanser"
# other_name = ["憨色儿"]
# label = "现实人物"
# ency_content = "..."
# map_content = "..."

# result = create_entity(person_name, other_name, label, ency_content, map_content)
# print(result)


# character_name = "Bronya"
# other_name = ["板鸭"]
# label = "动画人物"
# ency_content = "..."
# map_content = "..."

# result = create_entity(character_name, other_name, label, ency_content, map_content)
# print(result)

# person_name = "Hanser"
# character_name = "Bronya"
# relationship_type = "DUB_FOR"
# relationship_properties = {
#     "SINCE": "2014"
# }

# result = create_relationship(person_name, character_name, relationship_type, relationship_properties)
# print(result)

# query = "MATCH (p:现实人物)-[:ACT_AS]->(c:动画人物) WHERE p.NAME = 'Hanser' RETURN p, c"
# result = run_query(query)
# print(result)


# # 打开工作簿
# workbook = openpyxl.load_workbook("agriculture_knowledgegraph_django_model\\resources\\filename.xlsx")

# # 选择活动工作表
# worksheet = workbook.active

# # 读取某一列的数据
# column_data = []
# for col in worksheet['A:A']:
#     column_data.append(col.value)

# for node in column_data:
#     # 循环调用函数
#     name = node
#     create_entity(name,[""],"待定","","")