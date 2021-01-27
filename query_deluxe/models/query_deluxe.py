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

    name = fields.Char(string='Type a query : ')
    valid_query_name = fields.Char()

    show_raw_output = fields.Boolean(string='Show the raw output of the query')
    raw_output = fields.Text(string='Raw output')

    def print_result(self):
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
        if self.tips:
            self.name = self.tips.name

    def execute(self):
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
                no_fetching = ['update', 'delete', 'create', 'insert', 'alter', 'drop']
                max_n = len(max(no_fetching))

                is_insides = [(o in self.name.lower().strip()[:max_n]) for o in no_fetching]
                if True not in is_insides:
                    headers = [d[0] for d in self.env.cr.description]
                    datas = self.env.cr.fetchall()
            except Exception as e:
                raise UserError(e)

            rowcount = self.env.cr.rowcount
            self.rowcount = "{0} row{1} processed".format(rowcount, 's' if 1 < rowcount else '')

            if headers and datas:
                self.valid_query_name = self.name
                self.raw_output = datas

                header_html = "".join(["<th style='border: 1px solid'>"+str(header)+"</th>" for header in headers])
                header_html = "<tr>"+"<th style='background-color:white !important'/>"+header_html+"</tr>"

                body_html = ""
                i = 0
                for data in datas:
                    i += 1
                    body_line = "<tr>"+"<td style='border-right: 3px double; border-bottom: 1px solid; background-color: yellow'>{0}</td>".format(i)
                    for value in data:
                        body_line += "<td style='border: 1px solid; background-color: {0}'>{1}</td>".format('cyan' if i%2 == 0 else 'white', str(value) if (value is not None) else '')

                    body_line += "</tr>"
                    body_html += body_line

                self.html = """
<table style="text-align: center">
  <thead style="background-color: lightgrey">
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
    _order = 'create_date desc, id'

    name = fields.Char(string='Query', required=True)
    description = fields.Text(string="Description")
