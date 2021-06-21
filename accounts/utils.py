import africastalking
import random

username = "dnz"
api_key = "b8dc628ebf993960e1ed3db79a9f1bb24520969fbd02d84536b92123c405902c"
africastalking.initialize(username, api_key)

sms = africastalking.SMS


def send_sms(otp, phone_number):
    message = f"Your otp code is {otp}"
    response = sms.send(message, [phone_number])
    return response


def generate_code(length: int):
    val = "123456789qwertyuiplkjhgfdsazxcvbnm".upper()
    v = ""
    for x in range(length):
        v += val[random.randint(0, len(val) - 1)]

    return v


def blur_phone_number(phone_number: str):
    phone_number = list(phone_number)
    for x in range(7, 11, 1):
        phone_number[x] = "X"

    return "".join(phone_number)
