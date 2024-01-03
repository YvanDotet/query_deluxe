from odoo import api, fields, models, _


class PdfOrientation(models.TransientModel):
    _name = 'pdforientation'
    _description = "Select the orientation of the pdf"

    def orientation_choices(self):
        return [('landscape', _('Landscape')), ('portrait', _('Portrait'))]

    def get_default_caution_html(self):
        return _("""
        <div>
            <span style='color: red'>Be careful</span>, it will execute the query <span style='color: red; text-decoration: underline'>one more time</span> on your database in order to get-back the datas used to print the result.
            <br/>
            For example, query with <span style='color: orange'>CREATE</span> or <span style='color: orange'>UPDATE</span> statement without any 'RETURNING' statement will not necessary print a table unlike <span style='color: blue'>SELECT</span> statement,
            <br/>
            <span style='text-decoration: underline'>but it will still be executed one time in the background during the attempt of printing process</span>.
            <br/>
            So when you want to print the result, use preferably 'SELECT' statement to be sure to not execute an unwanted query twice.
        </div>
        """)

    orientation = fields.Selection(string="PDF orientation", selection=orientation_choices, default='landscape')
    name = fields.Text(string="Query")
    query_id = fields.Many2one('querydeluxe', string="Query")
    caution_html = fields.Html(string="CAUTION", default=get_default_caution_html)
    understand = fields.Boolean(string="I understand")

    def print_pdf(self):
        self = self.sudo()
        self.ensure_one()

        action_print_pdf = self.env.ref('query_deluxe.action_print_pdf')
        if self.orientation == 'landscape':
            action_print_pdf.paperformat_id.orientation = "Landscape"
        elif self.orientation == 'portrait':
            action_print_pdf.paperformat_id.orientation = "Portrait"
        return action_print_pdf.report_action(self.query_id)
