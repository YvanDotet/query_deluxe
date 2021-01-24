from odoo import models


class QueryDeluxeXlsx(models.AbstractModel):
    _name = "report.query_deluxe.query_deluxe_xlsx"
    _inherit = "report.query_deluxe.abstract"
    _description = "Query Deluxe XLSX Report"

    def generate_xlsx_report(self, workbook, data, queries):
        bold = workbook.add_format({"bold": True})
        grey = workbook.add_format({"bg_color": '#D3D3D3'})
        white = workbook.add_format({"bg_color": 'white'})

        for query in queries:
            self.env.cr.execute(query.valid_query_name)
            headers = [d[0] for d in self.env.cr.description]
            bodies = self.env.cr.fetchall()

            sheet = workbook.add_worksheet(str(query.valid_query_name))
            col = 0
            for header in headers:
                sheet.write(0, col, str(header), bold)
                col += 1

            row = 1
            for body in bodies:
                col = 0
                for value in body:
                    sheet.write(row, col, str(value) if (value is not None) else '', grey if row % 2 == 0 else white)

                    col += 1
                row += 1
