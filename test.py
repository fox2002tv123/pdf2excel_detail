# 
'''
Author: bob
Date: 2022-05-24 16:59:52
LastEditors: bob
LastEditTime: 2022-05-24 16:59:58
FilePath: \任务22-开发网络版对账单转换工具\main.ipynb
Description: 使用python编写的网络版对账单转换工具

Copyright (c) 2022 by bob, All Rights Reserved. 
'''


# 
# open读取txt文件

with open('data.txt', 'r',encoding='utf-8') as f:
    data = f.read()
data

# 
# 1.通过re模块提取数据-表头
import re
p=r'(\d{5,6}) (\S{17}) (\S{6})'
res_head=re.findall(p,data)
res_head


# 
# 2.通过re模块提取数据-表体
# import re
p=r'\*( 赔付)(\S*) ?(\S*) ?(\S*) ?(\S*) ?(\S*) ?(\S*) ?(\S*)'
res_body=re.findall(p,data)
res_body

# 
# 3.通过re模块提取数据-对账单序列号
# import re
p=r'Credit Note Number (\d{7})'
res_number=re.findall(p,data)
res_number=res_number[0]
res_number

# 
# 4.通过re模块提取数据-对账单日期
# import re
p=r'created on (\S{10})'
res_date=re.findall(p,data)
res_date=res_date[0]
res_date

# 

# 5.判断国产还是进口
first_char=res_head[0][1][0]
if first_char=='L':
    s='BBA'
else:
    s='GIS'
s

# 
# 通过pandas转换成dataframe
import pandas as pd
import numpy as np
df1=pd.DataFrame(res_head,columns=['保修单号','车架号','DWP保修单号'])
df1
df2=pd.DataFrame(res_body,columns=list('A1234567'))
df2
# 合并两个dataframe concat axis=1
df=pd.concat([df1,df2],axis=1)
df

# 去掉',',并转换成float
df.loc[:,'1':'7']=df.loc[:,'1':'7'].applymap(lambda x:str(x).replace(',',''))

# 转换成float
for i in range(1,8):
    df.loc[:,'{}'.format(i)]=pd.to_numeric(df.loc[:,'{}'.format(i)],errors='coerce')

# 添加汇总列
df['总计']=df.loc[:,'1':'7'].max(axis=1)

# 添加各种'对账单序列号','对账单日期'列
df['对账单序列号']=res_number
df['对账单日期']=res_date.replace('.','/')

df.head()
# df.info()

#  [markdown]
# 
# # 附加功能-找到每个细节

# 
df.shape

# 
# 0.re提取每个特征-生成段落
import re
detail_list=re.findall(r'[^_]+',data)[:-1]
detail_list.__len__()
detail_list[0]


# 
# 1提取工时行
FRU=re.findall(r'(\S{10}) (\d{7}) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)',detail_list[0])
FRU
df_FRU=pd.DataFrame(FRU,columns=list('ABCDFHKL'))
df_FRU

# 
# 2.提取零件行-正常配件
part_normal=re.findall(r'(\S{10}) (\S{11}) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)',detail_list[1])
part_normal
df_part_normal=pd.DataFrame(part_normal,columns=list('ABCDEFGJKL'))
df_part_normal

# 
# 3.提取零件行-BSI配件
part_BSI=re.findall(r'(8\S{8}6) (\S{11}) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)',detail_list[0])
part_BSI
df_part_BSI=pd.DataFrame(part_BSI,columns=list('ABCDFGKL'))
df_part_BSI

# 
# 4.提取辅料
sub_4=re.findall(r'(\S{10}) (\S{1}) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)',detail_list[0])
sub_4
df_sub_4=pd.DataFrame(sub_4,columns=list('ABCDFIKL'))
df_sub_4

# 
# 5.找到单行的表头
p=r'(\d{5,6}) (\S{17}) (\S{6})'
one_head=re.findall(p,detail_list[0])
one_head
claim,vin,dwp=one_head[0]
claim,vin,dwp

# 
# 建立一个空的dataframe，只包括表头-作用是避免漏掉没有数据的列
df_na=pd.DataFrame(columns=list('ABCDEFGHIJKL'))
df_na

# 
# 拼接dataframe
res_one_part=pd.concat([df_FRU,df_part_normal,df_part_BSI,df_sub_4],axis=0)
# column 按照字母排序
res_one_part.sort_index(axis=1,inplace=True)
# claim vin dwp 插入前三列
res_one_part.insert(0,'claim',claim)
res_one_part.insert(1,'vin',vin)
res_one_part.insert(2,'dwp',dwp)
res_one_part


