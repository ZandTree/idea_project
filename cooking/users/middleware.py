import logging

from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('user_issues')

User = get_user_model()


class CheckIdBanned(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_banned:
                try:
                    messages.add_message(request, messages.WARNING, 'This account is baned')
                    logger.error(f"banned user access {request.user.id}")
                except messages.MessageFailure:
                    logger.error("banned user message Failure")
                logout(request)
                logger.error(f"banned user is loged out {request.user.id}")
                return HttpResponseRedirect('/')
