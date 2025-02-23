from datetime import timedelta

from config.settings.base import env

MINIO_ENDPOINT = env.str("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = env.str("MINIO_ACCESS_KEY", None)
MINIO_SECRET_KEY = env.str("MINIO_SECRET_KEY", None)
MINIO_SECURE = env.bool("MINIO_SECURE", default=False)
MINIO_USE_HTTPS = MINIO_SECURE
MINIO_CONSISTENCY_CHECK_ON_START = False
PUBLIC_BUCKET_NAME = "football_arena_media"
MINIO_PUBLIC_BUCKETS = [
    PUBLIC_BUCKET_NAME,
]
MINIO_BUCKET_CHECK_ON_SAVE = True
MINIO_URL_EXPIRY_HOURS = timedelta(seconds=600)
