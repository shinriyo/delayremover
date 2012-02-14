#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import codecs
import urllib
import re

write = codecs.open("./output.txt","w","utf-8")
open = codecs.open("./input.txt","r","utf-8")

parcent_ary = []
source_ary = []

for x in open:
    parcent = re.search(".*%.*", x) # ％表示
    dot = re.search("^\.", x) # .スタート

    if dot: # アニメーションではないCSSのため
        break

    if parcent:
        per_num = re.search("([1-9]\d*|0)(\.\d+)?", x) # ％表示の数字
        if per_num:
            parcent_ary.append(per_num.group().rstrip())
            source_ary.append("REPLACE")
    else:
      source_ary.append(x.rstrip())

item_list = parcent_ary
duration = 0.0
delay = 0.0

for y in open:
    duration_reg = re.search("duration: ?(\d*\.?\d*)s?", y) # duration
    delay_reg = re.search("delay: ?(\d*\.?\d*)s?", y) # delay
    if duration_reg:
        duration = float(duration_reg.group(1))

    if delay_reg:
        delay = float(delay_reg.group(1))

#新全体の時間-----------------------
duration2 = duration + delay

replace_parcent_ary = []

#print (itemList)

for x in item_list:
    realtime =  (float(duration) * float(x)/100.0)
    replace_parcent = (realtime+delay)/duration2 * 100.0
    replace_parcent_ary.append(float("%.3f" % replace_parcent))

i = 0

# 置き換え
for wr in source_ary:
    replace = re.search("REPLACE", wr) # 置き換える
    if replace:
        parcent_num = str(replace_parcent_ary[i])
        if parcent_num == "100.0":
            parcent_num = "100"
        write.write("    " + parcent_num + "% {\n")
        i += 1
    else:
        write.write(wr + "\n")

write.write("    -webkit-animation-duration: " + str(float("%.3f" % duration2)) + "s;\n")
write.write("    -webkit-animation-delay: 0" + ";\n")

