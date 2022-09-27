

#
# open读取txt文件

# with open('data.txt', 'r',encoding='utf-8') as f:
#     data = f.read()

# data

#
# 预留-数据data提取的第二种方法
# data=input('请输入数据：')
# data
# txt_message = Element("message") # 创建一个文本框
# container = Element("output") # 容器

def run(data):
    # return 1

    # data=txt_message.value # 获取文本框的值
    #
    # 1.通过re模块提取数据-表头
    import re
    p = r'(\d{5,6}) (\S{17}) (\S{6})'
    res_head = re.findall(p, data)
    res_head

    #
    # 2.通过re模块提取数据-表体
    # import re
    p = r'\*( 赔付)(\S*) ?(\S*) ?(\S*) ?(\S*) ?(\S*) ?(\S*) ?(\S*)'
    res_body = re.findall(p, data)
    res_body

    #
    # 3.通过re模块提取数据-对账单序列号
    # import re
    p = r'Credit Note Number (\d{7})'
    res_number = re.findall(p, data)
    res_number = res_number[0]
    res_number

    #
    # 4.通过re模块提取数据-对账单日期
    # import re
    p = r'created on (\S{10})'
    res_date = re.findall(p, data)
    res_date = res_date[0]
    res_date

    #
    # 5.判断国产还是进口
    first_char = res_head[0][1][0]
    if first_char == 'L':
        s = 'BBA'
    else:
        s = 'GIS'
    s

    #
    # 0.re提取每个特征-生成段落
    import pandas as pd

    import re
    detail_list = re.findall(r'[^_]+', data)[:-1]
    detail_list.__len__()

    res_list = []
    for i in detail_list:

        concat_list = []

        #
        # 1提取工时行
        FRU = re.findall(
            r'(\S{10}) (\d{7}) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)', i)
        if FRU:
            df_FRU = pd.DataFrame(FRU, columns=list('ABCDFHKL'))
            concat_list.append(df_FRU)
        

        #
        #   2.提取零件行-正常配件
        part_normal = re.findall(
            r'(\S{10}) (\S{11}) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)', i)
        part_normal
        if part_normal:
            df_part_normal = pd.DataFrame(
                part_normal, columns=list('ABCDEFGJKL'))
            concat_list.append(df_part_normal)
        #

        #
        # 3.提取零件行-BSI配件
        part_BSI = re.findall(
            r'(8\S{8}6) (\S{11}) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)', i)
        part_BSI
        df_part_BSI = pd.DataFrame(part_BSI, columns=list('ABCDFGKL'))
        df_part_BSI
        # 3.提取零件行-BSI配件
        part_BSI = re.findall(
            r'(8\S{8}6) (\S{11}) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)', i)
        part_BSI
        if part_BSI:
            df_part_BSI = pd.DataFrame(part_BSI, columns=list('ABCDFGKL'))
            concat_list.append(df_part_BSI)

        # 4.提取零件行-全陪付配件
        #  re 设置为多行模式
        # re.MULTILINE
        df_part_short_detail = re.findall(
            r'^(\S{10}) (\S{11}) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)$', i, re.MULTILINE)
        df_part_short_detail
        if df_part_short_detail:
            df_short = pd.DataFrame(
                df_part_short_detail, columns=list('ABCDFGJKL'))
            concat_list.append(df_short)
        #
        # 5.提取辅料
        sub_4 = re.findall(
            r'(\S{10}) (\S{1}) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+)', i)
        sub_4
        if sub_4:
            df_sub_4 = pd.DataFrame(sub_4, columns=list('ABCDFIKL'))
            concat_list.append(df_sub_4)


        # 6.提取F111
        F111 = re.findall(r'(9999001386) (4) (\S+) (\S+) (\S+) (\S+) (\S+)', i)
        F111
        if F111:
            df_F111 = pd.DataFrame(F111, columns=list('ABCFIKL'))
            concat_list.append(df_F111)

        #
        # 7.找到单行的表头
        p = r'(\d{5,6}) (\S{17}) (\S{6})'
        one_head = re.findall(p, i)
        one_head
        claim, vin, dwp = one_head[0]
        claim, vin, dwp

        #
        # 建立一个空的dataframe，只包括表头-作用是避免漏掉没有数据的列
        df_na = pd.DataFrame(columns=list('ABCDEFGHIJKL'))
        concat_list.append(df_na)

        #
        # 拼接dataframe
        res_one_part = pd.concat(concat_list, axis=0)
        # column 按照字母排序
        res_one_part.sort_index(axis=1, inplace=True)
        # claim vin dwp 插入前三列
        res_one_part.insert(0, 'claim', claim)
        res_one_part.insert(1, 'vin', vin)
        res_one_part.insert(2, 'dwp', dwp)
        res_list.append(res_one_part)

    res1 = pd.concat(res_list, axis=0)
    res = res1.to_csv(index=False)
    
    return res_number, res_date, s, res  # 返回对账单序列号和对账单日期
    
