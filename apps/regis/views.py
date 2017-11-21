# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages

from models import *

def noname(req):
    return 'id' not in req.session

def index(req):
    return render(req, "regis/index.html")

def remove(req,id):
    this_user=User.manager.get(id=req.session['id'])
    this_quote = Quote.manager.get(id=id)
    this_quote.favorite.remove(this_user)
    return redirect('/success')

def add(req, id):
    this_user=User.manager.get(id=req.session['id'])
    this_quote = Quote.manager.get(id=id)
    this_quote.favorite.add(this_user) 
    return redirect('/success')

def success(req):
    if noname(req):
        return redirect('/')
    user = User.manager.get(id=req.session['id'])
    allQuote = Quote.manager.all()
    userID= req.session['id']
    this_user = User.manager.get(id= req.session['id'])
    isFav = this_user.favs.all()
    set1=set({})
    set2=set({})
    for quote in allQuote:
        set1.add(quote)
    for quote in isFav:
        set2.add(quote)
    try:
        yourQuote = set2
    except Exception:
        yourQuote= {}
    try:
        notYour = set1 - set2
    except Exception:
        notYour={}

    context ={
        'self': user,
        'allQuote': allQuote,
        'yourQuote': yourQuote,
        'notYour': notYour
    }
    print notYour
    print yourQuote
    return render(req, "regis/success.html", context)

def login(req):
    result = User.manager.login(req.POST)
    if result[0]:
        req.session['id'] = result[1].id
        # print req.session['id']
        return redirect('/success')
    for message in result[1]:
        messages.error(req,message[1])
    return redirect('/')

def register(req):
    result = User.manager.createUser(req.POST)
    if result[0]:
        for key, message in result[1].iteritems():
            messages.error(req, message)
        return redirect('/')
    for key, message in result[1].iteritems():
        messages.error(req, message)
    return redirect('/')

def user(req, id):
    if noname(req):
        return redirect('/')
    count = 0
    user=User.manager.get(id=id)
    isUser = Quote.manager.filter(creater_id=id)
    set1=set({})
    for quote in isUser:
        set1.add(quote)
    for ids in isUser:
        count += 1
    try:
        yourQuote = set1
    except Exception:
        yourQuote= {}
    context={
        'your': yourQuote,
        'user':user,
        'count': count
    }
    return render(req, 'regis/user.html',context)

def submit(req):
    result = Quote.manager.createQuote(req.POST)
    if len(result):
        for tag, error in result.iteritems():
            messages.error(req, error, extra_tags=tag)
        return redirect('/success')
    else:
        user = User.manager.get(id=req.session['id'])
        Quote.manager.create(Quoted = req.POST['Quoted'], Message=req.POST['Message'], creater = user)

        return redirect('/success')

def logout(req):
    req.session.clear()
    return redirect('/')
# Create your views here.
