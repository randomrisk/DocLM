import time
import openai
import logging

logger = logging.getLogger(__name__)


def get_summary(api_key: str, context: str, model: str):
    try:
        start_time = time.time()

        prompt = f"""Write a concise summary of the following:

                {context}

                CONCISE SUMMARY IN SAME LANGUAGE:"""

        if model == 'text-curie-001':
            response = openai.Completion.create(
                api_key=api_key,
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
                api_key=api_key,
                model="gpt-3.5-turbo",
                max_tokens=2000,
                messages=[{'role': "system", 'content': "You are a helpful assistant."},
                          {'role': "user", 'content': prompt}],
            )
            answer = response.choices[0].message.content.strip()
        else:
            return 'summary', None
        process_time = round(time.time() - start_time, 2)
        logger.info(f"summary time:{process_time}")
        return 'summary', answer
    except Exception as e:
        logger.exception(f"qa error {e}")
        return 'summary', None


def get_questions(api_key: str, context: str, model: str):
    try:
        start_time = time.time()

        prompt = f"""Ask 5 questions about the context below in the same language:

                    {context}

                    QUESTIONS:"""

        if model == 'text-curie-001':
            response = openai.Completion.create(
                api_key=api_key,
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
                api_key=api_key,
                model="gpt-3.5-turbo",
                max_tokens=500,
                messages=[{'role': "system", 'content': "You are a helpful assistant."},
                          {'role': "user", 'content': prompt}],
            )
            answer = response.choices[0].message.content.strip()
        else:
            return 'questions', None
        process_time = round(time.time() - start_time, 2)
        logger.info(f"questions time:{process_time}")
        return 'questions', answer
    except Exception as e:
        logger.exception(f"qa error {e}")
        return 'questions', None
