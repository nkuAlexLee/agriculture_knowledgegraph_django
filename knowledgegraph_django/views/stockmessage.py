import baostock as bs
import pandas as pd
import datetime
import re
import copy
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
lg = bs.logout()
lg = bs.login()
@csrf_exempt
def getStockAnswer(request):
    if request.method == "POST":
        stock= str(request.POST.get('stock'))
        model=str(request.POST.get('model'))
        if model=='d':
            days= int(request.POST.get('days'))
            ans,message=getStockDayInformation(stock,days)
        elif model=='m':
            minute= int(request.POST.get('minute'))
            ans,message=getStockMinuteInformation(stock,minute)
        elif model=='w':
            days= int(request.POST.get('days'))
            ans,message=getStockWeekInformation(stock,days)
        elif model=='M':
            days= int(request.POST.get('days'))
            ans,message=getStockMonthInformation(stock,days)
        else:
            return json_response({"success": False, "log": "wrong_model"})
    else:
        return json_response({"success": False, "log": "request_is_not_post"})
    if ans==None:
        return json_response({"success": False,"log": "search_error"})
    return json_response({"success": True,"content":{"list":ans,"message":message},"log": "success"})

@csrf_exempt
def getStocklistAnswer(request):
    if request.method == "POST":
        model=str(request.POST.get('model'))
        ans=getStockList(model)
        if ans==None:
            return json_response({"success": False,"log": "search_error"})
        return json_response({"success": True,"content":ans,"log": "success"})
    else:
        return json_response({"success": False, "log": "request_is_not_post"})

def convert_to_formatted_datetime(input_string):
    try:
        # 解析输入字符串为datetime对象
        input_datetime = datetime.datetime.strptime(input_string, "%Y%m%d%H%M%S%f")

        # 格式化为目标字符串格式
        output_string = input_datetime.strftime("%H:%M")
        return output_string
    except ValueError:
        return None

def format_stock_code(stock_code):
    pattern = r'\b\d{6}\b'
    try:
        stock_code= re.search(pattern, stock_code).group()
    except Exception:
        return None
    if re.match(r'^300\d{3}$', stock_code):
        return f"sz.{stock_code}"
    elif re.match(r'^(600|601|603)\d{3}$', stock_code):
        return f"sh.{stock_code}"
    elif re.match(r'^900\d{3}$', stock_code):
        return f"sh.{stock_code}"
    elif re.match(r'^000\d{3}$', stock_code):
        return f"sz.{stock_code}"
    elif re.match(r'^002\d{3}$', stock_code):
        return f"sz.{stock_code}"
    elif re.match(r'^200\d{3}$', stock_code):
        return f"sz.{stock_code}"
    elif re.match(r'^730\d{3}$', stock_code):
        return f"sh.{stock_code}"
    elif re.match(r'^700\d{3}$', stock_code):
        return f"sh.{stock_code}"
    elif re.match(r'^080\d{3}$', stock_code):
        return f"sz.{stock_code}"
    elif re.match(r'^580\d{3}$', stock_code):
        return f"sh.{stock_code}"
    elif re.match(r'^031\d{3}$', stock_code):
        return f"sz.{stock_code}"
    elif re.match(r'^400\d{3}$', stock_code):
        return f"sb.{stock_code}"
    elif re.match(r'^\d{6}$', stock_code):
        return f"sh.{stock_code}"  # 默认将其他六位数字认为是深市股票
    else:
        return None

def getStockMinuteInformation(stock,minute):
    # 获取当前时间
    try:
        
        stockmid= format_stock_code(stock)
        print(stockmid)
        message={}
        if stockmid==None:
            message["stockname"]=copy.deepcopy(stock)
            rs = bs.query_stock_basic(code_name=stock)
            stock=rs.get_row_data()[0]
            message["stockid"]=copy.deepcopy(stock)
            print(message)
        else:
            message["stockid"]=copy.deepcopy(stockmid)
            rs = bs.query_stock_basic(code=stockmid)
            stock=rs.get_row_data()[1]
            message["stockname"]=copy.deepcopy(stock)
            print(message)

        current_date = datetime.date.today()
        # 将时间格式化为所需的字符串格式
        formatted_time = current_date.strftime("%Y-%m-%d")
        # 计算30天前的日期
        days_before = datetime.timedelta(days=1)
        new_date = current_date - days_before
        # 将日期格式化为所需的字符串格式
        formatted_before_date = new_date.strftime("%Y-%m-%d")
        # print(formatted_before_date,formatted_time)
        rs = bs.query_history_k_data_plus(str(message['stockid']),
            "date,time,code,open,high,low,close,volume,amount,adjustflag",
            start_date=formatted_before_date, end_date=formatted_time,
            frequency=str(minute), adjustflag="3")
        # print('query_history_k_data_plus respond error_code:'+rs.error_code)
        # print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        ans=[]
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        # result = pd.DataFrame(data_list, columns=rs.fields)
        # print(result)
        for i in range(len(data_list)):
            ans.append([convert_to_formatted_datetime(data_list[i][1]),data_list[i][6],str(float(data_list[i][8])/float(data_list[i][7]))])
        #### 结果集输出到csv文件 ####   
        # result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
        # print(ans)
        #### 登出系统 ####
        
        print(ans)
        return ans,message
    except Exception as e:
        print(e)
        return None,None

def getStockDayInformation(stock,days):
    # 获取当前时间
    try:
        
        stockmid= format_stock_code(stock)
        print(stockmid)
        message={}
        if stockmid==None:
            message["stockname"]=copy.deepcopy(stock)
            rs = bs.query_stock_basic(code_name=stock)
            stock=rs.get_row_data()[0]
            message["stockid"]=copy.deepcopy(stock)
            print(message)
        else:
            message["stockid"]=copy.deepcopy(stockmid)
            rs = bs.query_stock_basic(code=stockmid)
            stock=rs.get_row_data()[1]
            message["stockname"]=copy.deepcopy(stock)
            print(message)

        current_date = datetime.date.today()
        # 将时间格式化为所需的字符串格式
        formatted_time = current_date.strftime("%Y-%m-%d")
        # 计算30天前的日期
        days_before = datetime.timedelta(days=days)
        new_date = current_date - days_before
        # 将日期格式化为所需的字符串格式
        formatted_before_date = new_date.strftime("%Y-%m-%d")
        # print(formatted_before_date,formatted_time)

        #### 登陆系统 ####
        # 显示登陆返回信息
        # print('login respond error_code:'+lg.error_code)
        # print('login respond  error_msg:'+lg.error_msg)

        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg

        rs = bs.query_history_k_data_plus(str(message['stockid']),
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            start_date=formatted_before_date, end_date=formatted_time,
            frequency="d", adjustflag="3")
        # print('query_history_k_data_plus respond error_code:'+rs.error_code)
        # print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        ans=[]
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        # result = pd.DataFrame(data_list, columns=rs.fields)
        for i in range(len(data_list)):
            ans.append([data_list[i][0],data_list[i][2],data_list[i][5],data_list[i][4],data_list[i][3]])
        #### 结果集输出到csv文件 ####   
        # result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
        # print(ans)
        #### 登出系统 ####
        
        return ans,message
    except Exception:
        return None,None

def getStockWeekInformation(stock,days):
    # 获取当前时间
    try:
        
        stockmid= format_stock_code(stock)
        print(stockmid)
        message={}
        if stockmid==None:
            message["stockname"]=copy.deepcopy(stock)
            
            rs = bs.query_stock_basic(code_name=stock)
            stock=rs.get_row_data()[0]
            message["stockid"]=copy.deepcopy(stock)
            print(message)
        else:
            message["stockid"]=copy.deepcopy(stockmid)
            
            rs = bs.query_stock_basic(code=stockmid)
            stock=rs.get_row_data()[1]
            message["stockname"]=copy.deepcopy(stock)
            print(message)

        current_date = datetime.date.today()
        # 将时间格式化为所需的字符串格式
        formatted_time = current_date.strftime("%Y-%m-%d")
        # 计算30天前的日期
        days_before = datetime.timedelta(days=days)
        new_date = current_date - days_before
        # 将日期格式化为所需的字符串格式
        formatted_before_date = new_date.strftime("%Y-%m-%d")
        # print(formatted_before_date,formatted_time)

        #### 登陆系统 ####
        # 显示登陆返回信息
        # print('login respond error_code:'+lg.error_code)
        # print('login respond  error_msg:'+lg.error_msg)

        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg

        rs = bs.query_history_k_data_plus(str(message['stockid']),
            "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
            start_date=formatted_before_date, end_date=formatted_time,
            frequency="w", adjustflag="3")
        # print('query_history_k_data_plus respond error_code:'+rs.error_code)
        # print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        ans=[]
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        # result = pd.DataFrame(data_list, columns=rs.fields)
        for i in range(len(data_list)):
            ans.append([data_list[i][0],data_list[i][2],data_list[i][5],data_list[i][4],data_list[i][3]])
        #### 结果集输出到csv文件 ####   
        # result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
        # print(ans)
        #### 登出系统 ####
        
        return ans,message
    except Exception:
        return None,None
    
def getStockMonthInformation(stock,days):
    # 获取当前时间
    try:
        
        stockmid= format_stock_code(stock)
        print(stockmid)
        message={}
        if stockmid==None:
            message["stockname"]=copy.deepcopy(stock)
            
            rs = bs.query_stock_basic(code_name=stock)
            stock=rs.get_row_data()[0]
            message["stockid"]=copy.deepcopy(stock)
            print(message)
        else:
            message["stockid"]=copy.deepcopy(stockmid)
            
            rs = bs.query_stock_basic(code=stockmid)
            stock=rs.get_row_data()[1]
            message["stockname"]=copy.deepcopy(stock)
            print(message)

        current_date = datetime.date.today()
        # 将时间格式化为所需的字符串格式
        formatted_time = current_date.strftime("%Y-%m-%d")
        # 计算30天前的日期
        days_before = datetime.timedelta(days=days)
        new_date = current_date - days_before
        # 将日期格式化为所需的字符串格式
        formatted_before_date = new_date.strftime("%Y-%m-%d")
        # print(formatted_before_date,formatted_time)

        #### 登陆系统 ####
        # 显示登陆返回信息
        # print('login respond error_code:'+lg.error_code)
        # print('login respond  error_msg:'+lg.error_msg)

        #### 获取沪深A股历史K线数据 ####
        # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
        # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
        # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg

        rs = bs.query_history_k_data_plus(str(message['stockid']),
            "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg",
            start_date=formatted_before_date, end_date=formatted_time,
            frequency="m", adjustflag="3")
        # print('query_history_k_data_plus respond error_code:'+rs.error_code)
        # print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

        #### 打印结果集 ####
        data_list = []
        ans=[]
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            data_list.append(rs.get_row_data())
        # result = pd.DataFrame(data_list, columns=rs.fields)
        for i in range(len(data_list)):
            ans.append([data_list[i][0],data_list[i][2],data_list[i][5],data_list[i][4],data_list[i][3]])
        #### 结果集输出到csv文件 ####   
        # result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
        # print(ans)
        #### 登出系统 ####
        
        return ans,message
    except Exception:
        return None,None

def getStockList(model):
    try:
        
        # current_date = datetime.date.today()
        # # 将时间格式化为所需的字符串格式
        # formatted_time = current_date.strftime("%Y-%m-%d")
        # # 计算30天前的日期
        # days_before = datetime.timedelta(days=1)
        # new_date = current_date - days_before
        # # 将日期格式化为所需的字符串格式
        # formatted_before_date = new_date.strftime("%Y-%m-%d")
        ans={}
        if model=="sz50":
            ansdict={
                "result":getQuery(0),
            }
        elif model=="hs300":
            ansdict={
                "result":getQuery(1),
            }
        elif model=="zz500":
            ansdict={
                "result":getQuery(2),
            }
        
        return ansdict
    except Exception as e:
        print(e)
        return None

def getQuery(model):
    # 获取上证50成分股
    if model==0:
        rs = bs.query_sz50_stocks()
    elif model==1:
        rs = bs.query_hs300_stocks()
    elif model==2:
        rs = bs.query_zz500_stocks()
    # 打印结果集
    sz50_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        sz50_stocks.append(rs.get_row_data())
    print(sz50_stocks)
    codelist=[]
    for i in sz50_stocks:
        codelist.append(i[1])
    print(codelist)
    codeStr=getCodeStr(codelist)
    ansdict=parse_stock_data(codeStr)
    print(ansdict)
    # 登出系统
    return ansdict

def getCodeStr(codelist):
    # codelist=['sh.600519','sh.601000','sh.601003']
    url = 'http://qt.gtimg.cn/q=';
    num=len(codelist)
    for i in range(num):
        mid='s_'+codelist[i].replace('.','')
        url = url+mid;
        if i!=num-1:
            url=url+','
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        return data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None
    
def parse_stock_data(data_string):
    pattern = r'v_s_sh\d+="(\d)~([^~]+)~(\d+)~([\d.]+)~([-\d.]+)~([-\d.]+)~(\d+)~(\d+)~~([\d.]+)~([^"]+)"'
    matches = re.findall(pattern, data_string)
    result = []
    for match in matches:
        index, name, code, price, change, percent, volume, turnover, _, _, = match
        color=''
        if float(change)>0:
            color='red'
        elif float(change)<0:
            color='green'
        else:
            color='black'
        entry = {
            # "序号": index,
            # "交易所": int(index),
            "名称": str(name),
            "代码": str(code),
            "现价": [str(price),color],
            # "涨跌": float(change),
            "涨跌幅": [str(percent),color],
            "成交量": str(volume),
            "成交金额": str(turnover),
        }
        result.append(entry)

    return result

@csrf_exempt
def json_response(answer):
    print(answer)
    return HttpResponse(json.dumps(answer, ensure_ascii=False))