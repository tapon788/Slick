__author__ = 'Tapon'

import xlsxwriter
import os,sys



class MakeExcelFile:

    def __init__(self, path):
        self.wb = xlsxwriter.Workbook(path)
        self.cell_format_header = self.wb.add_format({'bold': True, 'font_color': 'white','bg_color': '#7BB433','border':1,'border_color':'white'})
        self.cell_format_nok = self.wb.add_format({'bold': True, 'font_color': 'white','bg_color': 'red','border':1,'border_color':'yellow'})

    def createsheet(self, sheetname, data):

        ws = self.wb.add_worksheet(sheetname)
        row = -1

        #print(data)

        for dict in data:

            row += 1
            col = -1
            for key, val in dict.items():
                col += 1
                if row == 0:
                    #ws.write(row, col, key,self.cell_format_header)
                    ws.write(row, col, key,self.cell_format_header)
                else:
                    if val:
                        if val.find('NOK') >= 0:

                            ws.write(row, col, val, self.cell_format_nok)
                        else:

                            ws.write(row, col, val)
                    else:
                        ws.write(row, col, val,self.cell_format_nok)
    def close(self):
        self.wb.close()
