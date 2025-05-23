from sqlalchemy import inspect
from database import engine

def check_schema():
    inspector = inspect(engine)
    
    print("\nDatabase Schema Information:")
    print("-" * 30)
    
    # Get all table names
    tables = inspector.get_table_names()
    print(f"\nTables found: {tables}")
    
    for table in tables:
        print(f"\nTable: {table}")
        print("Columns:")
        for column in inspector.get_columns(table):
            print(f"  - {column['name']}: {column['type']}")
        
        print("Indexes:")
        for index in inspector.get_indexes(table):
            print(f"  - {index['name']}: {index['column_names']}")
            
        print("Foreign Keys:")
        for fk in inspector.get_foreign_keys(table):
            print(f"  - {fk['name']}: {fk['referred_table']}.{fk['referred_columns']} <- {fk['constrained_columns']}")

if __name__ == "__main__":
    check_schema()
