#!/usr/bin env python
# coding=utf-8

import math
import random

iter = 1
beta = 23
init_sigma = 10

def cum_gaussian(x):
  invsqrt2 = -0.707106781186547524400844362104
  return 0.5 * math.erfc(x * invsqrt2)

def v_fun(x):
  v = cum_gaussian(x)
  if v < 2.222758749e-162:
    return -x
  return (math.exp(-x * x / 2)) / math.sqrt(2 * math.pi) /v

def w_fun(x):
  if cum_gaussian(x) < 2.222758749e-162:
     return 1.0
  vWin = v_fun(x)
  return vWin * (vWin + x)


file = open("train_feature","r")

max_index = 0

for f in file:
  seg = f.strip().split("\t")
  for st in seg[1:]:
    index = int(st.split(":")[0])
    if index > max_index:
      max_index = index

# 均值和方差
m = range(max_index + 1)
v = range(max_index + 1)
for i in range(max_index + 1):
  m[i] = random.uniform(-0.5,0.5)
  v[i] = init_sigma

for i in range(iter):
  file = open("train_feature","r")
  for f in file:
    seg = f.strip().split("\t")
    label = int(seg[0])
    # bpr 的训练集 label值为1和-1
    if label > 0:
      label = 1
    else:
      label = -1 
    s = 0.0
    t = beta * beta 
    for st in seg[1:]:
      index = int(st.split(":")[0])
      s += m[index]
      t += v[index]
    std_sigma = math.sqrt(t)
    s = s * label /std_sigma
    v_result = v_fun(s)
    w_result = w_fun(s)
    for st in seg[1:]:
      index = int(st.split(":")[0])
      m[index] = m[index] + label * v[index] / std_sigma * v_result
      v[index] = v[index] * (1-v[index] / t * w_result)

file = open("validate_feature","r")
toWrite = open("pctr","w+")
c = 0
for f in file:
  c += 1
  seg = f.strip().split("\t")
  label = int(seg[0])
  s = 0.0
  t = beta * beta
  for st in seg[1:]:
    index = int(st.split(":")[0])
    if index <= max_index:
      s += m[index]
      t += v[index]
  
  std_sigma = math.sqrt(t)
  p = cum_gaussian(s / std_sigma)
  s = str(c) +"," + seg[0] + "," +str(p) + "\n" 
  toWrite.write(s)

toWrite.close()

    
c = 0
filet = open("test_feature","r")
toWrite2 = open("test_pctr","w+")
toWrite3 = open("test_pctr.csv","w+")

for f in filet:
  c += 1
  seg = f.strip().split("\t")
  label = int(seg[0])
  s = 0.0
  t = beta * beta
  for st in seg[1:]:
    index = int(st.split(":")[0])
    if index <= max_index:
      s += m[index]
      t += v[index]

  std_sigma = math.sqrt(t)
  p = cum_gaussian(s / std_sigma)
  label = 0
  if p > 0.5:
    label = 1
  s2 = str(c) + "," + str(label) + "," +str(p) +"\n"
  s3 = str(p) +"\n"
  toWrite2.write(s2)
  toWrite3.write(s3)


toWrite2.close()
toWrite3.close()


