from odoo import models, fields


class LinkTrackerThumb(models.Model):
    _name = "link.tracker.thumb"
    _description = "Link Tracker with Thumbnail"

    shortcode = fields.Char(required=True, index=True)
    title = fields.Char(string="Title")
    extended_description = fields.Text(string="Extended Description")
    thumbnail_url = fields.Char(string="Thumbnail URL")
    target_url = fields.Char(string="Target URL", required=True)
