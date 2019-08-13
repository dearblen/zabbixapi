#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import json, pymysql,os
import urllib.request, urllib.error, urllib.parse
import configparser
class ZabbixAPI:
 def __init__(self):
  self.__url = 'http://139.196.37.202/zabbix/api_jsonrpc.php'
  self.__user = 'admin2'
  self.__password = 'admin'
  self.__header = {"Content-Type": "application/json-rpc"}
  self.__token_id = self.UserLogin()
 #登陆获取token

 def UserLogin(self):
  data = {
   "jsonrpc": "2.0",
   "method": "user.login",
   "params": {
    "user": self.__user,
    "password": self.__password
   },
   "id": 0,
  }
  return self.PostRequest(data)
 #推送请求
 def PostRequest(self, data):
  request = urllib.request.Request(self.__url,json.dumps(data).encode('utf-8'),self.__header)
  result = urllib.request.urlopen(request)
  response = json.loads(result.read().decode('utf-8'))
  result.close()
  try:
   # print response['result']
   return response['result']
  except KeyError:
   raise KeyError

 def GotHostid(self,hostName):
  data = {
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": "hostid",
        "filter": {
            "host": hostName
        }
    },
    "auth": self.__token_id,
    "id": 1
  }
  hostid = self.PostRequest(data)[0]["hostid"]
  return hostid

 def GotItemid(self, hostName, key):
  hostid=self.GotHostid(hostName)
  data = {
   "jsonrpc":"2.0",
   "method": "item.get",
   "params": {
   "output": "itemids",
   "hostids": hostid,
   "search": {
            "key_": key
             },
   },
   "auth": self.__token_id,
   "id":1,       
  }
  
  itemid = self.PostRequest(data)[0]["itemid"]

  return itemid


 def ItemValueGET_int(self, hostName, key):
  itemid=self.GotItemid(hostName, key)
###history参数中有0,1,2,3,4表示：float,string,log,integer,text
  data = {
   "jsonrpc":"2.0",
   "method": "history.get",
   "params": {
   "output": "extend",
   "history": 3,
   "itemids": itemid,
   "limit": 1
   },
   "auth": self.__token_id,
   "id":1,       
  }
  return self.PostRequest(data)
 def GetJson(self):
  with open('hostlist.json','r') as hosts:
   data = json.load(hosts)

  return data

 def ItemValueGET_flaot(self, hostName, key):
  itemid=self.GotItemid(hostName, key)
###history参数中有0,1,2,3,4表示：float,string,log,integer,text
  data = {
   "jsonrpc":"2.0",
   "method": "history.get",
   "params": {
   "output": "extend",
   "history": 0,
   "itemids": itemid,
   "limit": 1
   },
   "auth": self.__token_id,
   "id":1,
  }
  return self.PostRequest(data)

 def insertMysqlF(self,HOST,ITEMKEY,ITEMDATA):
  db = pymysql.connect("10.100.6.214", "root", "Tjlh@2017", "serverstatus_test")
  cursor = db.cursor()
  sql = "INSERT INTO time(time,hostname,item_key,item_data) \
          VALUES (CURTIME(),'%s','%s','%.2f')" % (HOST,ITEMKEY,ITEMDATA)
  try:
   # 执行sql语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
  except:
   # 如果发生错误则回滚
   db.rollback()

  # 关闭数据库连接
  db.close()

 def insertMysqlI(self,HOST,ITEMKEY,ITEMDATA):
  db = pymysql.connect("10.100.6.214", "root", "Tjlh@2017", "serverstatus_test")
  cursor = db.cursor()
  sql = "INSERT INTO time(time,hostname,item_key,item_data) \
          VALUES (CURTIME(),'%s','%s','%d')" % (HOST,ITEMKEY,ITEMDATA)
  try:
   # 执行sql语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
  except:
   # 如果发生错误则回滚
   db.rollback()

  # 关闭数据库连接
  db.close()

 def loadIni(self):
  for i in range(len(self.GetJson())):
   host=(self.GetJson()[i]['keyList'][0])
   keylist=(self.GetJson()[i]['keyList'][1::])
   for key in keylist:
    if key == "system.cpu.util[,idle]":
     value=self.ItemValueGET_flaot(host,key)
     #print("{0} 的 {1} 是{2}%".format(host,key,float(value[0]['value'])))
     #print("{0} 的 {1} 是{2}%".format(host, key, float(value[0]['value'])))
     self.insertMysqlF(host,key,float(value[0]['value']))
    else:
     value=self.ItemValueGET_int(host,key)
     #print("{0} 的 {1} 是{2}".format(host,key,float(value[0]['value'])))
     #print(host, key, value)
     self.insertMysqlI(host, key, float(value[0]['value']))
    

def main():
 zapi=ZabbixAPI()
 #while True:
 zapi.loadIni()
 #print(os.getpid())

if __name__ == '__main__':
 main()

