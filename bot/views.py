import json
import logging

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

# Create your views here.
from bot.bot_api import handler, line_bot_api
from utils.postback.parser import PostbackParser

logger = logging.getLogger('BotHandler')
logger.setLevel(logging.DEBUG)


@csrf_exempt
def health(request):
    return JsonResponse({'status': 'up and running'})


@csrf_exempt
def send_message(request: HttpRequest):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode('utf-8'))
            msg = TextSendMessage(text=body['text'])
            line_bot_api.push_message(
                to=body['userId'],
                messages=msg
            )
        except Exception:
            print("Push message failed")
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST'])


# this is code is modified from https://github.com/line/line-bot-sdk-python
@csrf_exempt  # this is used for avoid csrf request from line server
def callback(request):
    if request.method == "POST":
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        global domain
        domain = request.META['HTTP_HOST']

        # get request body as text
        body = request.body.decode('utf-8')
        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event: MessageEvent):
    line_bot_api.reply_message(event.reply_token, TextSendMessage("Hello"))


@handler.add(PostbackEvent)
def handle_postback(event: PostbackEvent):
    pdata: str = event.postback.data
    try:
        message = PostbackParser.get_return_message(data=pdata, user_id=event.source.user_id)
    except Exception as e:
        text = "Error: " + " ".join(e.args)
        message = TextSendMessage(text=text)
    line_bot_api.reply_message(
        reply_token=event.reply_token,
        messages=message
    )
