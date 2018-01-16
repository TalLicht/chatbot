"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    user_message_to_list = user_message.lower()
    user_message_to_list = user_message_to_list.split()
    list_of_swears = ['ass','fuck','shit','shitty','hell']
    if any(word in user_message_to_list for word in list_of_swears):
        print("first if")
        a = handle_swears(user_message)
    else:
        print("else")
        a = handle_conversation(user_message)
    return json.dumps(a)


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')



def handle_swears(user_message):
    return {"animation": "no", "msg": "Please don't swear"}


def handle_conversation(user_message):
    if user_message.startswith("My name") or user_message.startswith("my name"):
        return {"animation": "inlove", "msg": "Hi"}
    elif user_message.startswith("music"):
        return {"animation": "dancing", "msg": "I love music!"}
    elif user_message.endswith("animal") or user_message.endswith("animals"):
        return {"animation": "dog", "msg": "Oh that's awesome! "}
    elif user_message.endswith("bye") or user_message.endswith("see you"):
        return {"animation": "heartbroke", "msg": "Goodbye"}
    else:
        return {"animation": "ok", "msg": user_message}



def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
