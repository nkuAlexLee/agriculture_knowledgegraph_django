class XMLConnector{
    /* 
        url: API 的 url
            必填
        method: 调用方法 "GET" 或者 "POST"
            必填
        msg:传入的数据 建议key值应该为字符串 格式为 [[key0, value0], [key1, value1]]
            如GET方法想传递信息 ../url?name=lihua&sex=0 则msg为: [["name", "lihua"], ["sex", 0]]
            不需要填null
        func_callback:获取数据之后的回调函数 回调函数格式应该为 func_callback(result_msg) 会返回获取到的信息
            result_msg 类型为回调信息的类型
            不需要填null
        func_wating:发送请求、接收到结果、超时，都会调用此函数 一次发送请求中 超时和接收到结果只会调用一次
            func_wating函数格式应该为 func_wating(is_wating) is_wating 类型为bool
            发送请求会调用func_wating(true) 接收到结果、超时会调用func_wating(false)
            不需要填null
        func_timeout:超时会调用此函数 调用方式为:func_timeout() 没有入参
            不需要填null
        可用方法:
            send()  发出请求
            setTimeOut(time_out)  设置超时时间 单位为ms 默认为500ms
    */
    time_out = 5000;  // ms
    is_wating = false;
    timer = null;
    constructor(url, method, msg, func_callback, func_wating, func_timeout){
        this.url = url;
        this.method = method;
        this.msg = msg;  // [[key0, value0], [key1, value1]]
        this.func_callback = func_callback;
        this.func_wating = func_wating;
        this.func_timeout = func_timeout;
        this.xml_http = new XMLHttpRequest();
    }
    setTimeOut(time_out){
        this.time_out = time_out;
    }
    send(){
        console.log(this.msgToStr());
        let this_ = this;
        this.xml_http.onreadystatechange=(function(this_){
            return function(){
                if(this_.xml_http.readyState==4 && this_.xml_http.status==200){
                    if(!this_.is_wating) return;  // 已经超时
                    this_.is_wating = false;
                    if(this_.func_callback!=null&&this_.func_callback!=undefined){
                        this_.func_callback(this_.xml_http.responseText);
                    }
                    if(this_.func_wating!=null&&this_.func_wating!=undefined){
                        this_.func_wating(false);  // 传入false 代表结束
                    }
                }
            }
        })(this_);
        if(this.method=="POST"){
            this.xml_http.open("POST",this.url,true);
            this.xml_http.setRequestHeader("Content-type","application/x-www-form-urlencoded;charset=utf-8");
            if(this.msg!=null&&this.msg!=undefined) this.xml_http.send(this.msgToStr());
            else this.xml_http.send();
        }else if(this.method=="GET"){
            if(this.msg!=null&&this.msg!=undefined) this.xml_http.open("GET",this.url + "?" + this.msgToStr(),true);
            else this.xml_http.open("GET",this.url,true);
            this.xml_http.send();
        }
        this.is_wating = true;
        if(this_.func_wating!=null&&this_.func_wating!=undefined){
            this_.func_wating(true);  // 传入true 代表开始
        }
        this.setTimer();  // 设置超时计时器
    }
    msgToStr(){
        let str = "";
        for(let i=0;i<this.msg.length;i++){
            if(i!=0) str += "&";
            str += this.msg[i][0].toString() + "=" + this.msg[i][1].toString();
        }
        return str;
    }
    setTimer(){
        console.log("设置计时器");
        let this_ = this;
        this.timer = setTimeout((function(this_){
            return function(){
                if(!this_.is_wating) return;
                else{
                    this_.is_wating = false;
                    if(this_.func_timeout!=null&&this_.func_timeout!=undefined){
                        this_.func_timeout();  // 超时
                    }
                    if(this_.func_wating!=null&&this_.func_wating!=undefined){
                        this_.func_wating(false);  // 传入false 代表结束
                    }
                }
            }
        })(this_), this.time_out);
    }
}

/* 
以下为示例
1. 需要访问http://127.0.0.1:5500/log/log接口 传递参数为name=lihua,sex=0,class=1 POST 回调函数等都存在
    let url = "http://127.0.0.1:5500/log/log";
    let msg = [["name", "lihua"], ["sex", 0], ["class", 1]];
    let XML_connector = new XMLConnector(url, "POST", msg, func0, func1, func2);
    // XML_connector.setTimeout(1000);  // 把默认的500ms超时改成1000ms
    XML_connector.send();  // 发送请求
    //  之后如果没用超时 则会调用回调函数 把获得的数据传入
    // 超时则会调用超时的函数
    // 发出请求之后 等待函数会被调用 会传入true (ture 是值)
    // 超时或者数据获得之后 等待函数会被调用 会传入false (false 是值)
    -->此时函数运行等价于
        this.xml_http.open("POST","http://127.0.0.1:5500/log/log",true);
        this.xml_http.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        this.xml_http.send("name=lihua&sex=0&class=1");
    <--
*/