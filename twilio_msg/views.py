from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from twilio.twiml.messaging_response import MessagingResponse

@csrf_exempt
def whatsapp(request):
    r = MessagingResponse()
    r.message('Hello from your Django app!')
    return HttpResponse(r, content_type='text/xml')
