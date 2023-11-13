from odoo import api, fields, models, exceptions, _


class QueryDeluxe(models.Model):
    _name = "querydeluxe"
    _description = "PostgreSQL queries from Odoo interface"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    def get_default_caution_html(self):
        return _("""
        <div>
            <span style='color: red'>Be careful</span>, the printing buttons will execute the query <span style='color: red; text-decoration: underline'>one more time</span> on your database in order to get-back the datas used to print the result.
            <br/>
            For example, query with <span style='color: orange'>CREATE</span> or <span style='color: orange'>UPDATE</span> statement without any 'RETURNING' statement will not necessary print a table unlike <span style='color: blue'>SELECT</span> statement,
            <br/>
            <span style='text-decoration: underline'>but it will still be executed one time in the background during the attempt of printing process</span>.
            <br/>
            So when you want to print the result, use preferably 'SELECT' statement to be sure to not execute an unwanted query twice.
        </div>
        """)

    active = fields.Boolean(string="Active", default=True)

    caution_html = fields.Html(string="CAUTION", default=get_default_caution_html)
    understand = fields.Boolean(string="I understand")

    rowcount = fields.Text(string='Rowcount')
    html = fields.Html(string='HTML')

    name = fields.Text(string='Type a query : ', help="Type the query you want to execute.")
    note = fields.Char(string="Note", help="Optional helpful note about the current query, what it does, the dangers, etc...", translate=True)

    def print_result_pdf(self):
        self.ensure_one()

        return {
            'name': _("Select orientation of the PDF's result"),
            'view_mode': 'form',
            'res_model': 'pdforientation',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_name': self.name,
                'default_query_id': self.id
            },
        }

    def print_result_excel(self):
        self.ensure_one()
        self=self.sudo()

        if not self.env['ir.module.module'].search([('name', '=', 'query_deluxe_xlsx'), ('state', '=', 'installed')]):
            raise exceptions.ValidationError(_("""
            Please install the module 'query_deluxe_xlsx', that depends on the module 'report_xlsx'.\n 
            The module 'query_deluxe_xlsx' is available at \n https://apps.odoo.com/apps/modules/17.0/query_deluxe_xlsx \n 
            The module 'report_xlsx' should be available at \n https://apps.odoo.com/apps/modules/17.0/report_xlsx \n
            """))

    def get_result_from_query(self, query):
        self = self.sudo()
        headers = []
        datas = []

        if query:
            try:
                self.env.cr.execute(query)
            except Exception as e:
                raise exceptions.UserError(e)

            try:
                if self.env.cr.description:
                    headers = [d[0] for d in self.env.cr.description]
                    datas = self.env.cr.fetchall()
            except Exception as e:
                raise exceptions.UserError(e)

        return headers, datas

    def execute(self):
        for record in self.sudo():
            record.rowcount = ''
            record.html = '<br></br>'

            if record.name:
                record.message_post(body=str(record.name))

                headers, datas = self.get_result_from_query(record.name)

                rowcount = record.env.cr.rowcount
                record.rowcount = _("{0} row{1} processed").format(rowcount, 's' if 1 < rowcount else '')

                if headers and datas:
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
