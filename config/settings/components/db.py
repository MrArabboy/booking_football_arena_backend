from config.settings.base import env

DATABASES = {"default": env.db()}
