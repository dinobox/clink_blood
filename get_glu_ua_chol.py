#!/usr/bin/python
# -*- coding:UTF-8 -*-
from bluepy import btle
from bluepy.btle import DefaultDelegate
import time
import binascii
import struct
import sys
getValue=False
class NotifyDelegate(DefaultDelegate):
    def __init__(self):
            DefaultDelegate.__init__(self)
    def handleNotification(self,cHandle,data):
        byte_text = binascii.b2a_hex(data) #得到的数据，是byte的字符串
        #val = binascii.unhexlify(val)
        #val = struct.unpack('f', val)[0]
        #print "notify from %s = %s\n" % (str(cHandle),str(val))
        text=str(byte_text, encoding = "utf-8") #转成utf8格式的字符串
        #text=str(text)
        text=text.replace("2450434c","") #去掉前缀信息（该硬件固定格式）
        if(len(text)==32):
            type=text[0:2]
            hex_value=text[26:28]
            int_value=int(hex_value,16) #16进制转成10进制
            #print "value:%s" % value
            #hex 2 10
            float_value=float(int_value) #整型转为浮点
            type_name=''
            mmol_value=0
            #根据不同的类别，用不同的计算公式。
            if(type=="41"): #glu
                 type_name='血糖(GLU)'
                 mmol_value=float_value/18
            if(type=="51"): #ua
                 type_name='尿酸（UA）'
                 mmol_value=float_value/16.81*0.1
            if(type=="61"): #chol
                 type_name='胆固醇（CHOL）'
                 mmol_value=float_value/38.66
            print ("\n %s: %.2f mmol/L\n" % (type_name,mmol_value))
            sys.exit() 
        else:
            print ("err\n")
            print (text)

dev=btle.Peripheral("00:15:83:00:47:B4").withDelegate(NotifyDelegate())

time.sleep(0.5)
print ("正在获取数据。。。")
try:
  while(True):
      dev.waitForNotifications(1)
      time.sleep(0.5)
finally:
    dev.disconnect()
