import os
import platform
import signal
from transformers import AutoTokenizer, AutoModel
import readline

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

tokenizer = AutoTokenizer.from_pretrained("/opt/data/private/zyx/chatglm2-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("/opt/data/private/zyx/chatglm2-6b", trust_remote_code=True).cuda()
# 多显卡支持，使用下面两行代替上面一行，将num_gpus改为你实际的显卡数量
from utils import load_model_on_gpus
model = load_model_on_gpus("/opt/data/private/zyx/chatglm2-6b", num_gpus=1)
model = model.eval()

os_name = platform.system()
clear_command = 'cls' if os_name == 'Windows' else 'clear'
stop_stream = False

# 将样例写入
# 1. 单选 多选 自由问答分类

# 单选题给出答案 电流对人体的效应由生理参数和电气参数决定。15～100Hz 正弦交流电流反应阈的通用值为（）。选项 A：1.5mA 选项 B：2mA 选项 C：0.1mA 选项 D：0.5mA
# 多选题给出答案 下列选项中，电力负荷应该为三级负荷的是（）。 选项 A：中断供电将在经济上造成较大损失的负荷 选项 B：中断供电影响重要用电单位正常工作的负荷 选项 C：一般货梯和自动扶梯 选项 D：不属于一级和二级的电力负荷
# 自由问答给出答案 如果一台$p$对磁极的单叠绕组，其元件电阻为$r_a$，电枢电流为$I_a$，若把它改接为单波绕组，并保持支路电流不变。试问电枢电阻和电枢电流变为多少?

def build_prompt(history):
    prompt = "欢迎使用 ChatGLM2-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序"
    for query, response in history:
        prompt += f"\n\n用户：{query}"
        prompt += f"\n\nChatGLM2-6B：{response}"
    return prompt


def signal_handler(signal, frame):
    global stop_stream
    stop_stream = True


def main():
    past_key_values, history = None, []
    global stop_stream
    print("欢迎使用 ChatGLM2-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序")
    while True:
        query = input("\n用户：")
        if query.strip() == "stop":
            break
        if query.strip() == "clear":
            past_key_values, history = None, []
            os.system(clear_command)
            print("欢迎使用 ChatGLM2-6B 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序")
            continue
        print("\nChatGLM：", end="")
        current_length = 0
        for response, history, past_key_values in model.stream_chat(tokenizer, query, history=history,
                                                                    past_key_values=past_key_values,
                                                                    return_past_key_values=True):
            if stop_stream:
                stop_stream = False
                break
            else:
                print(response[current_length:], end="", flush=True)
                current_length = len(response)
        print("")


if __name__ == "__main__":
    main()
