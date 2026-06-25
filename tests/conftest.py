# tests/conftest.py
import sys
from pathlib import Path

# اضافه کردن مسیر ریشه پروژه به sys.path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# حالا هم 'main' و هم 'app' قابل import هستند