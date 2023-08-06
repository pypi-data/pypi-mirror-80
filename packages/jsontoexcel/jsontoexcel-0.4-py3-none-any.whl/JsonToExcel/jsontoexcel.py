import sys, json
import xlsxwriter

class JsonToExcel:
    excelbook = None
    excelsheet = {}

    def __init__(self, filename):
        self.excelbook = xlsxwriter.Workbook(filename+".xlsx")

    def createSheet(self, sheetname, jsonData):
        self.excelsheet[sheetname] = self.excelbook.add_worksheet(sheetname)
        data = json.loads(jsonData)

        writeToSheet(self.excelsheet[sheetname], self.excelbook, 0, 1, data, "", 1)
        return self.excelsheet[sheetname]

    def getSheet(self, sheetname):
        return self.excelsheet[sheetname]

    def closeWorkbook(self):
        self.excelbook.close()




def writeToSheet(worksheet, workbook, col, row, data, header, maxRow):

    if type(data) is list:
        xrow = maxRow
        x = ((row, col), maxRow)
        for entry in data:
            x = writeToSheet(worksheet, workbook, col, xrow, entry, header, maxRow)
            maxRow = max(maxRow, x[1])
            xrow = maxRow+1
        return x[0], maxRow

    elif type(data) is dict:
        x = ((row, col-1), row)
        for key, value in data.items():
            x = writeToSheet(worksheet, workbook, x[0][1] + 1, row, value, header + "_" + key, row)
            maxRow = max(maxRow, x[1])
        return x[0], maxRow

    else:
        bold = workbook.add_format({'bold': True, 'bg_color': 'yellow'})
        worksheet.write(0, col, header, bold)
        worksheet.write(row, col, data)
        return (row, col), row
