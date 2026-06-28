# scripts/test_redis.py
import sys
from pathlib import Path

# اضافه کردن مسیر ریشه پروژه به sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.cache.redis_client import redis_client

redis_client.set("hello", "world")
print(redis_client.get("hello"))