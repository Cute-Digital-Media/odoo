import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class LinkTrackerController(http.Controller):

    @http.route('/r/<string:shortcode>', type='http', auth='public')
    def redirect_short_link(self, shortcode, **kwargs):
        _logger.info("Incoming request with shortcode: %s", shortcode)

        # Odoo's link.tracker uses field `code` for the short code
        tracker = request.env['link.tracker'].sudo().search([('code', '=', shortcode)], limit=1)
        if not tracker:
            _logger.warning("No tracker found for shortcode: %s", shortcode)
            return request.not_found()

        user_agent = request.httprequest.headers.get('User-Agent', '').lower()
        _logger.info("User-Agent detected: %s", user_agent)

        crawler_signatures = ["facebookexternalhit", "twitterbot", "whatsapp", "telegrambot", "linkedinbot"]

        if any(sig in user_agent for sig in crawler_signatures):
            _logger.info("Crawler detected, serving preview page")
            return request.render("link_tracker_thumb.link_tracker_preview", {
                "title": tracker.title or "",
                "extended_description": tracker.extended_description or "",
                "thumbnail_url": tracker.thumbnail_url or "",
                "url": tracker.url or "",
            })
        else:
            _logger.info("Normal user detected, redirecting to: %s", tracker.url)
            return request.redirect(tracker.url, code=301, local=False)
