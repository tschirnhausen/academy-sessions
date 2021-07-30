from django.shortcuts import render
from django.http import JsonResponse
from core.utils import token_generator
from ipaddr import client_ip

from django.views import View
from django.utils import timezone

from core.models import Log

###############################################################
#            DOCUMENTATION FOR DJANGO SESSIONS:               #
# https://docs.djangoproject.com/en/3.2/topics/http/sessions/ #
#               Written by Javier Valenzuela                  #
#              javier.valenzuelac@mail.udp.cl                 #
###############################################################

class UserSession(View):

    def setup(self, request, *args, **kwargs):
        try:
            session = request.session.get('token', token_generator())
            request.session['token'] = session
            last_activity = request.session.get('last_activity', timezone.now())
            request.session['last_activity'] = str(last_activity) # Ignore if already has activity
            # print(request.session.get_expiry_age()) Check the first expiry age
            request.session.set_expiry(365 * 24 * 60 * 60) # Increment expiry date for one year, each time is visited

        except Exception as e:
            # Be sure to create to see the error in production
            Log.objects.create(
                error=e
            )
            pass

        return super().setup(self, request, *args, **kwargs)


class TestView(UserSession):
    def get(self, request):
        session_id = request.session.get('token') # We do not assign here the session
        last_activity = request.session.get('last_activity')
        request.session['last_activity'] = str(timezone.now()) # Update activity time

        # Get visited times
        visited_times = request.session.get('visited', 0)
        if visited_times == 0:
            request.session['visited'] = 0
        request.session['visited'] += 1
        visited_times = request.session['visited']

        # print(request.session.get_expiry_age()) To check if expiry age has been updated

        return JsonResponse({
            'user_ip': client_ip(request),
            'session_id': session_id,
            'visited_times': visited_times,
            'last_timestamp': last_activity,
            'cookies_data': {
                'cookie_consent_status': request.COOKIES.get('cookieconsent_status', None),
                'session_id': request.COOKIES.get('sessionid', None)

            }
        })

class FlushView(View):
    def get(self, request):
        request.session.flush()
        return JsonResponse({
            'status': 'Your session has been deleted.'
        })        
