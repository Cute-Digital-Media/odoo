from odoo import http
from odoo.http import request


class LinkTrackerController(http.Controller):

    @http.route('/r/<string:code>', type='http', auth='public', website=True)
    def redirect_short_link(self, code, **kwargs):
        tracker = request.env['link.tracker'].sudo().search([('code', '=', code)], limit=1)
        if not tracker:
            return request.not_found()

        user_agent = request.httprequest.headers.get('User-Agent', '').lower()
        is_bot = any(bot in user_agent for bot in ['facebook', 'twitterbot', 'slackbot', 'whatsapp'])

        if is_bot:
            values = {
                'title': tracker.page_title or tracker.url,
                'description': tracker.extended_description or '',
                'image': tracker.thumbnail_url or '',
                'url': tracker.url,
            }
            return request.render('link_tracker_thumb.link_tracker_preview', values)

        # Regular users: redirect
        return request.redirect(tracker.url, code=302)
