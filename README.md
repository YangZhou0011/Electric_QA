# 电力知识问答大模型
为应对数据稀缺环境下的高知识密度的电力领域知识问答，我们首先考虑建立面向电力领域的完备知识库，随后利用电力领域原始文本以大语言模型生成电力领域相关问答为之后的指令微调进行准备。在测试阶段考虑到大语言模型生成的随机性，在调整温度系数等控制语言模型生成一致的参数外，我们考虑了模型的self-consistency，通过投票选择出模型最置信的结果。
## 整体框架
整体方案框架包括4 个部分，分别是数据构造与增强，指令prompt 构造、监督微调与知识库检索拼接与基于self-consistency 的后处理过程。
## 数据准备
在数据准备阶段，我们考虑电力领域与数学、电学等理工科科目所具有内在的高度一致性，我们通过电力领域关键词收集相关领域教材、行业标准等百余份领域文档，通过OCR技术获取并清洗原始文本，将原始文本合并为蕴含知识较多的文本段，作为原始知识库。并利用知识库，通过prompt 进行领域题目生成。数据生成prompt 如下所示：您将获得文本来构建电力领域相关的问题。TEXT 将用{delimiter}字符分隔。请用中文输出一个包含4 个dict 对象的python 列表，其中每个对象都是一个选择题，每个文本有4个选项，列表的最后一项为该题目答案，格式如下:
```
"question":关于文本的问题&gt;
"option_1":&lt; 问题答案选项&gt;
"option_2": &lt; 问题答案选项&gt;
"option_3": &lt; 问题答案选项&gt;
"option_4": &lt;问题答案选项&gt;
"answer": &lt;答案选项键标签&gt;
你应该告诉我你提出的选项中哪一个是正确的；
通过在"answer"字段中分配相应选项的键标签；
仅需输出由python 构造的问题列表；
若知识不足则返回：文本知识不足。
```
## Prompt 构造与指令微调格式
针对单选题、多选题、问答题指定不同的提示，进行学习。
单选题提示: 你是电力领域的专家，这是一个单项选择题，请逐步分析并从A、B、C、D 四个选项中选出最正确的一个选项,回答选项内容和字母。
多选题提示: 你是电力领域的专家，这是一个多项选择题，请从A、B、C、D 四个选项中选出最正确的几个，回答选项内容与字母。
问答题提示: 你是电力领域的专家，这是一个问答题，请逐步分析获得这个问题的解。
## Lora 微调
为节省微调数据所需的显存占用，我们使用Lora[1]对数据进行指令微调。在我们的方案中，我们设定lora 的学习率为4e-6，lora_rank=16，以微调我们的模型。为最大化利用数据，我们将添加不同prompt 的单选、多选、问答三类题型的数据一同进行训练。
## 知识库召回增强
在模型推理阶段，为缓解模型幻觉和弥补模型知识不足的问题，我们采用了外挂知识库的方式进行改进。知识库采用数据准备阶段得到的文本数据，利用langchain 的文本分割技术构建了数据量为10w+条的知识库。参考In-Context RALM[2]中提出的方法，我们采用了BM25 算法对题目进行知识召回，选取了知识库中最相关的top-k 条知识；然后将知识简单拼接在问题前，并适当添加了prompts 模板。在使用BM25 算法对知识库条目进行召回后，我们得到了题目与召回知识的相关性得分sim，并保存在中间数据文件中。当进行推理时，对于单选题，我们添加了所有召回的知识；对于多选题，我们添加了相关性得分sim 大于90 的知识，从容保证回答更为谨慎。实验结果表明，添加知识后，模型回答的准确率有一定的提升。
## 基于self-consistency[3]的后处理
为保证模型生成的一致性，我们控制问答题具有较低的温度系数，并从生成答案中随机选择。对单选题我们选择生成5 次并选取其中出现次数最多的作为答案、对于多选题，我们对可能出现的每个选项进行技术优先选择出现次数最多的两个选项，对于之后的选项若出现次数为0 则不考虑当前与后续选项，若出现次数与最后选项出现次数的差小于等于1 则添加该选项，直到某个选项出现次数为0。


# Electric Power Q&A LLM
To address the high knowledge density in the power sector under data scarcity conditions, we first consider establishing a comprehensive knowledge base tailored to the power sector. Subsequently, we utilize original texts from the power sector to generate related Q&A pairs using a large language model, preparing for subsequent instruction fine-tuning. During the testing phase, considering the randomness of the large language model generation, besides adjusting parameters such as the temperature coefficient to control consistent generation, we also consider the model's self-consistency, selecting the most trusted results through voting.

## Overall Framework
The overall framework consists of four parts: data construction and enhancement, instruction prompt construction, supervised fine-tuning, and knowledge base retrieval concatenation with self-consistency-based post-processing.

## Data Preparation
In the data preparation stage, considering the inherent high consistency of the power sector with subjects such as mathematics and electrical engineering, we collect over a hundred documents from related fields, including textbooks and industry standards, using power sector keywords. We utilize OCR technology to acquire and clean the original texts, merging them into knowledge-rich text segments as the original knowledge base. This knowledge base is then used to generate domain-specific questions through prompts.

The data generation prompt is as follows:
"You will receive a text to construct questions related to the power sector. The TEXT will be separated by the {delimiter} character. Please output a Python list containing four dict objects in Chinese, where each object is a multiple-choice question with four options, and the last item in the list is the answer to the question. The format is as follows:
``` 
'question': <Question based on the text>
'option_1': <Answer option>
'option_2': <Answer option>
'option_3': <Answer option>
'option_4': <Answer option>
'answer': <Answer option key>
```
You should tell me which of the options you proposed is correct by assigning the corresponding option's key to the 'answer' field; if the knowledge is insufficient, return: Insufficient text knowledge."
## Prompt Construction and Instruction Fine-tuning Format
Different prompts are specified for single-choice, multiple-choice, and Q&A questions to facilitate learning.

Single-choice prompt: You are an expert in the power sector. This is a single-choice question. Please analyze step-by-step and choose the most correct option from A, B, C, and D, and provide the content and letter of the option.
Multiple-choice prompt: You are an expert in the power sector. This is a multiple-choice question. Please choose the most correct options from A, B, C, and D, and provide the content and letters of the options.
Q&A prompt: You are an expert in the power sector. This is a Q&A question. Please analyze step-by-step to get the solution to this question.
## Lora Fine-tuning
To save GPU memory required for fine-tuning, we use Lora [1] for instruction fine-tuning of the data. In our scheme, we set the learning rate of Lora to 4e-6 and lora_rank to 16 to fine-tune our model. To maximize data utilization, we train with single-choice, multiple-choice, and Q&A type data added with different prompts.

## Knowledge Base Retrieval Enhancement
During model inference, to alleviate model hallucinations and compensate for the model's lack of knowledge, we use an external knowledge base. The knowledge base is constructed using text data obtained in the data preparation stage, utilizing LangChain's text splitting technique to create a knowledge base with over 100,000 entries. Referring to the method proposed in In-Context RALM [2], we use the BM25 algorithm for knowledge retrieval, selecting the top-k most relevant knowledge entries from the knowledge base; then, we simply concatenate the knowledge in front of the questions and appropriately add prompt templates. After retrieving the knowledge base entries using the BM25 algorithm, we obtain the relevance score sim between the questions and the retrieved knowledge and save it in an intermediate data file. During inference, for single-choice questions, we add all retrieved knowledge; for multiple-choice questions, we add knowledge with a relevance score sim greater than 90 to ensure cautious answering. Experimental results show that adding knowledge improves the model's answer accuracy.

## Self-consistency-based Post-processing
To ensure the consistency of the model-generated answers, we control the temperature coefficient of Q&A questions to be low and select randomly from the generated answers. For single-choice questions, we generate five times and select the answer that appears most frequently; for multiple-choice questions, we prioritize the top two options with the highest occurrence and if subsequent options have zero occurrences, we do not consider them. If the occurrence difference between the next option and the last option is less than or equal to one, we add that option until an option appears zero times.

References:
Lora
In-Context RALM
Self-consistency
