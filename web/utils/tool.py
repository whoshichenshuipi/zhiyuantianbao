from itsdangerous import URLSafeTimedSerializer


def convert_to_camel_case(snake_str):
    words = snake_str.split('_')
    return words[0] + ''.join(word.title() for word in words[1:])


def convert_to_camel_case_upper(snake_str):
    words = snake_str.split('_')
    return ''.join(word.title() for word in words[0:])


# 生成Token的函数
def generate_token(user_id, secret_key):
    serializer = URLSafeTimedSerializer(secret_key)
    token = serializer.dumps({'user_id': user_id})
    return token


# 验证Token的函数
def verify_token(token, secret_key, expiration=3600):
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        data = serializer.loads(token, max_age=expiration)
        return data['user_id']
    except:
        return None