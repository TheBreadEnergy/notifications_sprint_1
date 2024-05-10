class ConnectionIsNotEstablishedException(Exception):
    def __init__(self, message: str = "Соединение с брокером сообщений не установлено"):
        super().__init__(message)
