import openpyxl

class RouteExcelReader:

    @staticmethod
    def read(file):
        workbook = openpyxl.load_workbook(file)
        sheet = workbook.active
        headers = [cell.value for cell in sheet[1]]

        rows = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            rows.append(dict(zip(headers, row)))

        return rows, len(rows)