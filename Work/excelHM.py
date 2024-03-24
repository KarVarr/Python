import openpyxl
import pandas as pd
import os 

fn = "HM.xlsx"

book = openpyxl.open(fn)
sheet = book.active

capitals = ['IDs','Title','Color','Description','Material','Concept','Photos','',]
sheet.insert_cols(1, amount=len(capitals))


def formula(column):
    # Write formula into the second column
    formula = f"=VLOOKUP(A2, J:S, {column}, FALSE)"
    sheet.cell(row=2, column=column).value = formula

    # Fill the formula down to the last row of data in column A
    for i in range(2, len(column_I_data) + 1):  # Start from row 3 since the formula is already in row 2
        sheet.cell(row=i, column=column).value = "=VLOOKUP(A{}, J:S, {}, FALSE)".format(i,column)


for i in range(1, sheet.max_row + 1):
    value = sheet.cell(row=i, column=10).value
    sheet.cell(row=i, column=1).value = value

# Copy data from column I to a list
column_I_data = [sheet.cell(row=i, column=10).value for i in range(2, sheet.max_row + 1)]

# Sort the data in ascending order
column_I_data.sort()

# Remove duplicates
column_I_data = list(dict.fromkeys(column_I_data))

# Clear existing data in column A
for i in range(1, sheet.max_row + 1):
    sheet.cell(row=i, column=1).value = None

# Write sorted and deduplicated data to column A
for i, value in enumerate(column_I_data, start=1):
    sheet.cell(row=i, column=1).value = value

# Write formula into the second column
# formula = "=VLOOKUP(A2, J:S, 2, FALSE)"
# sheet.cell(row=2, column=2).value = formula

# # Fill the formula down to the last row of data in column A
# for i in range(3, len(column_I_data) + 1):  # Start from row 3 since the formula is already in row 2
#     sheet.cell(row=i, column=2).value = "=VLOOKUP(A{}, J:S, 2, FALSE)".format(i)
formula(2)
formula(3)
formula(4)
formula(5)

for i, capital in enumerate(capitals, start=1):
    sheet.cell(row=1, column=i, value=capital)
# Save the workbook
book.save("HM_updated.xlsx")

