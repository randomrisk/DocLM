import time
import openai
import logging

logger = logging.getLogger(__name__)


class GPT(object):

    @classmethod
    def init_key(cls, api_key: str):
        openai.api_key = api_key

    @staticmethod
    def get_answer(question: str, content: str, model: str):
        try:
            start_time = time.time()

            prompt = f"""Answer the question based on the context below. Use the same language as question.
                If the question cannot be answered using the information provided answer with "I don't know".

                Context: {content}

                Question: {question}

                Answer: """
            # prompt = f'''基于下面的内容用简洁的语言回答问题。\n
            #     {content}\n\n
            #     问题: {question}\n
            #     答案:
            # '''
            if model == 'text-curie-001':
                response = openai.Completion.create(
                    model="text-curie-001",
                    prompt=prompt,
                    temperature=0.9,
                    max_tokens=800,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                answer = response.choices[0].text.strip()
            elif model == 'gpt-3.5-turbo':

                # prompt = f'''Write a comprehensive answer in Chinese
                #     for the question below solely based on the provided context.
                #     If the context is insufficient,
                #     'reply "I cannot answer". '
                #     Answer in an unbiased, balanced, and scientific tone.
                #     Use Markdown for formatting code or text.\n\n
                #     {content}\n\n
                #     Question: {question}\n
                #     Answer: '''
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{'role': "system", 'content': "You are a helpful assistant."},
                              {'role': "user", 'content': prompt}],
                )
                answer = response.choices[0].message.content.strip()
            else:
                return ''
            process_time = round(time.time() - start_time, 2)
            logger.info(f"qa time:{process_time} question:{question}")
            return answer
        except Exception as e:
            logger.exception(f"qa error {e}")
            return None

    @staticmethod
    def get_summary(context: str, model: str):
        try:
            start_time = time.time()

            prompt = f"""Write a concise summary of the following:

                {context}

                CONCISE SUMMARY IN SAME LANGUAGE:"""

            if model == 'text-curie-001':
                response = openai.Completion.create(
                    model="text-curie-001",
                    prompt=prompt,
                    temperature=0.9,
                    max_tokens=800,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                answer = response.choices[0].text.strip()
            elif model == 'gpt-3.5-turbo':
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    max_tokens=2000,
                    messages=[{'role': "system", 'content': "You are a helpful assistant."},
                              {'role': "user", 'content': prompt}],
                )
                answer = response.choices[0].message.content.strip()
            else:
                return ''
            process_time = round(time.time() - start_time, 2)
            logger.info(f"summary time:{process_time}")
            return answer
        except Exception as e:
            logger.exception(f"qa error {e}")
            return None

    @staticmethod
    def get_questions(context: str, model: str):
        try:
            start_time = time.time()

            prompt = f"""Ask 5 questions about the context below in the same language:

                    {context}

                    QUESTIONS:"""

            if model == 'text-curie-001':
                response = openai.Completion.create(
                    model="text-curie-001",
                    prompt=prompt,
                    temperature=0.9,
                    max_tokens=800,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                answer = response.choices[0].text.strip()
            elif model == 'gpt-3.5-turbo':
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    max_tokens=500,
                    messages=[{'role': "system", 'content': "You are a helpful assistant."},
                              {'role': "user", 'content': prompt}],
                )
                answer = response.choices[0].message.content.strip()
            else:
                return ''
            process_time = round(time.time() - start_time, 2)
            logger.info(f"questions time:{process_time}")
            return answer
        except Exception as e:
            logger.exception(f"qa error {e}")
            return None
