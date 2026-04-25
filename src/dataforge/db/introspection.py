from sqlalchemy import create_engine, inspect
import json

class DatabaseInspector:
    def __init__(self, db_url="sqlite:///sample_company.db"):
        """
        Initializes the inspector with a database URL.
        Defaults to our local test database.
        """
        self.engine = create_engine(db_url)

    def get_schema_map(self):
        """
        Reads the database schema automatically and returns it 
        as a clean, LLM-friendly JSON string.
        """
        inspector = inspect(self.engine)
        schema_map = {}

        # Loop through all tables in the database
        for table_name in inspector.get_table_names():
            columns = []
            # Loop through all columns in each table
            for column in inspector.get_columns(table_name):
                # Format: "column_name (Data_Type)"
                col_info = f"{column['name']} ({str(column['type'])})"
                
                # Highlight primary keys for the LLM
                if column.get('primary_key'):
                    col_info += " [PK]"
                    
                columns.append(col_info)
            
            schema_map[table_name] = columns

        return json.dumps(schema_map, indent=2)

if __name__ == "__main__":
    # Test block to verify if introspection works
    print("Testing Database Introspection...")
    try:
        inspector = DatabaseInspector()
        schema = inspector.get_schema_map()
        print("Successfully extracted Schema Map for the LLM:\n")
        print(schema)
    except Exception as e:
        print(f"Error connecting to database: {e}")