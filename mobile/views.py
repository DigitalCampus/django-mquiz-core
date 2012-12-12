# Create your views here.
from django.shortcuts import render,render_to_response
from django.conf import settings
from django.template import RequestContext

def index_view(request,quiz_id=0):
    return render_to_response('mquiz/mobile/index.html', 
                                  {'settings': settings},
                                  context_instance=RequestContext(request))
