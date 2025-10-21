# Copyright 2022 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    default_forecast_date_start = fields.Date()
    default_forecast_date_end = fields.Date()

    # XXX rewrite this based on a trigger field on so lines
    def action_cancel(self):
        res = super().action_cancel()
        self.filtered(lambda r: r.state == "cancel").mapped(
            "order_line"
        )._update_forecast_lines()
        return res

    def action_confirm(self):
        res = super().action_confirm()
        self.filtered(lambda r: r.state == "sale").mapped(
            "order_line"
        )._update_forecast_lines()
        return res

    def write(self, values):
        res = super().write(values)
        if self and "project_id" in values:
            self.env["forecast.line"].sudo().search(
                [("sale_id", "in", self.ids)]
            ).write({"project_id": values["project_id"]})
        if self and "default_forecast_date_start" in values or "default_forecast_date_end" in values:
            for sol in self.mapped("order_line"):
                update_forecast = False
                if not sol.forecast_date_start:
                    sol.write({
                    "forecast_date_start": values.get(
                        "default_forecast_date_start"
                    )})
                    update_forecast = True
                if not sol.forecast_date_end:
                    sol.write({
                        "forecast_date_end": values.get("default_forecast_date_end"),
                    })
                    update_forecast = True
                if update_forecast:
                    sol._update_forecast_lines()
        return res
