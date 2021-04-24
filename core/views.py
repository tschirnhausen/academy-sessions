from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from core.utils import token_generator
from ipaddr import client_ip

def index(request):
    session_id = request.session.get('token', token_generator()) # Asign or create
    request.session['token'] = session_id # Set session id at browser

    # Get visited times
    visited_times = request.session.get('visited', 0)
    if visited_times == 0:
        request.session['visited'] = 0
    request.session['visited'] += 1
    visited_times = request.session['visited']

    return JsonResponse({
        'User IP': client_ip(request),
        'session_id': session_id,
        'visited_times': visited_times
    })
