from py2neo import Graph, Node, Relationship, ClientError

# 连接到Neo4j数据库
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))



# 创建实体节点的方法
def create_entity(name, other_name, label, ency_content, map_content):
    # 创建实体节点
    entity_node = Node(label, NAME=name, OTHER_NAME=other_name, LABEL=label, ENCY_CONTENT=ency_content, MAP_CONTENT=map_content)

    try:
        # 保存节点到数据库
        graph.create(entity_node)
        return True
    except ClientError:
        # 创建失败，返回False
        return False



# 创建实体关系（不带属性）的方法
def create_relationship(start_node_name, end_node_name, relationship_type):
    start_node = graph.nodes.match(NAME=start_node_name).first()
    end_node = graph.nodes.match(NAME=end_node_name).first()

    if start_node is not None and end_node is not None:
        relationship = Relationship(start_node, relationship_type, end_node)

        try:
            graph.create(relationship)
            return True
        except ClientError:
            return False
    else:
        return False



# 创建实体关系（带属性）的方法
def create_relationship_with_properties(start_node_name, end_node_name, relationship_type, relationship_properties):
    start_node = graph.nodes.match(NAME=start_node_name).first()
    end_node = graph.nodes.match(NAME=end_node_name).first()

    if start_node is not None and end_node is not None:
        # Create the relationship with properties
        relationship = Relationship(start_node, relationship_type, end_node, **relationship_properties)

        try:
            graph.create(relationship)
            return True
        except ClientError:
            return False
    else:
        return False


# 用于直接查询和多层嵌套查询（直接写Cypher语句）
def run_query(query):
    try:
        result = graph.run(query)
        return result.data()
    except ClientError:
        return None


# 函数的使用实例
person_name = "Hanser"
other_name = ["憨色儿"]
label = "现实人物"
ency_content = "..."
map_content = "..."

result = create_entity(person_name, other_name, label, ency_content, map_content)
print(result)


character_name = "Bronya"
other_name = ["板鸭"]
label = "动画人物"
ency_content = "..."
map_content = "..."

result = create_entity(character_name, other_name, label, ency_content, map_content)
print(result)

person_name = "Hanser"
character_name = "Bronya"
relationship_type = "ACT_AS"

result = create_relationship(person_name, character_name, relationship_type)
print(result)

person_name = "Hanser"
character_name = "Bronya"
relationship_type = "DUB_FOR"
relationship_properties = {
    "SINCE": "2014"
}

result = create_relationship_with_properties(person_name, character_name, relationship_type, relationship_properties)
print(result)

query = "MATCH (p:现实人物)-[:ACT_AS]->(c:动画人物) WHERE p.NAME = 'Hanser' RETURN p, c"
result = run_query(query)
print(result)