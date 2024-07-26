# 构建数据集的json文件
import json
import random
import pandas as pd
import os


def generate_prompt(row):
    if row['type'] == '单选':
        return '你是电力领域的专家，这是一个单项选择题，请从A、B、C、D四个选项中选出最正确的一个，且仅需要回答字母。'
    elif row['type'] == '多选':
        return '你是电力领域的专家，这是一个多项选择题，请从A、B、C、D四个选项中选出最正确的几个，且仅需要按字母顺序回答字母'
    elif row['type'] == '问答':
        return '你是电力领域的专家，这是一个问答题，请逐步分析获得这个问题的解'


def get_prompt(row):
    promptSet = {
        '单选': "你是电力领域的专家，这是一个单项选择题，请从A、B、C、D四个选项中选出最正确的一个，且仅需要回答字母。",
        '多选': "你是电力领域的专家，这是一个多项选择题，请从A、B、C、D四个选项中选出最正确的几个，且仅需要按字母顺序回答字母",
        '问答': "你是电力领域的专家，这是一个问答题，请逐步分析获得这个问题的解",
        '问题前缀': "### 问题：",
        '答案前缀': "### 答案：",
        '类别前缀': "### 类别："
    }
    if row['type'] == '单选':
        strs = promptSet['单选']  +' '+ promptSet['问题前缀'] +' '+ row['question'] +' '+ promptSet['答案前缀'] + str(row['answer'])+' '+ promptSet['类别前缀'] +  ' ' + str(row['type'])
        return strs
    elif row['type'] == '多选':
        strs = promptSet['多选']  +' '+ promptSet['问题前缀'] +' '+ row['question'] +' '+ promptSet['答案前缀'] + str(row['answer'])+' '+ promptSet['类别前缀'] +  ' ' + str(row['type'])
        return strs
    elif row['type'] == '问答':
        strs = promptSet['问答']  +' '+ promptSet['问题前缀'] +' '+ row['question'] +' '+ promptSet['答案前缀'] + str(row['answer']) +' '+ promptSet['类别前缀'] +' ' + str(row['type'])
        return strs
    else:
        print("题目类型有误。")


def get_base_str(row):
    str = row['question'] + "答案：" + str(row['answer'])
    return str


def get_data_json(csv_path, json_path, add_prompt=True):
    df = pd.read_csv(csv_path)
    new_item_list = []
    for idx in range(len(df)):
        row = df.iloc[idx]
        item_dict = {}
        if add_prompt == True:
            item_dict['text'] = get_prompt(row)
        else:
            item_dict['text'] = get_base_str(row)
        new_item_list.append(item_dict)

    with open(json_path, 'w', encoding='UTF-8') as json_file:
        json.dump(new_item_list, json_file, ensure_ascii=False, indent=2)


def split_data(root_path, ori_file, val_size):
    """
    根据val_size将原始数据集按比例划分为train set和test set
    train set用于SFT训练，test set 用于测试正确率及 Rouge-L
    """
    ori_path = os.path.join(root_path, ori_file)
    with open(ori_path, 'r') as json_file:
        items = json.load(json_file)  # list类型
        # 按val_size比例随机抽取数据作为test set
        split_index = int(len(items) * val_size)
        # 随机打乱数据顺序
        random.seed(2)
        random.shuffle(items, random=r)
        test_list = items[:split_index]
        train_list = items[split_index:]
    train_path = os.path.join(root_path, 'train.json')
    test_path = os.path.join(root_path, 'test.json')
    with open(train_path, 'w') as f:
        json.dump(train_list, f, ensure_ascii=False, indent=2)
    with open(test_path, 'w') as f:
        json.dump(test_list, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    r = random.random
    csv_path = '/opt/data/private/zyx/data_all/data_total/data_split/testset.csv'
    json_path = '/opt/data/private/zyx/data_all/data_total/data_split/test_data.json'
    get_data_json(csv_path, json_path, add_prompt=True)
    # split_data(root_path='../new/data', ori_file='electric_data.json', val_size=0.1)
