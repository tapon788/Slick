import xlwings as xl

def export_data():

    app = xl.App()
    wb = app.books[0]
    sheet = wb.sheets[0]
    wb.save(r"C:\parsing\output.xlsx")
    wb.close()
    app.quit()

export_data()