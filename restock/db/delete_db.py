from restock.db.mongo_util import DBPoolManager
from restock.config import DB

print("Dropping database")

try:
    db_pool = DBPoolManager()
    db_pool.delete_database()
except Exception as ex:
    print(ex)

print("COMPLETE!")
