AUTH_USER_MODEL = "notify.User"
AUTHENTICATION_BACKENDS = [
    "notify.backends.CustomBackend",
]
