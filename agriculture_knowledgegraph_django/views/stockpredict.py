import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
import re
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

ts.set_token('48acead4b9eb1e067bef2397bfc9308914469d05bdeb249924861800')
pro = ts.pro_api()


def format_stock(stock_code):
    pattern = r'\b\d{6}\b'
    try:
        stock_code = re.search(pattern, stock_code).group()
    except Exception:
        return None
    if re.match(r'^300\d{3}$', stock_code):
        return f"{stock_code}.SZ"
    elif re.match(r'^(600|601|603)\d{3}$', stock_code):
        return f"{stock_code}.SH"
    elif re.match(r'^900\d{3}$', stock_code):
        return f"{stock_code}.SH"
    elif re.match(r'^000\d{3}$', stock_code):
        return f"{stock_code}.SZ"
    elif re.match(r'^002\d{3}$', stock_code):
        return f"{stock_code}.SZ"
    elif re.match(r'^200\d{3}$', stock_code):
        return f"{stock_code}.SZ"
    elif re.match(r'^730\d{3}$', stock_code):
        return f"{stock_code}.SH"
    elif re.match(r'^700\d{3}$', stock_code):
        return f"{stock_code}.SH"
    elif re.match(r'^080\d{3}$', stock_code):
        return f"{stock_code}.SZ"
    elif re.match(r'^580\d{3}$', stock_code):
        return f"{stock_code}.SH"
    elif re.match(r'^031\d{3}$', stock_code):
        return f"{stock_code}.SZ"
    elif re.match(r'^400\d{3}$', stock_code):
        return f"{stock_code}.SB"
    elif re.match(r'^\d{6}$', stock_code):
        return f"{stock_code}.SZ"  # 默认将其他六位数字认为是深市股票
    else:
        return None


@csrf_exempt
def stockpredict(request):
    if request.method == 'POST':
        stock_code = request.POST.get('stock_code')
    else:
        return json_response({'success': False})
    ts_code = format_stock(stock_code)
    print(ts_code)
    data = pro.daily(ts_code=ts_code, start_date='20150301')
    data.to_csv(
        'agriculture_knowledgegraph_django\stockcsv\data.csv', index=False)
    data = pd.read_csv(
        'agriculture_knowledgegraph_django\stockcsv\data.csv', index_col=0, parse_dates=[0])

    # 将 trade_date 转换为日期格式
    data['trade_date'] = pd.to_datetime(data['trade_date'], format='%Y%m%d')

    # 将 trade_date 设置为索引
    data.set_index('trade_date', inplace=True)

    stock_day = data['close'].resample('D').mean()
    # 对数据进行重采样，以每周为单位计算 close 的均值
    # stock_week = data['close'].resample('W').mean()
    # stock_week
    stock_train = stock_day['2015':'2020'].dropna()
    stock_train.plot(figsize=(12, 8))
    model = ARIMA(stock_train, order=(2, 0, 2))
    result = model.fit()
    result.summary()
    pred = result.predict(1500, 2000, dynamic=True)
    pred_array = pred.values.tolist()  # 转换为Python列表
    return json_response({'success': True, 'data': pred_array})


@csrf_exempt
def json_response(answer):
    print(answer)
    return HttpResponse(json.dumps(answer, ensure_ascii=False))
