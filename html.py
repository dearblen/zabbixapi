#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import json, pymysql, re

class DataGET :
 def ConnectDB(self,hostname,key):
  db = pymysql.connect("10.100.6.214", "root", "Tjlh@2017", "serverstatus_test")
  cursor = db.cursor()
  if key == "cpu":
   COLUMN=self.Getcpu(hostname)
  elif key == "mem":
   COLUMN = self.GetMem(hostname)
  elif key == "freedesk":
   COLUMN = self.Getdesk(hostname)
  elif key == "totledesk":
   COLUMN = self.GetTotledesk(hostname)
  elif key == "80num":
   COLUMN = self.Get80num(hostname)
  elif key == "3306num":
   COLUMN = self.Get3306num(hostname)
  elif key == "8080num":
   COLUMN = self.Get8080num(hostname)
  elif key == "11211num":
   COLUMN = self.Get11211num(hostname)
  elif key == "NetOut":
   COLUMN = self.GetNetOut(hostname)
  elif key == "NetIn":
   COLUMN = self.GetNetIn(hostname)
  cursor.execute(COLUMN)
  results = cursor.fetchall()
  listdata=[]
  for i in range(len(results)):
   listdata.append(results[i][0])
  db.close()
  return listdata

 def GetTotleMem(self,hostname):
  db = pymysql.connect("10.100.6.214", "root", "Tjlh@2017", "serverstatus_test")
  cursor = db.cursor()
  sql = "SELECT cast(item_data as SIGNED) FROM time WHERE item_key = 'vm.memory.size[total]'  AND hostname = \'%s\' group by item_data" % (hostname)
  cursor.execute(sql)
  results = cursor.fetchall()
  return results[0][0]

 def GetMem(self,hostname) :
  totleMem=self.GetTotleMem(hostname)
  COLUMN="select  FORMAT((item_data) / %d * 100, 2) max \
  FROM time  WHERE item_key = 'vm.memory.size[available]' \
  AND hostname = \'%s\' \
  AND time >= DATE_SUB( CURDATE( ), INTERVAL  1 DAY ) \
  AND time < DATE_SUB( CURDATE( ), INTERVAL  0 DAY )\
  GROUP BY CEILING(DATE_FORMAT( time, \'%s\' )/2) " % (totleMem,hostname,'%h')
  return COLUMN

 def Getcpu(self, hostname):
  COLUMN ="SELECT \
	FORMAT( 100- max( item_data ), 2 ) max \
    FROM time \
    WHERE \
    item_key = 'system.cpu.util[,idle]' \
	AND hostname = \'%s\' \
	AND time >= DATE_SUB( CURDATE( ), INTERVAL 1 DAY ) \
	AND time < DATE_SUB( CURDATE( ), INTERVAL 0 DAY ) \
    GROUP BY \
	CEILING( DATE_FORMAT( time, \'%s\' ) / 2 )" % (hostname,'%h')
  return COLUMN

 def Getdesk(self,hostname) :
  COLUMN = "SELECT \
	max(cast(item_data as SIGNED)) \
     FROM \
	time  \
     WHERE \
	item_key like 'vfs.fs.size[/,free]'  \
	AND hostname = \'%s\' \
	AND time >= DATE_SUB( CURDATE( ), INTERVAL  1 DAY )  \
	AND time < DATE_SUB( CURDATE( ), INTERVAL  0 DAY ) " % (hostname)
  return COLUMN

 def GetTotledesk(self,hostname):
  COLUMN = "SELECT \
	cast(item_data as SIGNED) \
     FROM \
	time  \
     WHERE \
	item_key like  'vfs.fs.size[/,total]'  \
	AND hostname = \'%s\' \
	AND time >= DATE_SUB( CURDATE( ), INTERVAL  1 DAY )  \
	AND time < DATE_SUB( CURDATE( ), INTERVAL  0 DAY ) \
    GROUP BY item_data"  % (hostname)
  return COLUMN

 def Get80num(self,hostname) :
  COLUMN = "SELECT \
  	max(cast(item_data as SIGNED)) \
       FROM \
  	time  \
       WHERE \
  	item_key = '80connectNum'  \
  	AND hostname = \'%s\' \
  	AND time >= DATE_SUB( CURDATE( ), INTERVAL  1 DAY )  \
  	AND time < DATE_SUB( CURDATE( ), INTERVAL  0 DAY ) " % (hostname)
  return COLUMN

 def Get3306num(self,hostname) :
  COLUMN = "SELECT \
  	max(cast(item_data as SIGNED)) \
       FROM \
  	time  \
       WHERE \
  	item_key = '3306connectNum'  \
  	AND hostname = \'%s\' \
  	AND time >= DATE_SUB( CURDATE( ), INTERVAL  1 DAY )  \
  	AND time < DATE_SUB( CURDATE( ), INTERVAL  0 DAY ) " % (hostname)
  return COLUMN


 def Get8080num(self,hostname) :
  COLUMN = "SELECT \
  	max(cast(item_data as SIGNED)) \
       FROM \
  	time  \
       WHERE \
  	item_key = '8080connectNum'  \
  	AND hostname = \'%s\' \
  	AND time >= DATE_SUB( CURDATE( ), INTERVAL  1 DAY )  \
  	AND time < DATE_SUB( CURDATE( ), INTERVAL  0 DAY ) " % (hostname)
  return COLUMN

 def Get11211num(self,hostname) :
  COLUMN = "SELECT \
  	max(cast(item_data as SIGNED)) \
       FROM \
  	time  \
       WHERE \
  	item_key = '11211connectNum'  \
  	AND hostname = \'%s\' \
  	AND time >= DATE_SUB( CURDATE( ), INTERVAL  1 DAY )  \
  	AND time < DATE_SUB( CURDATE( ), INTERVAL  0 DAY ) " % (hostname)
  return COLUMN

 def GetNetOut(self,hostname) :
  COLUMN = "SELECT \
	FORMAT(((item_data)/1024/1024),2) max \
    FROM \
	time  \
    WHERE \
	item_key like  'net.if.out%s'  \
	AND hostname = \'%s\' \
	AND time >= DATE_SUB( CURDATE( ), INTERVAL  1 DAY )  \
	AND time < DATE_SUB( CURDATE( ), INTERVAL  0 DAY ) \
    GROUP BY \
	CEILING(DATE_FORMAT( time, \'%s\' )/2)" % ('%',hostname,'%h')
  return COLUMN

 def GetNetIn(self,hostname) :
  COLUMN = "SELECT \
	FORMAT(((item_data)/1024/1024),2) max \
    FROM \
	time  \
    WHERE \
	item_key like  'net.if.in%s'  \
	AND hostname = \'%s\' \
	AND time >= DATE_SUB( CURDATE( ), INTERVAL  1 DAY )  \
	AND time < DATE_SUB( CURDATE( ), INTERVAL  0 DAY ) \
    GROUP BY \
	CEILING(DATE_FORMAT( time, \'%s\' )/2)" % ('%',hostname,'%h')
  return COLUMN

 def Changejs(self,file,hostname,key):
  list=self.ConnectDB(hostname,key)
  f = open("{}".format(file), 'r+', encoding="utf-8")
  flist=f.readlines()
  flist[42] ="            data:%s,\n" % (list)
  f=open("{}".format(file),'w+',encoding="utf-8")
  f.writelines(flist)
  f.close()

 def Changedeskjs(self,hostname,file):
  list2=self.ConnectDB(hostname,'freedesk')
  list1=self.ConnectDB(hostname,'totledesk')
  list3=list1[0]-list2[0]
  #print(list1[0],list2[0],list3)
  f = open("{}".format(file), 'r+', encoding="utf-8")
  f = open("{}".format(file), 'r+', encoding="utf-8")
  flist=f.readlines()
  flist[36] ="                {value:%s, name:'已用容量G'},\n" % (int(list3/1024/1024/1024))
  flist[37] ="                {value:%s, name:'剩余容量G'},,\n" % (int(list2[0]/1024/1024/1024))
  f=open("{}".format(file),'w+',encoding="utf-8")
  f.writelines(flist)
  f.close()

 def Changehtml(self,hostname,key,file):
  data=self.ConnectDB(hostname,key)
  #print(data)
  f = open('{}'.format(file), 'r+', encoding="utf-8")
  s = f.read()
  if key == "80num":
   matchObj = re.search(r'>\d+<.*\n.*80.*', s)
  elif  key == "8080num":
   matchObj = re.search(r'>\d+<.*\n.*8080.*', s)
  elif  key == "3306num":
   matchObj = re.search(r'>\d+<.*\n.*3306.*', s)
  elif key == "11211num":
   matchObj = re.search(r'>\d+<.*\n.*11211.*', s)
  #print(matchObj)
  test = str(matchObj.group())
  begin = test.find('>')
  end = test.find('<')
  oldvalue = test[begin+1:end]
  file_data = ""
  with open('{}'.format(file), "r+", encoding="utf-8") as f:
   for line in f:
    if oldvalue in line:
     line = line.replace(str(oldvalue),str(data[0]))
    file_data += line
  with open('{}'.format(file), "r+", encoding = "utf-8") as f:
   f.write(file_data)

 def GetJson(self,file):
  with open('{}'.format(file),'r') as hosts:
   data = json.load(hosts)
  return data

 def dataInputHTML(self,file):
  for i in range(len(self.GetJson(file))):
   list = self.GetJson(file)[i]['htmlkey']
   #print(list)
   for j in range(2, len(list)):
    self.Changehtml('{}'.format(list[0]), '{}'.format(list[j]), '{}'.format(list[1]))
    #print(list[0],list[j],list[1])

 def dataInputJS(self,file):
  for i in range(len(self.GetJson(file))):
   list = self.GetJson(file)[i]['jskey']
   for j in range(1,len(list)):
    self.Changejs('{}'.format(list[j][0]), '{}'.format(list[0]), '{}'.format(list[j][1]))
    print(list[j][0],list[0],list[j][1])

 def dataInputDesk(self,file):
  for i in range(len(self.GetJson(file))):
   list = self.GetJson(file)
   #print(list[i]['deskjs'][0],list[i]['deskjs'][1])
   self.Changedeskjs('{}'.format(list[i]['deskjs'][0]),'{}'.format(list[i]['deskjs'][1]))

def main():
 data=DataGET()
 #data.Changejs('js/gansu/gansuweb01cpu.js','GanSuMobilenWEB01','cpu')
 #data.Changedeskjs('GanSuMobilenWEB01','js/gansu/gansuweb01desk.js')
 data.dataInputHTML("html.json")
 data.dataInputJS("js.json")
 data.dataInputDesk("desk.json")

if __name__ == '__main__':
 main()



