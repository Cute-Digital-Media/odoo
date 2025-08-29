from odoo import fields, models


class LinkTracker(models.Model):
    _inherit = 'link.tracker'

    thumbnail_url = fields.Char(
        string="Thumbnail URL",
        help="Optional thumbnail image for this link"
    )
    extended_description = fields.Text(
        string="Extended Description"
    )
