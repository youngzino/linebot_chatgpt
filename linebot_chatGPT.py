from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import openai
openai.api_key = "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"
model_use = "text-davinci-003"

channel_secret = "db61000871a5f743719e67ef2da013ba"
channel_access_token = "U05As0MI3O9Wj96CdCP+y56xYeLAMbcjyona0OynbKsxQ0+Hrs0KWy3uZmsnpim5Qjoe0cu5V0RsoXRXx3ua8xaRn7iwzHaunZP92y2dpYLw8vaIu1u/lso1F8/hG2PY7/Oz54yS1LFS7OM24jFKtwdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)

    prompt_text = text

    response = openai.Completion.create(
        model=model_use,
        prompt=prompt_text,  
        max_tokens=1024) # max 4096

    text_out = response.choices[0].text 
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()

