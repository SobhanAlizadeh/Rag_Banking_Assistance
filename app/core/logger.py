import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
logging.FileHandler("logs/app.log")
logger=logging.getLogger("rag_app")