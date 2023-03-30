from . import app
from .forms import AccountForm,DiffForm
from .models import Account
from flask import render_template,redirect,url_for,session,flash
import json
from typing import Dict,Union
from requests import Response,request
import threading
import requests
import re

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/account',methods=['GET','POST'])
def account():
    form = AccountForm()
    if form.validate_on_submit():
        account = Account(phone_num=form.phone_num.data,phone_code=form.phone_code.data,session_id=form.session_id.data)
        if account.session_id is None:
            account.set_session_id()  # 改为异步的方式来获取session_id
        account.save()
        return redirect(url_for('account'))
        
    return render_template('account.html',form=form)


@app.route('/account/edit/<int:id>')
def account_edit(id):
    pass

@app.route('/account/delete/<int:id>')
def account_delete(id):
    pass

@app.route('/diff',methods=['GET','POST'])
def diff():
    form = DiffForm()
    
    if form.validate_on_submit():
        text_from = form.text_from.data
        text = form.text.data
        base_env = form.base_env.data
        test_env = form.test_env.data
        
        session["text"] = text
        session["test_from"] = text_from
        session["base_env"] = base_env
        session["test_env"] = test_env
        method = ""
        if text_from == "1":
            regex = re.compile("'request': '(.*?)',")
            request_text = regex.findall(text)[0]
            app.logger.debug("Request:{}".format(request_text))
            dict_data = json.loads(request_text.strip())
            method = dict_data.get("Method")
        elif text_from == "2":
            dict_data = json.loads(text)
            method = dict_data.get("method")
        if method.upper()!= "GET":
            flash("暂不支持非GET请求的Diff")
            return redirect(url_for("diff"))
        result = async_fetch_all_url(text_from=text_from,request_data=dict_data,base_env=base_env,test_env=test_env)
        if result.get(base_env).status_code != 200:
            app.logger.warning("api request error:\nstatus_code:{},response_body:{}".format(result.get(base_env).status_code,result.get(base_env).json()))
        if result.get(test_env).status_code != 200:
            app.logger.warning("api request error:\nstatus_code:{},response_body:{}".format(result.get(base_env).status_code,result.get(base_env).json()))

        app.logger.debug("base_env:{},headers:{}".format(result.get(base_env).text,result.get(base_env).headers))
        app.logger.debug("test_env:{},headers:{}".format(result.get(test_env).text,result.get(test_env).headers))
        original_json = json.dumps(result.get(base_env).json(),ensure_ascii=False,indent=4,sort_keys=True)
        modified_json = json.dumps(result.get(test_env).json(),ensure_ascii=False,indent=4,sort_keys=True)
        
        return render_template('diff.html',form=form,original_json=original_json,modified_json=modified_json)
    original_json = session.get("original_json",None)
    modified_json = session.get("modified_json",None)
    text = session.get("text",None)
    text_from = session.get("test_from",None)
    base_env = session.get("base_env",None)
    test_env = session.get("test_env",None)
    if text:
        form.text.data = text
    if text_from:
        form.text_from.data = text_from
    if base_env:
        form.base_env.data = base_env
    if test_env:
        form.test_env.data = test_env
    
    return render_template('diff.html',form=form,original_json=original_json,modified_json=modified_json)


# https://yanbin.blog/how-flask-work-with-asyncio/
def async_fetch_all_url(text_from:int,request_data:dict,base_env=str,test_env=str): # Dict[str:Response]

    def _get_response(url:str,headers:dict,params:dict,result:dict,env_name:str,cookies=dict()):
        response = requests.get(url=url,headers=headers,params=params,timeout=30)
        result[env_name] = response
        return response
    
    result: Dict[str:Response] = dict()
    url = ""
    headers = dict()
    payload = dict()
    cookies = dict()

    if text_from == "1": # from bytest
        url = "https://" + request_data["Host"] + request_data["Path"]
        payload = { item["Key"]:item["Value"] for item in request_data["Query"]}
        headers = { item["Key"]:item["Value"] for item in request_data["Header"]}
        headers["X-Use-Ppe"] = "1"
        cookies = { item["Key"]:item["Value"] for item in request_data["Cookies"]}

    if text_from == "2": # from bytediff
        url = "https://" + request_data["headers"]["Host"] + request_data["uri"]
        headers:dict = request_data["headers"]
        headers["X-Use-Ppe"] = "1"

    threads = []
    for env_name in [base_env,test_env]:
        kwargs = {"url":url,"headers":headers,"cookies":cookies,"params":payload,"env_name":env_name,"result":result}
        threads.append(threading.Thread(target=_get_response,kwargs=kwargs))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result
        
            
        
    








