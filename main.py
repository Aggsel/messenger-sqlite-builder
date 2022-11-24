from dotenv import load_dotenv
from dbbuilder import DatabaseBuilder

def main():
    load_dotenv()
    db_builder = DatabaseBuilder()
    db_builder.create_database(overwrite=True)

if __name__ == "__main__":
    main()