from django.shortcuts import render, redirect
from .models import UrlModel, UrlCollection
from django.http import JsonResponse
from ShortIT.settings import home_url
from .utils import log, UrlResultState, UrlResult


# Homepage view
@log
def index(request):
    return render(request, 'main/index.html')


def response(url):
    response = {
        'msg': UrlResultState().get_current_state().value["msg"],
        'valid': UrlResultState().get_current_state().value["valid"],
        'new_url': url
    }
    return JsonResponse(response)


# Saving and generating shourter url for given input
@log
def add_url(request):
    UrlResultState().set_state(UrlResult.UNKNOWN)
    full_new_url = ""

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        old_url = request.POST.get('old_url', None) # getting data from input old_url

        if 'http:' in old_url[:5] or 'https:' in old_url[:6]:
            if old_url:
                url_obj = UrlModel(old_url)
                url_obj.generate_new_url()
                
                UrlCollection().add_item(url_obj)
                UrlResultState().set_state(UrlResult.OK)
                full_new_url = str(home_url) + 'r/' + str(url_obj.new_url)

        else:
            UrlResultState().set_state(UrlResult.WRONG_URL)

    return response(full_new_url)


# Redirecting to intended url
@log
def connect(request, new_url):
    for url_obj in  UrlCollection():
        if url_obj.new_url == new_url:
            return redirect(url_obj.original_url)

    return redirect('main:index')
