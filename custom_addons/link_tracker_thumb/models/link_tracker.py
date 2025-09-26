import uuid

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LinkTracker(models.Model):
    _inherit = 'link.tracker'

    code = fields.Char(
        string="Code",
        required=True,
        readonly=False,
        store=True,
        default=lambda self: str(uuid.uuid4())[:8],
    )

    thumbnail_url = fields.Char(
        string="Thumbnail URL",
        help="Optional thumbnail image for this link"
    )
    extended_description = fields.Text(
        string="Extended Description"
    )

    _sql_constraints = [
        ("link_tracker_code_uniq", "unique(code)", "Code must be unique!"),
    ]

    @api.model
    def create(self, vals):
        record = super().create(vals)

        if record.code:
            tracker_code = self.env['link.tracker.code'].search([('link_id', '=', record.id)], limit=1)
            if tracker_code:
                tracker_code.write({'code': record.code})

        return record

    def write(self, vals):
        res = super().write(vals)

        if "code" in vals:
            for rec in self:
                tracker_code = self.env['link.tracker.code'].search([('link_id', '=', rec.id)], limit=1)
                if tracker_code:
                    tracker_code.write({'code': rec.code})

        return res

    @api.constrains("code")
    def _check_unique_code(self):
        for rec in self:
            if rec.code and self.search([("code", "=", rec.code), ("id", "!=", rec.id)], limit=1):
                raise ValidationError(_("This code is already in use. Please choose another one."))
