from enum import Enum


class APIMessage(Enum):
    UNAUTHORIZED = "Ошибка авторизации"
    FORBIDDEN = "Недостаточно прав"
    BAD_REQUEST = "Ошибка запроса"
    NOT_FOUND = "Данные не найдены"

    ACTION_ERROR = "Ошибка действия!"
    ADD_DATA_ERROR = "Ошибка при добавлении"

    EMAIL_IS_CONFIRMED = "Эта почта подтверждена"
    EMAIL_IS_UNSUBSCRIBED = "Эта почта уже отписана от рассылок"
    USER_DOESNT_EXIST = "Пользователя с таким email нет"
