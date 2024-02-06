AUTH_USER_MODEL = "movies.User"
AUTHENTICATION_BACKENDS = [
    "movies.backends.CustomBackend",
]
