# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    enable_task_planning = fields.Boolean("Enable Task Planning?")
