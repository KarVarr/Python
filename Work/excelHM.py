import openpyxl

fn = "HM.xlsx"

book = openpyxl.open(fn)
sheet = book.active

capitals = ['IDs','Title','Color','Material','Description','Concept','Photos']
sheet.insert_cols(1, amount=len(capitals))

for i, capital in enumerate(capitals, start=1):
    sheet.cell(row=1, column=i, value=capital)



book.save("HM_updated.xlsx")
