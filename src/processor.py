import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from deep_translator import GoogleTranslator
from pathlib import Path

class DataProcessor:
    def __init__(self, df):
        self.df = pd.DataFrame(df)

    def clean(self):
        self.drop_nulls()
        self.clean_product_name()
        self.clean_price()
        return self.df
    
    # Drop rows with a null value in any column
    def drop_nulls(self):
        self.df = self.df.dropna(how='any')

    # Translate and strip name of the product
    def clean_product_name(self):
        self.df['product_name'] = self.df['product_name'].str.strip()
        self.df['product_name'] = self.df['product_name'].apply(self.translate_es_to_en)
    
    def translate_es_to_en(self, text):
        if pd.notna(text):
            try:
                return GoogleTranslator(source='es', target='en').translate(text)
            except:
                return text
        return text
    
    # Transform price to work with it as a float number
    def clean_price(self):
        self.df['price'] = (self.df['price']
                        .str.replace('€', '', regex=False)
                        .str.replace('.', '', regex=False)
                        .str.replace(',', '.', regex=False)
                        .str.strip())
        
        self.df['price'] = pd.to_numeric(self.df['price'], errors='coerce').dropna()

    def save_to_csv(self, keyword='nike'):
        kw = keyword.strip().replace(" ", "_")
        file_name = kw + ".csv"

        base_dir = Path(__file__).parent.parent
        file_path = base_dir / "data" / file_name
        self.df.to_csv(file_path, index=False)