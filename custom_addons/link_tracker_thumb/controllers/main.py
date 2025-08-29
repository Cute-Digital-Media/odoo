from odoo import http
from odoo.http import request


class LinkTrackerController(http.Controller):

    @http.route('/r/<string:shortcode>', type='http', auth='public')
    def redirect_short_link(self, shortcode, **kwargs):
        link = request.env['link.tracker.thumb'].sudo().search(
            [('shortcode', '=', shortcode)], limit=1
        )
        if not link:
            return request.not_found()

        # Detect crawlers
        user_agent = request.httprequest.headers.get('User-Agent', '').lower()
        crawler_signatures = ["facebookexternalhit", "twitterbot", "whatsapp", "telegrambot", "linkedinbot"]

        if any(sig in user_agent for sig in crawler_signatures):
            return request.render("link_tracker_thumb.link_tracker_preview", {
                "title": link.title,
                "extended_description": link.extended_description,
                "thumbnail_url": link.thumbnail_url,
                "url": link.target_url,
            })
        else:
            # Normal user: redirect
            return request.redirect(link.target_url, code=302)
