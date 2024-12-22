from flask import Flask,request
import os
import time
import requests
import json
import base64
import redis
import logging

app = Flask(__name__)
SK_ESTOKEN=''
SK_CMCKEY=''


@app.route('/hello')
def hello_world():
   return 'Hello World'
   
@app.route('/', methods=['GET', 'POST'])
@app.route('/index.php', methods=['GET', 'POST'])
def forward():
    url = 'http://127.0.0.1:85/index.php'
    method = request.method
    data = request.get_data()
   
    # 转发请求
    response = requests.request(method, url, data=data)
    
    # 返回转发请求的响应
    return response.content, response.status_code, response.headers.items()

@app.route('/getbal',methods=['GET'])
def getbal():
   addr=request.args.get('addr')
   addr=str(base64.b64decode(addr), 'utf-8')
   url="https://api.etherscan.io/api?module=account&action=balance&address="+addr+"&tag=latest&apikey="+SK_ESTOKEN
   res=requests.get(url)
   return res.text
   
@app.route('/gettkbal',methods=['GET'])
def gettkbal():
   addr=request.args.get('addr')
   addr=str(base64.b64decode(addr), 'utf-8')
   tkaddr=request.args.get('tkaddr')
   tkaddr=str(base64.b64decode(tkaddr), 'utf-8')
   url="https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress="+tkaddr+"&address="+addr+"&tag=latest&apikey="+SK_ESTOKEN
   res=requests.get(url)
   return res.text

@app.route('/getprice',methods=['GET'])
def getprice():
   url="https://api.etherscan.io/api?module=stats&action=ethprice&apikey="+SK_ESTOKEN
   res=requests.get(url)
   return res.text

@app.route('/geturl',methods=['GET'])
def geturl():
   tourl=request.args.get('tourl')
   url=str(base64.b64decode(tourl), 'utf-8')
   res=requests.get(url)
   return res.text

@app.route('/getcmcurl',methods=['GET'])
def getcmcurl():
   headers = {'Accepts': 'application/json','X-CMC_PRO_API_KEY': SK_CMCKEY}
   tourl=request.args.get('tourl')
   if tourl=='':
      tourl='/v1/cryptocurrency/listings/latest'
   else:
      tourl=str(base64.b64decode(tourl), 'utf-8')
      
   partxt=request.args.get('partxt')
   if partxt=='':
      parameters = {}
   else:
      partxt=str(base64.b64decode(partxt), 'utf-8')
      parameters=json.loads(partxt)
      
   url = 'https://pro-api.coinmarketcap.com'+tourl
   
   #app.logger.info('tourl:%s', tourl)
   #app.logger.info('partxt:%s', partxt)
   app.logger.info('parameters:%s', parameters)
   app.logger.info('url:%s', url)
   
   session = requests.Session()
   session.headers.update(headers)
   res=session.get(url,params=parameters)
   #app.logger.info('res.text:%s', res.text)
   return res.text
   
@app.route('/getcac',methods=['GET'])
def getcac():
   host="red-ctipejggph6c738b3u90"
   r = redis.Redis(host, port=6379, db=0)
   r.set('mykey', 'myvalue')
   return r.get('mykey')

if __name__ == '__main__':
   SK_ESTOKEN= os.environ.get('SK_ESTOKEN')
   SK_CMCKEY= os.environ.get('SK_CMCKEY')
   app.run('0.0.0.0',82,True)
