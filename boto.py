"""
This is the template server side for ChatBot
"""
from sys import argv
from bottle import route, run, template, static_file, request
import json
import requests


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    user_message_to_list = user_message.lower().split()
    for word in user_message_to_list:
        if word == "joke":
            print "in joke"
            a = get_random_joke()
        else:
            a = handle_conversation(user_message)
    return json.dumps(a)


@route("/test", method='POST')
def chat():
    user_message = request.get('msg')
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



def get_random_joke():
    joke = requests.get('http://api.icndb.com/jokes/random')
    joke = joke.json()
    joke = joke['value']['joke']
    return {"animation": "laughing", "msg": joke}


def handle_conversation(user_message):
    user_message_to_list = user_message.lower()
    user_message_to_list = user_message_to_list.split()
    list_of_swears = ['ass', 'fuck', 'shit', 'shitty', 'hell']
    if any(word in user_message_to_list for word in list_of_swears):
        return {"animation": "no", "msg": "Please don't swear"}
    elif user_message.startswith("My name") or user_message.startswith("my name"):
        return {"animation": "inlove", "msg": "Hi"}
    elif user_message.startswith("music"):
        return {"animation": "dancing", "msg": "I love music!"}
    elif user_message.endswith("animal") or user_message.endswith("animals"):
        return {"animation": "dog", "msg": "Oh that's awesome! "}
    elif user_message.endswith("bye") or user_message.endswith("see you"):
        return {"animation": "heartbroke", "msg": "Goodbye"}
    else:
        return {"animation": "ok", "msg": user_message}



def main(host="0.0.0.0", port=None):
    if not port:
        port = argv[1]   
    run(host=host, port=port)


if __name__ == '__main__':
    main(host="localhost", port=7000)  # run on localhost
    #main()
