from captcha.image import ImageCaptcha
import random
import base64
from io import BytesIO


def generate_captcha_image_base64(captchaType):
    # 创建ImageCaptcha对象，并设置一些参数以保证数字相对清晰
    image_captcha = ImageCaptcha(width=200, height=80, font_sizes=[30])
    captcha_text=''
    result = 0
    if 'math' == captchaType:
        # 定义可能用到的运算符列表
        operators = ['+', '-', '*']
        # 随机生成两个在1到20之间的整数
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        # 随机选择一个运算符
        operator = random.choice(operators)
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
            while result <= 0 or result >= 40:
                num1 = random.randint(1, 20)
                num2 = random.randint(1, 20)
                result = num1 - num2
        elif operator == '*':
            result = num1 * num2
            while result <= 0 or result >= 40:
                num1 = random.randint(1, 20)
                num2 = random.randint(1, 20)
                result = num1 * num2
        # 生成验证码文本
        captcha_text = f"{num1} {operator} {num2} = "
    elif 'char' == captchaType:
        list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        for i in range(4):  # 可指定验证码的位数，此处为6位
            captcha_text += list[random.randint(0, 61)]  # 此处62代表list中的元素个数
        result = captcha_text
    # 生成图形验证码
    captcha_image = image_captcha.generate(captcha_text)
    # 将图形验证码转换为字节流
    captcha_image_io = BytesIO(captcha_image.read())
    # 将字节流转换为Base64编码
    captcha_image_base64 = base64.b64encode(captcha_image_io.getvalue()).decode('utf-8')
    return captcha_image_base64, captcha_text, str(result)
