import baostock as bs
import pandas as pd
import datetime
import re
import copy
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def getStockAnswer(request):
    if request.method == "POST":
        stock= str(request.POST.get('stock'))
        days= int(request.POST.get('days'))
    else:
        return json_response({"success": False, "log": "request_is_not_post"})
    ans,message=getStockInformation(stock,days)
    if ans==None or ans==[]:
        return json_response({"success": False,"log": "search_error"})
    return json_response({"success": True,"content":{"list":ans,"message":message},"log": "success"})

def format_stock_code(stock_code):
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
        return f"sz.{stock_code}"  # 默认将其他六位数字认为是深市股票
    else:
        return None

def getStockInformation(stock,days):
    # 获取当前时间
    try:
        lg = bs.login()
        stockmid= format_stock_code(stock)
        print(stockmid)
        message={}
        if stockmid==None:
            message["stockname"]=copy.deepcopy(stock)
            rs = bs.query_stock_industry()
            rs = bs.query_stock_basic(code_name=stock)
            stock=rs.get_row_data()[0]
            message["stockid"]=copy.deepcopy(stock)
            print(message)
        else:
            message["stockid"]=copy.deepcopy(stockmid)
            rs = bs.query_stock_industry()
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
        bs.logout()
        return ans,message
    except Exception:
        return None,None


@csrf_exempt
def json_response(answer):
    print(answer)
    return HttpResponse(json.dumps(answer, ensure_ascii=False))