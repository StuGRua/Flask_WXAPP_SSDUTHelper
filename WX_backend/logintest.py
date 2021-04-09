import base64
from flask import jsonify,request
import requests, json

def testsignin():
    url_json = 'http://127.0.0.1:5000/api/users'
    headers={'Content-Type':'application/json'}
    data_json = json.dumps({'userid': 201873030, 'password': 'value22','phonenumber':13888071504})  # dumps：将python对象解码为json数据
    r_json = requests.post(url_json,headers=headers, data=data_json)
    print(data_json)
    print(r_json)
    print(r_json.headers)
    print(r_json.raw)

def testrequest(userid):
    url_json = 'http://127.0.0.1:5000/api/users/'+userid
    r_json = requests.get(url_json)
    print(r_json)
    print(r_json.headers)
    print(r_json.raw)
    print(r_json.content)
    print(r_json.text)

def testlogin(acc,pas):
    url = 'http://127.0.0.1:5000/api/token'
    #headers={'Content-Type':'application/json'}
    serect = acc + ":" + pas
    serect=str(base64.b64encode(serect.encode("utf-8")), "utf-8")
    headers = {"Authorization": "Basic {}".format(serect)}
    r_json = requests.get(url,headers=headers,data='')
    res=dict(r_json.json())
    print(res['token'])
    return res['token']
    #print(r_json)
#    print(r_json.headers)
#    print(r_json.content)

#    print(json.dumps(r_json.content))


def testres(token):
    url = 'http://127.0.0.1:5000/api/resource'
    serect = token + ":" + ''
    serect=str(base64.b64encode(serect.encode("utf-8")), "utf-8")
    headers = {"Authorization": "Basic {}".format(serect)}
    print(headers)
    r_json = requests.get(url,headers=headers,data='')
    #print(r_json)
    #print(r_json)
    print(r_json.headers)
    print(r_json.content)


if __name__=='__main__':
    #testsignin()
    # testrequest('201873030')
    token=testlogin('201873030','value22')
    testres(token)
    # print(r_json)
    # print(r_json.text)
    # print(r_json.content)