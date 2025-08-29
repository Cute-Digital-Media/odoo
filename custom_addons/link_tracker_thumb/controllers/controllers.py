from odoo import http
from odoo.http import request

import logging

_logger = logging.getLogger(__name__)


class LinkTrackerController(http.Controller):

    @http.route('/rt/<string:code>', type='http', auth='public', website=True)
    def redirect_short_link(self, code, **kwargs):

        _logger.info("Incoming request with shortcode: %s", code)
        _logger.debug("Request headers: %s", request.httprequest.headers)

        tracker = request.env['link.tracker'].sudo().search([('code', '=', code)], limit=1)
        if not tracker:
            _logger.warning("No link found for shortcode: %s", code)
            return request.not_found()

        user_agent = request.httprequest.headers.get('User-Agent', '').lower()

        _logger.info("User-Agent detected: %s", user_agent)

        is_bot = any(bot in user_agent for bot in ['facebook', 'twitterbot', 'slackbot', 'whatsapp'])

        if is_bot:
            _logger.info("Crawler detected, rendering preview for shortcode %s", code)
            values = {
                'title': tracker.page_title or tracker.url,
                'description': tracker.extended_description or '',
                'image': tracker.thumbnail_url or '',
                'url': tracker.url,
            }
            return request.render('link_tracker_thumb.link_tracker_preview', values)

        # Regular users: redirect
        _logger.info("Normal user detected, redirecting to: %s", tracker.url.target_url)
        return request.redirect(tracker.url, code=302)
