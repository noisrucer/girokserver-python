import random
import string


def generate_verification_code(token_len=6):
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(token_len))
