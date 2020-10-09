from django.http import HttpResponse


# Create your views here.


def home(request):
    return HttpResponse()

#
# @api_view(http_method_names=['GET'])
# def get_text_response(request: HttpRequest):
#     uid = request.GET.get('user_id')
#     text = request.GET.get('text')
#     response = DialogFlowAgent.detect_intent(session_id=uid, text=text)
#     return JsonResponse({'result': response})
