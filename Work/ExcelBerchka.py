import pandas as pd
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

df = pd.read_excel("C:/Users/karen.vardanyan/Desktop/BershkaTruck1.xlsx")

print(df.values)