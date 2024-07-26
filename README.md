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
