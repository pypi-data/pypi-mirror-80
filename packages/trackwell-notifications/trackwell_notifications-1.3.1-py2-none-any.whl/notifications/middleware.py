# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import operator
import re

from django.utils.deprecation import MiddlewareMixin

from .models import Notification, UserNotification

try:
    from urlparse import urlparse  # Python 2 only
except ImportError:
    from urllib.parse import urlparse  # Python 3 only


class NotificationMiddleware(MiddlewareMixin):

    def is_valid_request(self, request):
        return hasattr(request, 'user') and request.user.is_authenticated

    def process_request(self, request):
        """
        Adds notification status to requests for handling in views etc.
        :param request:
        :return: None
        """
        if self.is_valid_request(request):
            request.notifications = Notification.unseen(request.user)

    def process_response(self, request, response):

        if not self.is_valid_request(request):
            return response

        notifications = Notification.unseen(request.user)
        # Need to ensure cookie string is in reverse order from closest to last
        sorted_items = sorted(notifications.items(), key=operator.itemgetter(1))

        now = datetime.datetime.now()
        any_active_with_matching_path = False
        if notifications:
            notification_value_list = UserNotification.objects.filter(id__in=notifications.keys()).values_list(
                'notification__display_only_if_url_path_matches_regex', 'notification__active_from',
                'notification__expires')
            for regex, active_from, expires in notification_value_list:
                if active_from is not None and now < active_from:
                    continue
                if expires is not None and now > expires:
                    continue
                any_active_with_matching_path |= re.search(regex, request.path) is not None
                if not any_active_with_matching_path:
                    referer_path = urlparse(request.META.get('HTTP_REFERER', '')).path
                    any_active_with_matching_path |= re.search(regex, referer_path) is not None

                if any_active_with_matching_path:
                    break

        if any_active_with_matching_path:
            epoch = datetime.datetime.utcfromtimestamp(0)
            max_age = 14 * 24 * 60 * 60
            expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)

            coookie_string = "-".join('{}:{}'.format(
                key, (val - epoch).total_seconds() * 1000.0) for key, val in sorted_items
                                       )
            response.set_cookie(
                'notifications', coookie_string, expires=expires
            )
        else:
            response.delete_cookie('notifications')

        return response
