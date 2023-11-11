from random import randint


def generate_verification_token():
    """Создание токена для проверки e-mail, без него user is not_active=False, и он не может войти в систему"""
    token = ''.join(str(randint(0, 9)) for _ in range(20))
    return token
