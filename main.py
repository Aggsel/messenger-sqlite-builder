import os
from dotenv import load_dotenv
from dbbuilder import DatabaseBuilder

def main():
    load_dotenv()
    folder_location = os.getenv("CONVERSATION_PATH")
    db_name = os.getenv("DATABASE_NAME")
    db_builder = DatabaseBuilder(folder_location, db_name=db_name)

if __name__ == "__main__":
    main()