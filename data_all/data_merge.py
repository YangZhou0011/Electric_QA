# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.model_selection import train_test_split

datapath_S = './data_total/single_choice_dataset.csv'
datapath_M = './data_total/multiple_choice_dataset.csv'
datapath_Q = './data_total/qa_dataset.csv'

data_path = './data_total/data_split/trainset.csv'


def data_split(df):
    # 读取 CSV 文件
    # df = pd.read_csv(datapath)
    # 按照 9:1 的比例进行随机划分
    train_df, test_df = train_test_split(df, test_size=0.1, random_state=42)

    # 打印划分后的训练集和测试集
    # print("训练集:")
    # print(train_df)
    # print("测试集:")
    # print(test_df)
    return train_df, test_df

def pro_choice_aug(df,colum='type',name='单选'):
    # df = pd.read_csv(datapath)
    df['question'] = df['question'] +' A.' +  df['A'] + ' B.' + df['B'] + ' C.' + df['C'] + ' D.' + df['D']
    df = df.drop(['A', 'B', 'C', 'D'], axis=1)
    df[colum] = name
    # print(df)
    return df

def pro_choice(datapath,colum='type',name='单选'):
    df = pd.read_csv(datapath)
    df['question'] = df['question'] +' A.' +  df['A'] + ' B.' + df['B'] + ' C.' + df['C'] + ' D.' + df['D']
    df = df.drop(['A', 'B', 'C', 'D'], axis=1)
    df[colum] = name
    # print(df)
    return df

def pro_qus(datapath,colum='type',name='问答'):
    df = pd.read_csv(datapath)
    df[colum] = name
    return df


def pro_choice_augment_other(datapath,sp_col='question',colum='type', spec='单选'):
    df = pd.read_csv(datapath)
    # selected_rows = df[df[colum] == spec]
    other_rows = df[df[colum] != spec]
    # quetion = selected_rows[sp_col]
    # split_columns = quetion.str.split(' ', expand=True)
    # print(split_columns)
    return other_rows


def sing_augment_toB(df,ans='A'):
    # 创建一个空的数据框来存储调换后的行
    new_rows = pd.DataFrame(columns=df.columns)
    for index, row in df.iterrows():
    # 根据某个列的值调换其他列的值
        if row['answer'] == ans:
            # 创建一个副本以避免修改原始行
            new_row = row.copy()  
            # 调换其他列的值
            temp_value = new_row[ans]
            new_row[ans] = new_row['B']
            new_row['B'] = temp_value
            new_row['answer'] = 'B'
            # 将调换后的行添加到新的数据框
            new_rows = new_rows.append(new_row, ignore_index=True)
    return new_rows


def sing_augment_toC(df,ans='A'):
    # 创建一个空的数据框来存储调换后的行
    new_rows = pd.DataFrame(columns=df.columns)
    for index, row in df.iterrows():
    # 根据某个列的值调换其他列的值
        if row['answer'] == ans:
            # 创建一个副本以避免修改原始行
            new_row = row.copy()  
            # 调换其他列的值
            temp_value = new_row[ans]
            new_row[ans] = new_row['C']
            new_row['C'] = temp_value
            new_row['answer'] = 'C'
            # 将调换后的行添加到新的数据框
            new_rows = new_rows.append(new_row, ignore_index=True)
    return new_rows


def sing_augment_toD(df,ans='B'):
    # 创建一个空的数据框来存储调换后的行
    new_rows = pd.DataFrame(columns=df.columns)
    for index, row in df.iterrows():
    # 根据某个列的值调换其他列的值
        if row['answer'] == ans:
            # 创建一个副本以避免修改原始行
            new_row = row.copy()  
            # 调换其他列的值
            temp_value = new_row[ans]
            new_row[ans] = new_row['D']
            new_row['D'] = temp_value
            new_row['answer'] = 'D'
            # 将调换后的行添加到新的数据框
            new_rows = new_rows.append(new_row, ignore_index=True)
    return new_rows


other_rows = pro_choice_augment_other(data_path)
df = pd.read_csv(datapath_S)
train_sin, test_sin = data_split(df)

# A
A_B = sing_augment_toB(train_sin,'A')
A_C = sing_augment_toC(train_sin,'A')

# B
B_C = sing_augment_toC(train_sin,'B')
B_D = sing_augment_toD(train_sin,'B')

# C
C_D = sing_augment_toD(train_sin,'C')
C_B = sing_augment_toB(train_sin,'C')

# D
D_B = sing_augment_toB(train_sin,'D')
D_C = sing_augment_toC(train_sin,'D')

merged_argu = pd.concat([train_sin, A_B, A_C, B_C, B_D, C_D, C_B, D_B, D_C], ignore_index=True)
merged_argu = pro_choice_aug(merged_argu)
merged_argu = pd.concat([merged_argu,other_rows], ignore_index=True)

# print(merged_argu)

merged_argu.to_csv('./data_total/data_argument/train_aug.csv',index=False)
# print(D_C)



# df_sing = pro_choice(datapath_S)
# df_multi = pro_choice(datapath_M,'type','多选')
# df_qu = pro_qus(datapath_Q)



# train_mul, test_mul = data_split(df_multi)
# train_qu, test_qu = data_split(df_qu)


# merged_train = pd.concat([train_sin, train_mul, train_qu], ignore_index=True)
# merged_test = pd.concat([test_sin, test_mul, test_qu], ignore_index=True)

# merged_train.to_csv('./data_total/data_split/trainset.csv',index=False)
# merged_test.to_csv('./data_total/data_split/testset.csv',index=False)


# print(train_sin)
# print(train_mul)
# print(train_qu)



