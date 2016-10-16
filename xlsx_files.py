import xlsxwriter


class XlsxFile:

    def __init__(self, file_name):
        self.file_name = file_name
        self.book = None
        self.sheet = None
        self.row_count = 0

    def create_file(self):
        self.book = xlsxwriter.Workbook(self.file_name + '.xlsx')
        self.sheet = self.book.add_worksheet()

    def write_to_sheet(self, row):
        for i, val in enumerate(row):
            self.sheet.write(self.row_count, i, val)
        self.row_count += 1

    def save_workbook(self):
        self.book.close()
