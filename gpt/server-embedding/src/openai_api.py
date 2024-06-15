import time
import openai
import logging
from typing import List

logger = logging.getLogger(__name__)


class GPT(object):

    @classmethod
    def init_key(cls, api_key: str):
        openai.api_key = api_key

    @staticmethod
    def get_embedding(text: List[str], model="text-embedding-ada-002"):
        try:
            start_time = time.time()
            response = openai.Embedding.create(input=text, model=model)
            embedding = [i["embedding"] for i in response["data"]]
            process_time = round(time.time() - start_time, 2)
            logger.info(f"embedding time:{process_time} text:{len(text)}")
            return embedding
        except Exception as e:
            logger.exception(f"embedding error")
            return None
