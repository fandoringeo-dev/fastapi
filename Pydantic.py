from pydantic import BaseModel


class Message(BaseModel):
    id: int
    content: str

# Пример использования
message = Message(id=1, content="Hello, Pydantic!")
print(message)  # Вывод: id=1 content='Hello, Pydantic!'

#======================================================================================================================================

'Метод model_dump()'

'''Этот метод преобразует объект Pydantic в Python-словарь (dict). 
Он полезен, когда нужно получить данные модели в виде словаря для дальнейшей обработки в коде.'''

message.model_dump(*, include=None, exclude=None, by_alias=False, exclude_unset=False, exclude_defaults=False, exclude_none=False) -> dict

include: #Указывает, какие поля включить в результирующий словарь (множество, список или словарь с именами полей).
exclude: #Указывает, какие поля исключить из результирующего словаря.
by_alias: #Если True, ключи словаря будут использовать псевдонимы (алиасы), заданные в модели (например, если в модели есть alias для поля).
exclude_unset: #Если True, исключаются поля, которые не были явно установлены (например, если значение осталось значением по умолчанию).
exclude_defaults: #Если True, исключаются поля, значения которых совпадают со значениями по умолчанию, определёнными в модели.
exclude_none: #Если True, исключаются поля со значением None.

#======================================================================================================================================

'Метод model_dump_json()'
#Этот метод сериализует объект Pydantic в JSON-строку. 
#Он полезен, когда нужно получить данные в формате JSON для отправки по сети или сохранения

print(message.model_dump_json())  # Сериализация в JSON: {"id": 1, "content": "Hello, Pydantic!"}

message.model_dump_json(*, include=None, exclude=None, by_alias=False, exclude_unset=False, exclude_defaults=False, exclude_none=False, indent=None) -> str
#Те же, что и у model_dump(): include, exclude, by_alias, exclude_unset, exclude_defaults, exclude_none.
indent: #Указывает отступ для форматирования JSON-строки (например, indent=2 для читаемого формата).

#======================================================================================================================================

'Специализированные типы Pydantic'
EmailStr: #Проверяет, что строка — валидный email (требуется pip install email-validator).
HttpUrl: #Проверяет, что строка — валидный URL.
PositiveInt: #Проверяет, что целое число положительное.
NonNegativeInt: #Проверяет, что целое число не отрицательное.
NegativeFloat: #Проверяет, что число с плавающей точкой отрицательное.
constr: #Ограничивает строки (например, по длине или регулярному выражению).
conint: #Ограничивает целые числа (например, по диапазону).


#Пример
from pydantic import BaseModel, EmailStr, HttpUrl, PositiveInt

class User(BaseModel):
    email: EmailStr
    website: HttpUrl
    age: PositiveInt

#======================================================================================================================================

'Вложенные модели'
#Модели могут содержать другие модели, что полезно для сложных структур данных:

from pydantic import BaseModel


class Author(BaseModel):
    name: str
    email: EmailStr


class Message(BaseModel):
    id: int
    content: str
    author: Author  # Вложенная модель

message = Message(
    id=1,
    content="Hello",
    author=Author(name="Alice", email="alice@example.com")
)

#======================================================================================================================================
from pydantic import Field

'Валидация через Field'

'''Модуль pydantic.Field позволяет задавать ограничения для полей, такие как длина строки, диапазон чисел, регулярные выражения и т.д. 
По умолчанию все поля в модели обязательные.'''

default: #Значение по умолчанию для поля, если оно не указано.
Field(default="some_value")
#Делает поле необязательным.

default_factory: #Функция, вызываемая для создания значения по умолчанию (для динамических значений, например, UUID).
Field(default_factory=lambda: uuid4())
#Делает поле необязательным.

title: #Заголовок поля для документации (например, OpenAPI).
Field(..., title="User ID")

description: #Описание поля для документации.
Field(..., description="Unique identifier for a user")

const: #Указывает, что поле является константой и всегда имеет значение из default.
Field(default="constant_value", const=True)

gt: #Ограничение "больше" для числовых полей.
Field(..., gt=0)

ge: #Ограничение "больше или равно" для числовых полей.
Field(..., ge=0)

lt: #Ограничение "меньше" для числовых полей.
Field(..., lt=100)

le: #Ограничение "меньше или равно" для числовых полей.
Field(..., le=100)

multiple_of: #Числовое значение должно быть кратно указанному числу.
Field(..., multiple_of=5)

min_length:# Минимальная длина строки.
Field(..., min_length=3)

max_length: #Максимальная длина строки.
Field(..., max_length=50)

pattern: #Регулярное выражение для валидации строк.
Field(..., pattern=r"^[a-zA-Z0-9]+$")
#Проверяет, что строка соответствует заданному регулярному выражению.

strict: #Включает строгий режим валидации (требует точное соответствие типов).
Field(..., strict=True)

exclude: #Исключает поле из сериализации (например, в model.dict()).
Field(..., exclude=True)

include: #Указывает, включать ли поле в сериализацию (используется редко, обычно с exclude).
Field(..., include=True)

json_schema_extra: #Дополнительные параметры для JSON-схемы (например, для OpenAPI).
Field(..., json_schema_extra={"example": "example_value"})

deprecated: #Помечает поле как устаревшее для документации.
Field(..., deprecated=True)

frozen: #Запрещает изменение значения поля после создания экземпляра.
Field(..., frozen=True)


'Регулярные выражения'

from pydantic import BaseModel, Field

class Article(BaseModel):
    text: str
    slug: str = Field(pattern=r'^[-a-zA-Z0-9_]+$')

# Пример использования:
valid_article = Article(text="Some text", slug="valid-slug_123")
invalid_article = Article(text="Some text", slug="Invalid Slug!") # Ошибка
invalid_article2 = Article(text="Some text", slug=" ") # Ошибка

#======================================================================================================================================


'Кастомная валидация с @field_validator'

from pydantic import BaseModel, Field, field_validator


class Message(BaseModel):
    content: str = Field(min_length=1, max_length=500)

    @field_validator("content")
    @classmethod
    def check_forbidden_words(cls, value):
        forbidden_words = ["spam", "offensive"]
        if any(word in value.lower() for word in forbidden_words):
            raise ValueError("Message contains forbidden words")
        return value

message = Message(content="Hello, world!")  # OK
message = Message(content="This is spam")  # Ошибка: Message contains forbidden words


#Можно валидировать несколько полей одновременно:
class Message(BaseModel):
    id: int
    content: str

    @field_validator("content")
    @classmethod
    def check_content_id_match(cls, value, info):
        if str(info.data.get("id", "")) not in value:
            raise ValueError("Content must contain the ID")
        return value

message = Message(id=1, content="Message 1")  # OK
message = Message(id=1, content="No ID here")  # Ошибка: Content must contain the ID

#В Pydantic параметр info в @field_validator предоставляет доступ к данным модели через info.data.

#======================================================================================================================================

'Валидация на уровне модели через @model_validator'

'''В Pydantic декоратор @model_validator используется для валидации на уровне модели, когда нужно проверить взаимосвязь между несколькими полями.
Он позволяет выполнять проверки, учитывающие значения нескольких полей одновременно, до или после стандартной валидации.'''

from pydantic import BaseModel, model_validator

class User(BaseModel):
    name: str
    age: int
    email: str

    @model_validator(mode='after')
    def check_age_and_email(self):
        if self.age < 18 and self.email:
            raise ValueError("Несовершеннолетним нельзя указывать email")
        return self

# Пример использования
data = {"name": "Alice", "age": 16, "email": "alice@example.com"}
try:
    user = User.model_validate(data)
except ValueError as e:
    print(e)  # Выведет: Несовершеннолетним нельзя указывать email

'Режимы валидации:'

mode='before' #— валидация до преобразования данных в типы модели.
mode='after'# — валидация после преобразования (чаще используется).

'''Метод должен возвращать объект (обычно self) или изменённые данные. Для ошибок валидации обычно вызывается ValueError или ValidationError.
Это полезно для сложных проверок, зависящих от нескольких полей, например, согласованности дат или условий между значениями.'''

#======================================================================================================================================

'Кастомные типы с Annotated'
#Pydantic активно использует typing.Annotated для создания кастомных типов с помощью StringConstraints, NumberConstraints и т.д.:

from pydantic import BaseModel
from typing import Annotated
from pydantic.types import StringConstraints

Username = Annotated[str, StringConstraints(min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$")]

class User(BaseModel):
    username: Username

user = User(username="john_doe")  # OK
user = User(username="ab")  # Ошибка: слишком короткое имя


'Валидация чисел с плавающей точкой'
#Для чисел с плавающей точкой можно задавать точность:

from pydantic import BaseModel, Field
from decimal import Decimal

class Product(BaseModel):
    price: Decimal = Field(max_digits=6, decimal_places=2)  # Например, 1234.56

product = Product(price=1234.56)  # OK
product = Product(price=1234567.89)  # Ошибка: слишком много цифр

