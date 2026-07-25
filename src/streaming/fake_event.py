import sys
import time
import threading

sys.path.append(r'C:\users\hp\desktop\farid\projects\praktika\data-platform-zip')

from src.ingestion.bronze_load import bronze_load
from src.ingestion.silver_load import silver_load
from src.ingestion.silver_load_fake_orders import silver_load_fake_orders
from src.ingestion.gold_load import gold_load
from src.ingestion.postgres_load import postgres_load


def fake_order_stream():
    while True:
        silver_load_fake_orders()
        gold_load()
        postgres_load()

        print("Cycle finished...")
        time.sleep(5)   


if __name__ == "__main__":

    threading.Thread(
        target=fake_order_stream,
        daemon=True
    ).start()
    

    
    while True:
        time.sleep(1)