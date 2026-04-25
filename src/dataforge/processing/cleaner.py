import pandas as pd
import numpy as np

class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        """
        Initializes the cleaner with a raw Pandas DataFrame.
        """
        # Create a copy to avoid SettingWithCopyWarning
        self.df = df.copy()

    def clean_data(self) -> pd.DataFrame:
        """
        Performs essential data engineering tasks:
        1. Standardizes column names.
        2. Fills missing numeric values with the median.
        3. Fills missing categorical values with 'Unknown'.
        """
        # 1. Standardize column names (lowercase, replace spaces with underscores)
        self.df.columns = [str(col).strip().lower().replace(' ', '_') for col in self.df.columns]

        # 2. Handle missing values automatically based on data type
        for col in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                # Fill numeric NaNs with median to avoid outlier skew
                median_val = self.df[col].median()
                # If the entire column is NaN, fill with 0
                if pd.isna(median_val):
                    median_val = 0
                self.df[col] = self.df[col].fillna(median_val)
            else:
                # Fill categorical or text NaNs with 'Unknown'
                self.df[col] = self.df[col].fillna('Unknown')

        return self.df

    def get_summary_stats(self) -> str:
        """
        Returns a statistical summary (min, max, mean, count) of the dataset 
        formatted as JSON for the LLM to easily understand.
        """
        # include='all' ensures we get stats for both numeric and text columns
        return self.df.describe(include='all').to_json()

if __name__ == "__main__":
    # Test block to simulate "Dirty Data" and verify our cleaner
    print("Testing Data Preprocessing Module...")
    
    # Intentionally dirty data with missing values (NaN) and bad column names
    dirty_data = {
        'Customer Name ': ['Alice', 'Bob', np.nan, 'David'],
        ' Age': [25, np.nan, 30, 45],
        'Total Spend': [150.5, 200.0, np.nan, 400.0]
    }
    df_dirty = pd.DataFrame(dirty_data)
    
    print("\n--- Original Dirty Data ---")
    print(df_dirty)

    # Run the cleaner
    cleaner = DataCleaner(df_dirty)
    df_cleaned = cleaner.clean_data()
    
    print("\n--- Cleaned Data ---")
    print(df_cleaned)
    
    print("\n--- Summary Stats for LLM ---")
    print(cleaner.get_summary_stats())