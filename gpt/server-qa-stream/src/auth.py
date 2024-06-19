import env
import logging
from jose import JWTError, jwt
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def create_access_token(data: dict) -> str:
    """创建带exp字段的JWT字符串"""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=env.ACCESS_TOKEN_EXPIRE_DAYS)
    expire = int(expire.timestamp())
    to_encode.update({"exp": expire})  # datetime.datetime(2023, 1, 18, 8, 14, 02, 453944)
    # ACCESS_TOKEN_SECRET_KEY对声明集进行签名的密钥
    # jwt.encode()对声明集进行编码并返回 JWT 字符串。
    encoded_jwt = jwt.encode(to_encode, env.ACCESS_TOKEN_SECRET_KEY, algorithm=env.ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt


def valid_access_token(token: str) -> (bool, dict):
    """
    解密JWT，即验证JWT字符串的SIGNATURE签名并返回claims(也称PAYLOAD)的信息
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, env.ACCESS_TOKEN_SECRET_KEY, algorithms=[env.ACCESS_TOKEN_ALGORITHM])
        user = payload.get("uid")
        exp = payload.get("exp")
        now = int(datetime.now().timestamp())
        if user and exp > now:
            return True, {'uid': user}
        return False, {}
    except Exception as e:
        logger.info(f'valid_access_token error {e}')
        return False, {}


def encode_chat_data(data: dict) -> str:
    """创建带exp字段的JWT字符串"""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(seconds=env.CHAT_DATA_EXPIRE_SECONDS)
    expire = int(expire.timestamp())
    to_encode.update({"exp": expire})  # datetime.datetime(2023, 1, 18, 8, 14, 02, 453944)
    # ACCESS_TOKEN_SECRET_KEY对声明集进行签名的密钥
    # jwt.encode()对声明集进行编码并返回 JWT 字符串。
    encoded_jwt = jwt.encode(to_encode, env.ACCESS_TOKEN_SECRET_KEY, algorithm=env.ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt


def decode_chat_data(token: str) -> (bool, dict):
    """
    解密JWT，即验证JWT字符串的SIGNATURE签名并返回claims(也称PAYLOAD)的信息
    """
    try:
        payload = jwt.decode(token, env.ACCESS_TOKEN_SECRET_KEY, algorithms=[env.ACCESS_TOKEN_ALGORITHM])
        exp = payload.get("exp")
        now = int(datetime.now().timestamp())
        if exp > now:
            return True, payload
        return False, {}
    except Exception as e:
        logger.info(f'decode_chat_data error {e}')
        return False, {}
