from odoo import api, fields, models


class QueryDeluxe(models.Model):
    _inherit = "querydeluxe"

    def print_result_excel(self):
        res = super().print_result_excel()

        report_id = self.env.ref("query_deluxe_xlsx.action_print_xlsx")
        return report_id.report_action(self)
