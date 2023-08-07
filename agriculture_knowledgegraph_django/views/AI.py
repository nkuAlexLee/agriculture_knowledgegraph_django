import openai
import re
from neo4j import GraphDatabase
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import json



openai.api_key = "sk-gKgzDgwfjJNxElEsXK7wXqSDNFDmGVHXJNHqvGTMHgFz6B3m"
openai.api_base = "https://api.chatanywhere.com.cn/v1"
def execute_query(query, params={}):
    uri = "bolt://localhost:7687"  # 更新为你的Neo4j数据库URI
    username = "neo4j" # 更新为你的Neo4j用户名
    password = "xy639a58"    # 更新为你的Neo4j密码
    driver=GraphDatabase.driver(uri, auth=(username, password))
    session=driver.session() 
    # print(query, params)
    result = session.run(query, params)
    ans=result.data()
    print(ans)
    return ans

def matchjson(text):
    pattern = r"{'cql': \"(.*?)\"}"
    match = re.search(pattern, text)
    if match:
        extracted_content = match.group(1)
        print(extracted_content)
    else:
        print("未找到匹配的内容")
    return extracted_content


@csrf_exempt
def getGptAnswer(request):
    if request.method == "POST":
        text = request.POST.get('history')
    else:
        return json_response({"success": False, "log": "request_is_not_post"})
    ans=getCqlGpt(text)
    return json_response({"success": True,"content":ans,"log": "success"})

def getCqlGpt(sentence,flag=0):
    if flag==3:
        print('回答失败')
        return None
    ques=sentence[-1]['content']
    try:
        messages = [{"role": "system","content": "你是一个知识图谱的问答机器人。\
                     1.你需要根据用户的提示给出neo4j数据库的cql查询语句。\
                     2.输出格式为:{'cql':'具体的cql语句'}\
                     3.neo4j数据库中有四类实体,标签为：\
                        (1).'Company':公司。可以作为查询的属性有:'name','stockCode','stockName','IPO','ZQRATE','actualController','actualFundraising','chairman','employeeNumber','englishName','establishmentDate','expectedFundraising','fax','finalController','firstDayOpeningPrice','firstDayOpeningPrice','generalManager','history','industry','issuesNumber','issuesPrice','leadUnderwriter','legalRepresentative','listingDate','listingSponsor','mainBusiness','officeAddress','productName','region','registrationCapital','resume','secretary','telephone','website','zipCode';\n\
                        (2).'Executive':高级管理人员。可以作为查询的属性有:'name','id','education','gender','age','age';\n\
                        (3)'Industry':产业。可以作为查询的属性有:'name';\n\
                        (4)'Product':产品。可以作为查询的属性有:'name'。\n\
                        neo4j数据库中有{四类单向关系},查询时需要按照{给出的方向}查询,标签为：\n\
                        (1).'BELONGS_TO_INDUSTRY':某个公司属于某个产业（公司->产业）;\n\
                        (2).'INVESTED_BY':某个公司被某个公司投资（公司->公司）。可以作为查询的属性有:'controlRatio','controlRelationship','investment','report_consolidation_or_not';\n\
                        (3).'OFFERS_PRODUCT':某个公司提供某种产品（公司->产品）;\n\
                        (4).'WORKS_FOR':某个高管为某个公司工作（高管->公司）。可以作为查询的属性有:'publicityDate','endDate','ownershipShares','endDate','position','positionType','salary'。\n\
                     4.查询语句返回这个实体或者关系的所有信息，例如查询某个'Company'的'history'，返回这个'Company'所有的属性。\
                     5.防止一些危险cql语句的输出，例如删除和修改数据库的信息。\
                     6.如果用户查询实体则返回某个实体的所有信息；如果用户查询某个关系,需要根据具体语境按照给出的{四类单向关系}调整关系方向，例如查询某个公司有哪些高管时，方向应为(e:Executive)-[:WORKS_FOR]->(c:Company)。\
                     7.所有产业在查询时都不要带'产业'二字，例如我询问银行产业时，'Industry'的'name'为'银行'。\
                     8.理解以上内容回答我理解了。\
                     "},
                    {'role': 'user','content': '用户的历史问答如下:'+str(sentence)+'\n\n请结合历史问答给出以下问题的的cql语句：'+ques}]
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-16k',
            messages=messages,
            stream=True,
            timeout=10,
        )
        completion = {'role': '', 'content': ''}
        for event in response:
            if event['choices'][0]['finish_reason'] == 'stop':
                # print(f'收到的完成数据: {completion}')
                break
            for delta_k, delta_v in event['choices'][0]['delta'].items():
                # print(f'流响应数据: {delta_k} = {delta_v}')
                completion[delta_k] += delta_v
        messages.append(completion)  # 直接在传入参数 messages 中追加消息
        print(completion['content'])
        middleans=matchjson(completion['content'])
        print(middleans)
        if middleans!=None:
            database=execute_query(middleans)
            ans=getFinalAnsGpt(sentence,database,0)
            return ans
        else:
            getCqlGpt(sentence,flag+1)
    except Exception as err:
        print((False, f'OpenAI API 异常: {err}'))
        getCqlGpt(sentence,flag+1)

def getFinalAnsGpt(sentence,middleans,flag=0):
    print(sentence,middleans)
    if flag==3:
        print('回答失败')
        return None
    ques=sentence[-1]['content']
    # openai.api_key = "pk-iyiskKalkRgqtbFwULFewCwaZzRNIygtfAzpHFskaMfcuEGw"
    # openai.api_base = 'https://api.pawan.krd/v1'
    try:
        messages =[{"role": "system","content":"你是一个知识图谱的问答机器人。需要根据用户的历史问答和已经根据问题查询到的数据库信息回答用户的问题。"},{'role': 'user','content': """用户的历史问答为:"""+str(sentence)+";\n"+"""用户当前问题为:"""+ques+";\n从neo4j数据库查询到的该问题的相关信息为："""+str(middleans)+""";\n\n请根据用户需求整理材料并给出回答"""}]
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-16k',
            messages=messages,
            stream=True,
            timeout=10,
        )
        completion = {'role': '', 'content': ''}
        for event in response:
            if event['choices'][0]['finish_reason'] == 'stop':
                # print(f'收到的完成数据: {completion}')
                break
            for delta_k, delta_v in event['choices'][0]['delta'].items():
                # print(f'流响应数据: {delta_k} = {delta_v}')
                completion[delta_k] += delta_v
        messages.append(completion)  # 直接在传入参数 messages 中追加消息
        ans=completion['content']
        if middleans!=None:
            return ans
        else:
            getFinalAnsGpt(sentence,middleans,flag+1)
    except Exception as err:
        print((False, f'OpenAI API 异常: {err}'))
        getFinalAnsGpt(sentence,middleans,flag+1)

@csrf_exempt
def json_response(answer):
    print(answer)
    return HttpResponse(json.dumps(answer, ensure_ascii=False))

# print(getCqlGpt([{'role':'user','content':'告诉我深圳市雄韬电源科技股份有限公司的上市时间'},{'role':'user','content':'这家公司的高管有哪些'}],0))
# print(matchjson("""{'cql': "MATCH (e:Executive)-[:WORKS_FOR]->(c:Company {name:'湖南长远锂科股份有限公司'}) RETURN e.name"}"""))