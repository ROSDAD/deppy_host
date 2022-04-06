#%tensorflow_version 1.14
from django.shortcuts import render,redirect
from django.http import HttpResponse
#from deppy.deppy import Chatbotclass
 
import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tensorflow as tf
import random
import tflearn
import pandas as pd
import json
import ijson
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tensorflow as tf
import random
import tflearn
import pandas as pd
import json
import ijson 
from .models import Users
from .models import Chats,Sentiments
from textblob import TextBlob
import secrets
import string
from datetime import date
N = 20

data = pd.read_json('deppy/intents_2.json')
#with open('intents.json', encoding='utf-8') as f:
#   data = json.load(f)
#data = ijson.parse(open("intents.json"))
#pd.DataFrame.from_dict(data, orient='index').T.set_index('index')
#df_json = globals()['intents.json'].to_json(orient='split')
#data=pd.read_json(df_json, orient='split')
#Extracting data
data=dict(data)
#print(data)
words = []
labels = []
docs_x = []
docs_y = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tags"])
        
    if intent['tags'] not in labels:
        labels.append(intent['tags'])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training = numpy.array(training)
output = numpy.array(output)

#model
tf.compat.v1.reset_default_graph()
#tf.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

#model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
#model.save("model.tflearn")
model.load("model.tflearn")
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)
def chat(inp):
    while True:
        
        if inp.lower() == "quit":
            return "Nice talking to you! Have a good day!"
            break

        results = model.predict([bag_of_words(inp, words)])
        results_index = numpy.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg['tags'] == tag:
                responses = tg['responses']

        return random.choice(responses)

def index(request):
    if "username" in request.session or "email" in request.session:
        obj = Chats.objects.all().filter(email=request.session['email'])
        
        return render(request,"deppy.html",{"obj":obj})
    else:
        return render(request,"login.html")

def chatpost(request):
    if request.method=="POST":
        obj = Chats()
        message = request.POST["message"]
        chatreply = chat(message)
        obj.email = request.session['email']
        obj.inpchat = message
        obj.replychat = chatreply
        obj.sessionuid = request.session['suid']
        obj.save()
        return HttpResponse(chatreply)
def signup(request):
    if request.method=="POST":
        if request.POST["signupuname"]!="":
            uname = request.POST["signupuname"]
        else:
            return render(request,"login.html")
        if request.POST["signupemail"]!="":
            email = request.POST["signupemail"]
        else:
            return render(request,"login.html") 
        if request.POST["signuppass"]!="":
            signuppass = request.POST["signuppass"]
        else:
            return render(request,"login.html")
        if request.POST["signupcnfpass"]!="":
            signupcnfpass = request.POST["signupcnfpass"]
        else:
            return render(request,"login.html")        
        if signuppass==signupcnfpass:
            
            obj = Users.objects.all().filter(email=email)
            if len(obj) == 0:
                
                users = Users()
                users.name = uname
                users.email = email
                users.password = signuppass

                users.save()
                res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(N))
                request.session['suid']=res
                sentiments = Sentiments.objects.all().filter(email=email)
                sessionno=len(sentiments)+1
                obj = Sentiments()
                obj.sessionno = sessionno
                obj.email = email
                
                obj.sessionuid = res
                obj.save()
                request.session['uname'] = uname
                request.session['email'] = email
                
            return redirect("/")
                

def signin(request):
    if request.method=="POST":
        if request.POST["signinemail"]!="":
            uemail = request.POST["signinemail"]
        else:
            return render(request,"login.html")
        if request.POST["signinpass"]!="":
            password = request.POST["signinpass"]
        else:
            return render(request,"login.html") 
        user = Users.objects.all().filter(email=uemail,password=password)
        if len(user) != 0:
            res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)for i in range(N))
            request.session['suid']=res
            sentiments = Sentiments.objects.all().filter(email=uemail)
            sessionno=len(sentiments)+1
            obj = Sentiments()
            obj.sessionno = sessionno
            obj.email = uemail
           
            obj.sessionuid = res
            obj.save()
            user = Users.objects.get(email=uemail,password=password)
            request.session['uname'] = user.name
            request.session['email'] = uemail
        return redirect("/")
            
        
def logout(request):
    if request.method == "POST":
        if request.POST['action']=="logout":
            del request.session['email']
            del request.session['suid']
            del request.session['uname']
            return HttpResponse("logoutsuccessful")
def showprofile(request):
    if request.session.get('email', None):
        sentiments = Sentiments.objects.all().filter(email=request.session['email'],sentiment="NA")
         
        for i in range(len(sentiments)):
            
            sentarr = []

            chats = Chats.objects.all().filter(sessionuid=sentiments[i].sessionuid)
            if len(chats)>0:
                for j in range(len(chats)):
                    
                    sentarr.append(TextBlob(chats[j].inpchat).sentiment.polarity)
                    
                sent = float(sum(sentarr))/len(sentarr)
            else:
                sent="NA"
            obj = Sentiments.objects.get(sessionuid=sentiments[i].sessionuid)
            obj.sentiment = str(sent)
            obj.save()
        sentiments = Sentiments.objects.all().filter(email=request.session['email'])
        sent = sentiments
        overhap = []
        for i in sent:
            if i.sentiment !="NA":
                senttemp = '{0:.2f}'.format(float(i.sentiment)*100)
                i.sentiment = senttemp
                overhap.append(float(i.sentiment))
                i.sentiment = senttemp+"%"
        
        overallhap = '{0:.2f}'.format(float(sum(overhap))/len(overhap))
        return render(request,"profile.html",{"sentiments":sent,"uname":request.session['uname'],"uemail":request.session['email'],"date":date.today(),"overallhap":overallhap})
    else:
        return render(request,"login.html")
        