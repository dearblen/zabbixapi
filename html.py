#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import json, pymysql

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
	100-max(item_data) free \
     FROM \
	time  \
     WHERE \
	item_key = 'vfs.fs.size[/,pfree]'  \
	AND hostname = \'%s\' \
	AND time >= DATE_SUB( CURDATE( ), INTERVAL  1 DAY )  \
	AND time < DATE_SUB( CURDATE( ), INTERVAL  0 DAY ) \
    GROUP BY \
	CEILING(DATE_FORMAT( time, \'%s\' )/2)" % (hostname, '%h')
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
	item_key = 'net.if.out[team0]'  \
	AND hostname = \'%s\' \
	AND time >= DATE_SUB( CURDATE( ), INTERVAL  1 DAY )  \
	AND time < DATE_SUB( CURDATE( ), INTERVAL  0 DAY ) \
    GROUP BY \
	CEILING(DATE_FORMAT( time, \'%s\' )/2)" % (hostname,'%h')
  return COLUMN

 def GetNetIn(self,hostname) :
  COLUMN = "SELECT \
	FORMAT(((item_data)/1024/1024),2) max \
    FROM \
	time  \
    WHERE \
	item_key = 'net.if.in[team0]'  \
	AND hostname = \'%s\' \
	AND time >= DATE_SUB( CURDATE( ), INTERVAL  1 DAY )  \
	AND time < DATE_SUB( CURDATE( ), INTERVAL  0 DAY ) \
    GROUP BY \
	CEILING(DATE_FORMAT( time, \'%s\' )/2)" % (hostname,'%h')
  return COLUMN

 def Changejs(self,hostname,key,file):
  list=self.ConnectDB(hostname,key)
  f = open("{}".format(file), 'r+', encoding='utf8')
  new = []
  for line in f:
   new.append(line)
  new[42] ="            data:%s,\n" % (list)
  f.seek(0)
  for n in new:
   f.write(n)
  f.close()
 def Changehtml(self,hostname,key,file):
  list=self.ConnectDB(hostname,key)
  print(list)
  f = open('echarts.html', 'r+', encoding='utf8')
  new = []
  for line in f:
   new.append(line)
  new[47] ='       <div id="order_num" class="order_num">%s</div> \n' % (list[0])
  f.seek(0)
  for n in new:
   f.write(n)
  f.close()
def main():
 data=DataGET()
 #cpuvalue=data.ConnectDB('GanSuMobilengx','cpu')
 #print(cpuvalue)
 data.Changehtml('GanSuMobilengx','80num','echarts.html')

if __name__ == '__main__':
 main()



