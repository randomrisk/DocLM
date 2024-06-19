import random
import time
import openai
import logging

import env

logger = logging.getLogger(__name__)

prompts = {
    'ribao': '根据我提供的工作内容，用中文帮我写一篇工作日报，尽量详细，用markdown格式，下面是我的工作内容。',
    'zhoubao': '根据我提供的工作内容，用中文帮我写一份工作周报，尽量详细，用markdown格式，下面是我本周的工作内容。',
    'yuebao': '根据我提供的工作内容，用中文帮我写一份工作月报，尽量详细，用markdown格式，下面是我本月的工作内容。',
    'okr': '根据我提供的内容，用中文帮我写一份OKR，尽量详细，要有量化指标，用markdown格式，下面是我提供的内容。',
    'email': '根据我提供的内容，用中文帮我写一封邮件，格式尽量标准，下面是我提供的内容。',
    'askforleave': '根据下面的内容，用中文帮我写一个请假条，格式尽量标准。',
    'check': '找出下面文本中的语法错误，并给出修改结果。',
    'retouch': '对下面的文本润色，用地道的表达方式。',
    'read': '用浅显易懂的中文解释下面的内容。',
    'ce': '你是一个语言学家，把下面的句子翻译成地道的英文，不要遗漏内容，也不要有多余的内容。',
    'ec': '你是一个语言学家，把下面的句子翻译成地道的中文，不要遗漏内容，也不要有多余的内容。',
    'eq': '用中文高情商回复下面的问题。',
    'guo': '根据下面提供的内容，用中文写一份推卸责任的例子，要做到让别人信服。',
    'thumbup': '根据下面提供的内容，用中文写一份夸人的例子。',
    'emoji': '将下面的内容翻译成emoji表情符号。除了表情符号，不要回复其他的内容。',
    'dream': '下面是我做的梦的内容。帮我分析一下并给出建议。',
    'word': '我想让你充当一名词源学家。我会给你一个词，你要研究这个词的起源，追溯它的古老根源。如果可以的话，你还应提供关于该词的含义如何随时间变化的信息。',
    'biology': '我想让你充当一名生物学家。我会给你一个生物的名称，你要给我详细的介绍一下这种生物。',
    'redbook': '根据下面的内容，写一份小红书风格的文案。',
    'meituan': '根据下面的内容，写一份美团/大众点评风格的文案。',
    'taobao': '根据下面的内容，写一份商品评价。',
    'terminal': '你是一个python解释器，我把代码给你，你执行代码并返回结果，不要包含多余的内容，不要写解释。',
    'python': '你是一个Python专家，请帮我用Python写一个函数，实现我需要的功能，下面是我需要的功能。',
    'regular': '你是一个正则表达式生成器，根据我提供的内容相应的正则表达式，不要包含多余的内容，不要写解释。',
    'name-people': '你是一个文学家，根据下面的内容生成5个中文名字，名字要好听且富有诗意。',
    'name-company': '你是一个文学家，根据下面的内容生成5个中文公司名字，名字要符合公司业务。',
    'public-relations': '你是一个公共关系专家，针对下面提供的内容写一份公关声明，挽救企业形象，申明要体现以下几点：承认错误，给出补救措施，态度谦卑，突出消费者的重要性，给人们留下好印象。'
}


def get_answer_with_role(question: str, role: str):
    try:
        start_time = time.time()

        response = openai.ChatCompletion.create(
            api_key=random.choice(env.OPENAI_KEYS),
            model="gpt-3.5-turbo",
            messages=[{'role': "system", 'content': prompts.get(role)},
                      {'role': "user", 'content': question}],
            temperature=0.1,
            max_tokens=1800,
            stream=True
        )

        for chunk in response:
            # print(chunk['choices'][0]['delta'].get('content', ''))
            yield chunk['choices'][0]['delta'].get('content', '')

        process_time = round(time.time() - start_time, 2)

        logger.info(f"qa time:{process_time} question:{question}")
    except Exception as e:
        logger.exception(f"qa error {e}")
        yield None


def get_answer_with_context(question: str, context: str, model: str):
    try:
        start_time = time.time()

        prompt = f"""基于下面上下文的内容回答下面的问题，使用中文回答，如果答案包含是格式化的代码或者文本，使用Markdown格式。
            如果根据提上下文内容无法回答问题，就使用你自己的知识编写一个答案。

            上下文: {context}

            问题: {question}
            
            """

        response = openai.ChatCompletion.create(
            api_key=random.choice(env.OPENAI_KEYS),
            model="gpt-3.5-turbo",
            messages=[{'role': "system", 'content': "You are a helpful assistant."},
                      {'role': "user", 'content': prompt}],
            temperature=0.3,
            stream=True
        )

        for chunk in response:
            # print(chunk['choices'][0]['delta'].get('content', ''))
            yield chunk['choices'][0]['delta'].get('content', '')

        process_time = round(time.time() - start_time, 2)

        logger.info(f"qa time:{process_time} question:{question}")
    except Exception as e:
        logger.exception(f"qa error {e}")
        yield None
