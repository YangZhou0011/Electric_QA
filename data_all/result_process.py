import re
import json
import pandas as pd




def find_answer(text):
    patterns = [
        r'\s*([A-D])$',# 正确数量不增加
        r"^答：\s*([A-D])",
        r"答：\s*([A-D])",
        r"答案\s*([A-D])",
        r"^选([A-D])",
        r"选([A-D])",
        r"选：([A-D])",
        r"故([A-D])",
        # r"因此为([A-D])",
        r"^选项([A-D])",
        r"选项([A-D])",
        r"选择([A-D])",
        r"是\s*([A-D])",
        r"为?([A-D])选项",
        r"即?([A-D])。",
        r"答案是\s*选?项?\s?([A-D])",
        r"答案为\s*选?项?\s?([A-D])",
        r"答案应为\s*选?项?\s?([A-D])",
        r"答案选\s*选?项?\s?([A-D])",
        r"答案是:\s*选?项?\s?([A-D])",
        r"答案应该是:\s*选?项?\s?([A-D])选?项?",
        r"答案应该是\s*选?项?\s?([A-D])选?项?",
        r"答案应该选\s*([A-D])",
        r"正确的一项是\s*([A-D])",
        r"正确的一项为\s*([A-D])",
        r"正确的?选项是\s*([A-D])",
        r"正确的?选项为\s*([A-D])",
        r"答案为:\s*选?项?\s?([A-D])",
        r"答案应为:\s*选?项?\s?([A-D])",
        r"答案:\s*选?项?\s?([A-D])",
        r"答案是：\s*选?项?\s?([A-D])",
        r"答案应该是：\s*选?项?\s?([A-D])",
        r"答案为：\s*选?项?\s?([A-D])",
        r"答案应为：\s*选?项?\s?([A-D])",
        r"答案：\s*选?项?\s?([A-D])",
        r"选?项?([A-D])是正确的?答案",
        r"选?项?([A-D])为正确的?答案",
        r"([A-D])选?项?是正确的?答案",
        r"([A-D])选?项?为正确的?答案",
        r"最终答案为([A-D])",
        r"答案为\s*(\w+)",
        r"^答案：([A-D])",
        r"^故选([A-D])",
        r"^解答：([A-D])",
        r"^是([A-D])",
        r"^选项是([A-D])",
        r"^选项([A-D])",
        r"^故([A-D])",
        r"解答： ([A-D])"
        # r"选项\s*[A-D]"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            answer = match.group(1)
            return answer
    
    return '没有匹配到'
    
# 单选后处理
def extract_ans_single(response_str, cot):
    pattern = [
        r"^选([A-D])",
        r"^选项([A-D])",
        r"答案是\s*选?项?\s?([A-D])",
        r"答案为\s*选?项?\s?([A-D])",
        r"答案应为\s*选?项?\s?([A-D])",
        r"答案选\s*选?项?\s?([A-D])",
        r"答案是:\s*选?项?\s?([A-D])",
        r"答案应该是:\s*选?项?\s?([A-D])选?项?",
        r"答案应该是\s*选?项?\s?([A-D])选?项?",
        r"答案应该选\s*([A-D])",
        r"正确的一项是\s*([A-D])",
        r"正确的一项为\s*([A-D])",
        r"正确的?选项是\s*([A-D])",
        r"正确的?选项为\s*([A-D])",
        r"答案为:\s*选?项?\s?([A-D])",
        r"答案应为:\s*选?项?\s?([A-D])",
        r"答案:\s*选?项?\s?([A-D])",
        r"答案是：\s*选?项?\s?([A-D])",
        r"答案应该是：\s*选?项?\s?([A-D])",
        r"答案为：\s*选?项?\s?([A-D])",
        r"答案应为：\s*选?项?\s?([A-D])",
        r"答案：\s*选?项?\s?([A-D])",
        r"选?项?([A-D])是正确的?答案",
        r"选?项?([A-D])为正确的?答案",
        r"([A-D])选?项?是正确的?答案",
        r"([A-D])选?项?为正确的?答案",
        r"最终答案为([A-D])"
    ]
    ans_list = []
    # if not cot:
    # if response_str[0] in ["A", 'B', 'C', 'D']:
        # ans_list.append(response_str[0])
    # else:
    #     if len(response_str)>=2:
    #         if response_str[0] in ["A", 'B', 'C', 'D'] and response_str[1] in [".", "."] :
    #             ans_list.append(response_str[0])
    #     else:
    #         if response_str[0] in ["A", 'B', 'C', 'D']:
    #             ans_list.append(response_str[0])

    for p in pattern:
        if len(ans_list) == 0:
            ans_list = re.findall(p, response_str)
            print(ans_list)
        else:
            break
    return ans_list

# 读取原始文件
def read_result_split(datapath,group_clo='type'):
    # 读取JSON文件
    with open(datapath, 'r') as file:
        json_data = json.load(file)
    df = pd.DataFrame(json_data)
    # 创建一个列表来存储分组后的DataFrame
    grouped_dataframes = []
    grouped = df.groupby(group_clo)
    for group_name, group_df in grouped:
        # 创建一个独立的DataFrame副本，并将其添加到列表中
        group_copy = group_df.copy()
        grouped_dataframes.append(group_copy)
    return grouped_dataframes

def single_ans(df_single):
    ans_list = df_single['label'].tolist()
    generate_list = df_single['generate'].tolist()
    total_len = len(ans_list)
    correct = 0
    for index, element in enumerate(generate_list):
        ans = find_answer(str(element))
        print(ans_list[index][0])
        if ans == '没有匹配到':
            print(element)
        else:
            print(ans[0])
        if ans[0] == str(ans_list[index])[0]:
            # print(ans)
            # print(str(ans_list[index]))
            correct += 1
        print('-'*40)
    print(correct)

datapath = '/opt/data/private/zyx/data_all/data_total/data_split/test_result.json'
grouped_dataframes = read_result_split(datapath)

# # 遍历grouped_dataframes列表，访问每个DataFrame
# for i, df in enumerate(grouped_dataframes):
#     # 打印DataFrame索引和内容
#     print("DataFrame索引:", i)
#     print("DataFrame内容:")
#     print(df)
#     print()

df_single = grouped_dataframes[0]
df_multi = grouped_dataframes[1]
df_qz = grouped_dataframes[2]

single_ans(df_single)

# txts = '分析：惰性失真是由于阻抗饱和或者电容放电时间过长引起的，频率失真和截止失真都是由于超调失真引起的。因此，正确选项应该是B.惰性失真。 答案：B'

# answer = find_answer(txts)
# print(answer)