from odoo import api, fields, models, _


class QueryDeluxe(models.Model):
    _inherit = "querydeluxe"

    def print_xlsx(self):
        self.ensure_one()
        report_id = self.env.ref("addons_xlsx_query_deluxe.report_xlsx")
        return report_id.report_action(self)
