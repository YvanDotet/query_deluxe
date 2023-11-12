from odoo import api, fields, models, _


class PdfOrientation(models.TransientModel):
    _name = 'pdforientation'
    _description = "Select the orientation of the pdf"

    def orientation_choices(self):
        return [('landscape', _('Landscape')), ('portrait', _('Portrait'))]

    orientation = fields.Selection(string="PDF orientation", selection=orientation_choices, default='landscape')
    name = fields.Text(string="Query")
    query_id = fields.Many2one('querydeluxe', string="Query")

    def print_pdf(self):
        self.ensure_one()

        action_print_pdf = self.env.ref('query_deluxe.action_print_pdf')
        if self.orientation == 'landscape':
            action_print_pdf.paperformat_id.orientation = "Landscape"
        elif self.orientation == 'portrait':
            action_print_pdf.paperformat_id.orientation = "Portrait"
        return action_print_pdf.report_action(self.query_id)
