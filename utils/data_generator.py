import datetime
import random
import string
from typing import Any
from uuid import uuid4

from faker import Faker

faker = Faker()


class DataGenerator:
    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_int(max_value: int):
        return random.randint(1, max_value)

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)

        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные тестового пользователя для создания через БД"""
        return {
            'id': f'{uuid4()}',
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

    @staticmethod
    def generate_random_movie():
        return {
          "name": f"{faker.word().capitalize()} {faker.word().capitalize()}",
          "imageUrl": "https://dummyimage.com/600x400",
          "price": random.randint(100, 1000),
          "description": f"{faker.word().capitalize()} {faker.word().capitalize()} {faker.word().capitalize()}",
          "location": "SPB",
          "published": True,
          "genreId": 8
        }

    @staticmethod
    def generate_movie_with_existing_name(name: str):
        return {
            "name": name,
            "imageUrl": "https://dummyimage.com/600x400",
            "price": random.randint(100, 1000),
            "description": f"{faker.word().capitalize()} {faker.word().capitalize()} {faker.word().capitalize()}",
            "location": "SPB",
            "published": True,
            "genreId": 8
        }

    @staticmethod
    def generate_movie_with_custom_price(price: Any):
        return {
            "name": f"{faker.word().capitalize()} {faker.word().capitalize()}",
            "imageUrl": "https://dummyimage.com/600x400",
            "price": price,
            "description": f"{faker.word().capitalize()} {faker.word().capitalize()} {faker.word().capitalize()}",
            "location": "SPB",
            "published": True,
            "genreId": 8
        }

