from py2neo import Graph, Node, Relationship, ClientError
import openpyxl
import re

# 连接到Neo4j数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))


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

# 创建实体节点的方法
def create_node(name, other_name, label, ency_content, map_content):
    """
    创建节点

    参数：
    name: 名称
    other_name: 别名
    label: 标签名
    ency_content: 实体描述或内容
    map_content: 图信息（如果适用）

    返回值：
    成功保存节点到数据库，返回True，否则返回False
    """
    # 创建节点
    node = Node(label, NAME=name, OTHER_NAME=other_name, LABEL=label, ENCY_CONTENT=ency_content, MAP_CONTENT=map_content)

    try:
        # 保存节点到数据库
        graph.create(node)
        return True
    except ClientError as e:
        print(f"Error creating node: {e}")
        return False


# 创建实体关系的方法
def create_relationship(start_node_name, end_node_name, relationship_name, relationship_properties):
    """
    创建节点之间的关系

    参数：
    start_node_name: 起始节点名称
    end_node_name: 终止节点名称
    relationship_name: 关系名
    relationship_properties: 关系属性

    返回值：
    成功保存关系到数据库，返回True，否则返回False
    """
    start_node = graph.nodes.match(NAME=start_node_name).first()
    end_node = graph.nodes.match(NAME=end_node_name).first()

    if start_node is not None and end_node is not None:
        # 创建带有属性的关系
        relationship = Relationship(start_node, relationship_name, end_node, **relationship_properties)

        try:
            graph.create(relationship)
            return True
        except ClientError as e:
            print(f"Error creating relationship: {e}")
            return False
    else:
        return False


# 实体信息直接查询
def search_node(node_name):
    """
    实体信息直接查询

    参数：
    node_name: 节点名称

    返回值：
    查询到的节点数据，如果没有找到则返回None
    """
    try:
        query ="""
            MATCH (node {name: $node_name})
            RETURN node;
         """
        result = graph.run(query, node_name=node_name)
        return result.data()

    except ClientError as e:
        print(f"Error searching node: {e}")
        return None


# 实体直接关系查询
def search_node_relationship(node_name):
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
    

    

# 实体多层嵌套关系查询
def search_node_nested_relationship(node_name, depth):
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
        return [record['related_node_name'] for record in result if record['related_node_name']!=None]
    except ClientError as e:
        print(f"Error searching nested relationship: {e}")
        return None


    
print(search_node_relationship('Laurence Fishburne'))
    

# 实体间直接关系查询
def search_direct_relationship_between(start_node_name, end_node_name):
    """
    实体间直接关系查询

    参数：
    start_node_name: 起始节点名称
    end_node_name: 终止节点名称

    返回值：
    查询到的关系数据，如果没有找到则返回None
    """
    try:
        query ="""
            MATCH (startNode {name: $start_name}) -[r]- (endNode {name: $end_name})
            RETURN r;
         """
        result = graph.run(query, start_name=start_node_name, end_name=end_node_name)
        return result.data()
    except ClientError as e:
        print(f"Error searching direct relationship: {e}")
        return None


# 实体间最短关系路径查询
def search_indirect_relationship_between(start_node_name, end_node_name):
    """
    实体间最短关系路径查询

    参数：
    start_node_name: 起始节点名称
    end_node_name: 终止节点名称

    返回值：
    查询到的关系路径数据，如果没有找到则返回None
    """
    try:
        query ="""
            MATCH (startNode {name: $start_name}), (endNode {name: $end_name})
            MATCH path = shortestPath((startNode)-[*]-(endNode))
            RETURN path;
         """
        result = graph.run(query, start_name=start_node_name, end_name=end_node_name)
        return result.data()
    except ClientError as e:
        print(f"Error searching indirect relationship: {e}")
        return None


# 函数的使用实例
# person_name = "Hanser"
# other_name = ["憨色儿"]
# label = "现实人物"
# ency_content = "..."
# map_content = "..."

# result = create_node(person_name, other_name, label, ency_content, map_content)
# print(result)


# character_name = "Bronya"
# other_name = ["板鸭"]
# label = "动画人物"
# ency_content = "..."
# map_content = "..."

# result = create_node(character_name, other_name, label, ency_content, map_content)
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
#     create_node(name, [""], "待定", "", "")
