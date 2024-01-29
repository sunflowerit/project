# Copyright 2024 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    # Make forecast end date computable and stored
    forecast_date_planned_end = fields.Date(
        compute="_compute_forecast_date_planned_end", inverse=lambda x: None, store=True
    )

    @api.depends("date_deadline")
    def _compute_forecast_date_planned_end(self):
        """Set forecast end to be equal with date deadline"""
        for this in self:
            this.forecast_date_planned_end = this.date_deadline
