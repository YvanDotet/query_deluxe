from odoo import api, fields, models, _
from odoo.exceptions import UserError


class QueryDeluxe(models.Model):
    _name = "querydeluxe"
    _description = "Postgres queries from Odoo interface"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    tips = fields.Many2one('tipsqueries', string="Examples")
    tips_description = fields.Text(related='tips.description')

    rowcount = fields.Text(string='Rowcount')
    html = fields.Html(string='HTML')

    name = fields.Text(string='Type a query : ')
    valid_query_name = fields.Text()

    show_raw_output = fields.Boolean(string='Show the raw output of the query')
    raw_output = fields.Text(string='Raw output')

    def print_result(self):
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

    def copy_query(self):
        self.ensure_one()

        if self.tips:
            self.name = self.tips.name

    def execute(self):
        self = self.sudo()
        self.ensure_one()

        self.show_raw_output = False
        self.raw_output = ''

        self.rowcount = ''
        self.html = '<br></br>'

        self.valid_query_name = ''

        if self.name:
            self.tips = False
            self.message_post(body=str(self.name))

            headers = []
            datas = []

            try:
                self.env.cr.execute(self.name)
            except Exception as e:
                raise UserError(e)

            try:
                if self.env.cr.description:
                    headers = [d[0] for d in self.env.cr.description]
                    datas = self.env.cr.fetchall()
            except Exception as e:
                raise UserError(e)

            rowcount = self.env.cr.rowcount
            self.rowcount = _("{0} row{1} processed").format(rowcount, 's' if 1 < rowcount else '')

            if headers and datas:
                self.valid_query_name = self.name
                self.raw_output = datas

                header_html = "<tr style='background-color: lightgrey'> <th style='background-color:white'/>"
                header_html += "".join(["<th style='border: 1px solid black'>" + str(header) + "</th>" for header in headers])
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

                self.html = """
<table style="text-align: center">
  <thead>
    {0}
  </thead>

  <tbody>
    {1}
  </tbody>
</table>
""".format(header_html, body_html)


class TipsQueries(models.Model):
    _name = 'tipsqueries'
    _description = "Tips for queries"

    name = fields.Text(string='Query', required=True)
    description = fields.Text(string="Description", translate=True)
