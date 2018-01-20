"""
This is the template server side for ChatBot
"""
from sys import argv
from bottle import route, run, template, static_file, request, response
import datetime, time, json, requests, os, random


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    if user_message[-1] =="?" or user_message[-1] =="!" or user_message[-1] ==":" or user_message[-1] =="," or user_message[-1] ==".":
         user_message = user_message[:-1]
    user_message_to_list = user_message.lower().split()
    for word in user_message_to_list:
        if word == "name":
            return json.dumps(save_name(user_message))
        elif word == "joke" or word == "chuck" or word == "norris":
            return json.dumps(get_random_joke(user_message))
        elif word == "game" or word == "paper" or word == "rock" or word == "scissors":
            return json.dumps(play_game(user_message))
        elif word == "weather":
            return json.dumps(get_weather(user_message))
        elif word == "time":
            return json.dumps(get_time())
        elif word == "date":
            return json.dumps(get_date())
        else:
            respond = handle_conversation(user_message)
    return json.dumps(respond)


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


@route('/sounds/<filename:re:.*\.wav>', method='GET')
def sounds(filename):
    return static_file(filename, root='sounds')


def save_name(user_message):
    user_message = user_message.lower().split("is")
    user_message = user_message[1][1:].capitalize()
    user_name = request.get_cookie("user_name")
    if user_name == user_message:
        return {"animation": "inlove", "msg": "Hello again " + str(user_name) + "! I'm glad to see you again(:"}
    else:
        response.set_cookie(name = "user_name", value = str(user_message))
        return {"animation": "excited", "msg": "Howdy stranger, nice to meet you " + str(user_message) + "!"}


def get_random_joke(user_message):
    if "chuck" in user_message or "norris" in user_message:
        joke = requests.get('http://api.icndb.com/jokes/random')
        joke = joke.json()
        joke = joke['value']['joke']
        return {"animation": "giggling", "msg": joke}
    else:
        joke = requests.get('http://api.yomomma.info')
        joke = joke.json()
        joke = joke['joke']
        return {"animation": "laughing", "msg": joke}



def play_game(user_message):
    options = ["paper","rock","scissors"]
    if user_message == "paper" or user_message == "rock" or user_message == "scissors":
        user_choice = user_message
        boto_choice = random.choice(options)
        if (boto_choice == "paper" and user_choice == "rock") or (boto_choice == "rock" and user_choice == "scissors") or (boto_choice == "scissors" and user_choice == "paper"):
            return {"animation": "money", "msg": "I chose " + boto_choice + ". I won! show me the MONEY!!"}
        elif (boto_choice == "paper" and user_choice == "scissors") or (boto_choice == "rock" and user_choice == "paper") or (boto_choice == "scissors" and user_choice == "rock"):
            return {"animation": "crying", "msg": "I chose " + boto_choice + ". You won!"}
        else:
            return {"animation": "bored", "msg": "I chose " + boto_choice + ". It's a tie, bummer, it's boring.."}
    else:
        return {"animation": "excited", "msg": "Let's play paper, rock scissors! please choose one.."}




def get_weather(user_message):
    try:
        if 'in' not in user_message:
            city_name = 'tel aviv'
            weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+ city_name + '&appid=5d1452edf89427c2b801a97919ea0a8b')
            json_object = weather.json()
            temp_k = int(json_object['main']['temp'])
            temp_c = int(temp_k - 273.15)
            if temp_c < 15:
                return {"animation": "takeoff", "msg": "The weather in " + str(city_name.capitalize()) + " ya habibi Tel aviv is " + str(temp_c) + " celsius. So cold!!"}
            elif 16 < temp_c < 28:
                return {"animation": "inlove", "msg": "The weather in " + str(city_name.capitalize()) + " ya habibi Tel aviv is " + str(temp_c) + " celsius. Nice and warm, just as I love it!"}
            else:
                return {"animation": "takeoff", "msg": "The weather in " + str(city_name.capitalize()) + " ya habibi Tel aviv is " + str(temp_c) + " celsius. Way too hot for me.."}
        else:
            user_message = user_message.lower().split("in")
            city_name = user_message[1][1:]
            weather = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+ city_name + '&appid=5d1452edf89427c2b801a97919ea0a8b')
            if weather is None:
                return {"animation": "confused", "msg": "There's no such city.. please correct yourself"}
            else:
                json_object = weather.json()
                temp_k = int(json_object['main']['temp'])
                temp_c = int(temp_k - 273.15)
                if city_name == 'tel aviv':
                    if temp_c < 15:
                        return {"animation": "takeoff", "msg": "The weather in " + str(city_name.capitalize()) + " ya habibi Tel aviv is " + str(temp_c) + " celsius. So cold!!"}
                    elif 16 < temp_c < 28:
                        return {"animation": "inlove", "msg": "The weather in " + str(city_name.capitalize()) + " ya habibi Tel aviv is " + str(temp_c) + " celsius. Nice and warm, just as I love it!"}
                    else:
                        return {"animation": "takeoff", "msg": "The weather in " + str(city_name.capitalize()) + " ya habibi Tel aviv is " + str(temp_c) + " celsius. Way too hot for me.."}
                else:
                    if temp_c < 15:
                        return {"animation": "takeoff", "msg": "The weather in " + str(city_name.capitalize()) + " is " + str(temp_c) + " celsius. So cold!!"}
                    elif 16 < temp_c < 28:
                        return {"animation": "inlove", "msg": "The weather in " + str(city_name.capitalize()) + " is " + str(temp_c) + " celsius. Nice and warm, just as I love it!"}
                    else:
                        return {"animation": "takeoff", "msg": "The weather in " + str(city_name.capitalize()) + " is " + str(temp_c) + " celsius. Way too hot for me.."}
    except Exception:
        return {"animation": "confused", "msg": "There's no such city.. please correct yourself"}


def get_time():
    return {"animation": "waiting", "msg": "The time right now is " + str(time.strftime("%H:%M"))}


def get_date():
    return {"animation": "waiting", "msg": "Today is " + datetime.date.today().strftime("%B") + " " + time.strftime("%d") + " " + time.strftime("%Y")}



def handle_conversation(user_message):
    user_message_to_list = user_message.lower().split()
    list_of_swears = ['ass', 'fuck', 'shit', 'shitty', 'hell']
    if any(word in user_message_to_list for word in list_of_swears):
        return {"animation": "no", "msg": "Please don't swear"}
    elif user_message.startswith("boo") or user_message.startswith("scary"):
        return {"animation": "afraid", "msg": "Ahhhhh"}
    elif user_message.endswith("music"):
        return {"animation": "dancing", "msg": "I love music! Yalla kapa eim!"}
    elif user_message.endswith("animal") or user_message.endswith("animals"):
        return {"animation": "dog", "msg": "I prefer animals on humans anytime.."}
    elif user_message.endswith("bye") or user_message.endswith("see you"):
        return {"animation": "heartbroke", "msg": "Goodbye for now, see you soon!"}
    else:
        return {"animation": "ok", "msg": user_message}


def main(host="0.0.0.0", port=None):
    if not port:
        port = argv[1]   
    run(host=host, port=port)


if __name__ == '__main__':
    main(host="localhost", port=7000)  # run on localhost
    #main()
