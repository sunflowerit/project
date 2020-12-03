# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = "project.task"

    enable_task_planning = fields.Boolean(
        related='project_id.enable_task_planning')
    date_range_id = fields.Many2one(
        comodel_name="date.range", string="Date range")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")

    _sql_constraints = [
        ('start_end_date_check',
         "CHECK ((start_date <= end_date))",
         "The start date must be prior to the end date."),
    ]

    @api.onchange("date_range_id")
    def onchange_date_range_id(self):
        self.start_date = self.date_range_id.date_start
        self.end_date = self.date_range_id.date_end
