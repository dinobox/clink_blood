#!/usr/bin/python
# -*- coding:UTF-8 -*-
#2017-11-15
import os
import time
import sys
class Semioe_clickBlood:
  def __init__ ( self, parent = None ):
      self.loop=True
      self.out=sys.stdout
  def display(self,str):
    #str="Characteristic value/descriptor: fe fd 40 01 6b 0a"
    str=str[33:50].replace(" ","").replace("fefd","").replace("0a","")
    if len(str)!=6:
      #error
      msg="error"
    else:
      state=str[0:2] #状态：00表示测量中温度正常，40表示测量结束，温度正常。41表示测量中，温度低，42表示测量结束，温度高。A0表示错误，A1表示电压不足。
      temp_hex=str[2:6] #16进制温度
      temp_int=int(temp_hex,16)*0.1 #转化为10进制的温度
      temp_str="%s℃" % (temp_int) #字符串的温度
      if state=="00":
        self.out.write("\r测量中 %s" % (temp_str))
      if state=="40":
        self.out.write("\r测量成功，您的温度是：%s\n" % (temp_str))
        self.loop=False
      if state=="42":
        self.out.write("\r体温异常！您的温度是：%s" % (temp_str))
        self.loop=False
      if state=="A0":
        self.out.write("\r系统错误！")
        self.loop=False
      if state=="A1":
        self.out.write("\r电池不足，请更换！")
        self.loop=False
      self.out.flush()
    if self.loop:
      self.get_value()
  def get_value(self):
    time.sleep(0.5)
    process = os.popen("sudo gatttool -b C6:05:04:03:F1:BF --char-read -a 0x001b")
    output = process.read()
    #out.write("\n%s" % (output))
    self.display(output)
    process.close

if __name__ == '__main__':
  os.system("sudo hciconfig hci0 down")
  os.system("sudo hciconfig hci0 up")
  semioe_clickBlood=Semioe_clickBlood()
  semioe_clickBlood.get_value()
