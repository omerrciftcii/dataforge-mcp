from mcp.server.fastmcp import FastMCP
import pandas as pd
from sqlalchemy import create_engine
import os

# Import our internal modules
from dataforge.db.introspection import DatabaseInspector
from dataforge.processing.cleaner import DataCleaner
from dataforge.visualization.plotter import DataVisualizer

# Initialize FastMCP server
mcp = FastMCP("DataForge-MCP")

# Setup Database connection (Defaults to our sample SQLite DB)
DB_URL = os.getenv("DATABASE_URL", "sqlite:///sample_company.db")
engine = create_engine(DB_URL)

@mcp.tool()
def get_database_schema() -> str:
    """
    Returns the complete database schema mapping. 
    Use this tool FIRST to understand the available tables and columns before writing any SQL queries.
    """
    inspector = DatabaseInspector(db_url=DB_URL)
    return inspector.get_schema_map()

@mcp.tool()
def analyze_sql_data(query: str) -> str:
    """
    Executes a SQL query, cleans the resulting data automatically (handles missing values), 
    and returns a statistical summary of the dataset.
    Always pass a valid SQL query based on the schema.
    """
    try:
        # Execute SQL and load into Pandas
        df = pd.read_sql(query, engine)
        
        if df.empty:
            return "Query executed successfully, but returned no data."

        # Clean and process data
        cleaner = DataCleaner(df)
        cleaned_df = cleaner.clean_data()
        
        # Ensure output directory exists
        if not os.path.exists("output"):
            os.makedirs("output")
            
        # Save to a temporary CSV so the visualizer tool can access the latest query results
        cleaned_df.to_csv("output/latest_query_results.csv", index=False)

        return f"Data successfully extracted and cleaned. Here is the statistical summary:\n{cleaner.get_summary_stats()}"
    except Exception as e:
        return f"Error executing SQL query: {str(e)}"

@mcp.tool()
def generate_chart(column_name: str) -> str:
    """
    Generates a visualization chart for a specific column from the latest SQL query results.
    Always use analyze_sql_data tool first before calling this tool.
    """
    try:
        # Load the latest queried data
        if not os.path.exists("output/latest_query_results.csv"):
            return "Error: No data available. Please run analyze_sql_data first."
            
        df = pd.read_csv("output/latest_query_results.csv")
        
        # Generate plot using our Plotter module
        visualizer = DataVisualizer(df, output_dir="output")
        file_path = visualizer.plot_column_distribution(column_name)
        
        return f"Success! Chart generated and saved securely to: {file_path}"
    except Exception as e:
        return f"Error generating chart: {str(e)}"

if __name__ == "__main__":
    # Start the MCP server
    print("Starting DataForge-MCP Server...")
    mcp.run()