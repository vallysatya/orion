from memory.sqlite_memory import SQLiteMemory

db = SQLiteMemory()

db.set("user_name", "Sriram")

print(db.get("user_name"))

print(db.exists("user_name"))

db.delete("user_name")

print(db.exists("user_name"))
