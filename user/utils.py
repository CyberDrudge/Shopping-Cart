import random
import string


class CodeGenerator:
    def code(self, size=4, use_chars=None):
        if use_chars:
            chars = string.ascii_letters
        else:
            chars = string.digits
        code = ''.join(random.choice(chars) for _ in range(size))
        return code
