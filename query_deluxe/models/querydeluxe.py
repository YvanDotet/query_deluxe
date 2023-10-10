from odoo import api, fields, models, exceptions, _


class QueryDeluxe(models.Model):
    _name = "querydeluxe"
    _description = "Postgres queries from Odoo interface"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    active = fields.Boolean(string="Active", default=True)

    rowcount = fields.Text(string='Rowcount')
    html = fields.Html(string='HTML')

    name = fields.Text(string='Type a query : ', help="Type the query you want to execute.")
    valid_query_name = fields.Text()

    note = fields.Char(string="Note", help="Optional helpful note about the current query, what it does, the dangers, etc...", translate=True)

    raw_output = fields.Text(string='Raw output')

    def print_result_pdf(self):
        self.ensure_one()

        return {
            'name': _("Select orientation of the PDF's result"),
            'view_mode': 'form',
            'res_model': 'pdforientation',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_query_name': self.valid_query_name
            },
        }

    def print_result_excel(self):
        self.ensure_one()

        if not self.env['ir.module.module'].search([('name', '=', 'query_deluxe_xlsx'), ('state', '=', 'installed')]):
            raise exceptions.ValidationError(_("Please install the module 'query_deluxe_xlsx', that depends to the module 'report_xlsx'."))

    def execute(self):
        for record in self.sudo():
            record.raw_output = ''

            record.rowcount = ''
            record.html = '<br></br>'

            record.valid_query_name = ''

            if record.name:
                record.message_post(body=str(record.name))

                headers = []
                datas = []

                try:
                    record.env.cr.execute(record.name)
                except Exception as e:
                    raise exceptions.UserError(e)

                try:
                    if record.env.cr.description:
                        headers = [d[0] for d in record.env.cr.description]
                        datas = record.env.cr.fetchall()
                except Exception as e:
                    raise exceptions.UserError(e)

                rowcount = record.env.cr.rowcount
                record.rowcount = _("{0} row{1} processed").format(rowcount, 's' if 1 < rowcount else '')

                if headers and datas:
                    record.valid_query_name = record.name
                    record.raw_output = datas

                    header_html = "<tr style='background-color: lightgrey'> <th style='background-color:white'/>"
                    header_html += "".join(["<th style='border: 1px solid black'>"+str(header)+"</th>" for header in headers])
                    header_html += "</tr>"

                    body_html = ""
                    i = 0
                    for data in datas:
                        i += 1
                        body_line = "<tr style='background-color: {0}'> <td style='border-right: 3px double; border-bottom: 1px solid black; background-color: yellow'>{1}</td>".format('cyan' if i%2 == 0 else 'white', i)
                        for value in data:
                            display_value = ''
                            if value is not None:
                                display_value = str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                            body_line += "<td style='border: 1px solid black'>{0}</td>".format(display_value)
                        body_line += "</tr>"
                        body_html += body_line

                    record.html = """
                    <table style="text-align: center">
                        <thead">
                            {0}
                        </thead>
                        
                        <tbody>
                            {1}
                        </tbody>
                    </table>
                    """.format(header_html, body_html)
