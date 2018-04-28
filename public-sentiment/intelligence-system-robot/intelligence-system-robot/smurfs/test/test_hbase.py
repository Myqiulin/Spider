# -*- coding: utf-8 -*-
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from hbase import Hbase
from hbase.ttypes import *

transport = TSocket.TSocket('192.168.11.194', 9090)

transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)

client = Hbase.Client(protocol)

transport.open()
#row = 'row-key1'

#mutations = [Mutation(column="cf:a", value="1")]
#client.mutateRow('test', row, mutations, None)

#获取表所有内容
row = client.getRow('TB_INFORMATION','9P-1494656614763')
for k,v in row[0].columns.items():
   print type(k),type(v),v.value


scanner = client.scannerOpen('TB_INFORMATION','',['f1:infoTitle'])
#column = client.getRowWithColumns('TB_INFORMATION','9P-1494656614763',['f1:infoTitle'])
r = client.scannerGet(scanner)
result =[]
while r:
   print r[0]
   for i in r:
      result.append(i)
      print i
      r = client.scannerClose(scanner)

print 'END'
print result

"""
添加数据
name = Mutation(column=bytes('f1:infoType'), value=bytes('name'))
foo = Mutation(column=bytes('f1:infoContent'), value=bytes('value'))

client.mutateRow('TB_INFORMATION', 'THERE', [name, foo])
"""
