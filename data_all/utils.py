"""
[
  {
    "prompt": "提示词",
    "input": "question",
    "output": "answer"
  },
  {
    "prompt": "提示词",
    "input": "question",
    "output": "answer"
  }
]
"""
import csv
import json

import pandas as pd

def generate_prompt(row):
    if row['type'] == '单选':
        return '你是电力领域的专家，这是一个单项选择题，请从A、B、C、D四个选项中选出最正确的一个，且仅需要回答字母。'
    elif row['type'] == '多选':
        return '你是电力领域的专家，这是一个多项选择题，请从A、B、C、D四个选项中选出最正确的几个，且仅需要按字母顺序回答字母'
    elif row['type'] == '问答':
        return '你是电力领域的专家，这是一个问答题，请逐步分析获得这个问题的解'

# def generate_prompt(row):
#     if row['type'] == '单选':
#         return '这是一个单项选择题，请选出最正确的一个选项。'
#     elif row['type'] == '多选':
#         return '这是一个多项选择题，请选出最正确的几个选项。'
#     elif row['type'] == '自由问答':
#         return ''


def get_data_json(csv_path):
    """
    将 csv 文件转换为 json 文件，带有相应的 prompt 提示
    """
    dict_list = []
    df = pd.read_csv(csv_path)
    for idx in range(len(df)):
        item_dict = {}
        row = df.iloc[idx]
        item_dict['instruction'] = generate_prompt(row)
        if item_dict['instruction'] == '':
            item_dict['instruction'] = row['question']
            item_dict['input'] = ''
        else:
            item_dict['input'] = row['question']
        item_dict['output'] = row['answer']
        dict_list.append(item_dict)
    with open('electric_aug_prompt.json', 'w') as json_file:
        json.dump(dict_list, json_file, ensure_ascii=False, indent=2)


def get_qa_only(csv_path):
    dict_list = []
    # csv_path = 'merged_file.csv'
    df = pd.read_csv(csv_path)
    for idx in range(len(df)):
        item_dict = {}
        row = df.iloc[idx]
        if row['type'] == '问答':
            item_dict['instruction'] = row['question']
            item_dict['input'] = ''
            item_dict['output'] = row['answer']
            dict_list.append(item_dict)
        else:
            continue
    with open('electric_aug_qa.json', 'w') as json_file:
        json.dump(dict_list, json_file, ensure_ascii=False, indent=2)



if __name__ == '__main__':
    csv_path = '/opt/data/private/zyx/data_all/data_total/data_argument/train_aug.csv'
    get_qa_only(csv_path)
    get_data_json(csv_path)