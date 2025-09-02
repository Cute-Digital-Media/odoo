import logging

from odoo.addons.link_tracker.controller import main as linktracker_main

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class LinkTrackerController(linktracker_main.LinkTracker):

    @http.route('/r/<string:code>', type='http', auth='public', website=True)
    def full_url_redirect(self, code, **post):
        _logger.info("Incoming request with shortcode: %s", code)

        # Odoo's link.tracker uses field `code` for the short code
        tracker = request.env['link.tracker.code'].sudo().search([('code', '=', code)], limit=1)
        if not tracker:
            _logger.warning("No tracker found for shortcode: %s", code)
            return request.not_found()

        if request.env['ir.http'].is_a_bot():
            _logger.info("Crawler detected, serving preview page")
            return request.render("link_tracker_thumb.link_tracker_preview", {
                "title": tracker.link_id.title or "",
                "extended_description": tracker.link_id.extended_description or "",
                "thumbnail_url": tracker.link_id.thumbnail_url or "",
                "url": tracker.link_id.url or "",
            })
        else:
            _logger.info("Register Click")
            request.env['link.tracker.click'].sudo().add_click(
                code,
                ip=request.httprequest.remote_addr,
                country_code=request.geoip.country_code,
            )
            _logger.info("Normal user detected, redirecting to: %s", tracker.link_id.url)
            return request.redirect(tracker.link_id.url, code=301, local=False)
