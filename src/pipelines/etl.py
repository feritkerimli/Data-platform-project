import sys
sys.path.append(r'C:\users\hp\desktop\farid\projects\praktika\data-platform-zip')
from src.ingestion.bronze_load import bronze_load
from src.ingestion.silver_load import silver_load
from src.ingestion.gold_load import gold_load
from src.ingestion.postgres_load import postgres_load
if __name__ == "__main__":
    bronze_load()
    silver_load()
    gold_load()
    postgres_load()
