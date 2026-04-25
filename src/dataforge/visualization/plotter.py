import pandas as pd
import matplotlib.pyplot as plt
import os

class DataVisualizer:
    def __init__(self, df: pd.DataFrame, output_dir: str = "output"):
        """
        Initializes the visualizer with a Pandas DataFrame and an output directory.
        Creates the output directory if it doesn't exist.
        """
        self.df = df
        self.output_dir = output_dir
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def plot_column_distribution(self, column_name: str) -> str:
        """
        Generates a bar chart for categorical data or a histogram for numeric data.
        Saves the plot as a PNG file and returns the relative file path.
        """
        if column_name not in self.df.columns:
            raise ValueError(f"Column '{column_name}' not found in the dataset.")

        # Create a new figure
        plt.figure(figsize=(10, 6))

        # Check if the column is numeric or categorical
        if pd.api.types.is_numeric_dtype(self.df[column_name]):
            # Plot Histogram for numbers (e.g., age, price)
            self.df[column_name].plot(kind='hist', bins=20, color='skyblue', edgecolor='black')
            plt.title(f'Distribution of {column_name.capitalize()}')
            plt.ylabel('Frequency')
            plt.xlabel(column_name.capitalize())
        else:
            # Plot Bar Chart for text/categories (e.g., country, category)
            # Only take the top 10 categories to avoid messy charts
            value_counts = self.df[column_name].value_counts().head(10)
            value_counts.plot(kind='bar', color='coral', edgecolor='black')
            plt.title(f'Top 10 Categories in {column_name.capitalize()}')
            plt.ylabel('Count')
            plt.xlabel(column_name.capitalize())
            plt.xticks(rotation=45, ha='right')

        # Adjust layout to prevent clipping of labels
        plt.tight_layout()
        
        # Save the plot securely
        file_path = os.path.join(self.output_dir, f"{column_name}_chart.png")
        plt.savefig(file_path)
        plt.close() # Close the plot to free memory
        
        return file_path

if __name__ == "__main__":
    # Test block to verify our visualizer
    print("Testing Data Visualization Module...")
    
    # Create some dummy data
    data = {
        'category': ['Electronics', 'Clothing', 'Clothing', 'Toys', 'Electronics', 'Electronics', 'Sports'],
        'price': [299.99, 45.50, 55.00, 15.99, 899.00, 150.00, 120.50]
    }
    df_test = pd.DataFrame(data)
    
    visualizer = DataVisualizer(df_test)
    
    # 1. Test categorical plot
    cat_path = visualizer.plot_column_distribution('category')
    print(f"Success! Categorical chart saved to: {cat_path}")
    
    # 2. Test numeric plot
    num_path = visualizer.plot_column_distribution('price')
    print(f"Success! Numeric chart saved to: {num_path}")