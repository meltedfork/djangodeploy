# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Wish


def index(request):
    if 'userid' in request.session:
       return redirect("/success") 
    else:
        print 'hello from login index'
        return render(request, 'index.html')

def register(request):
    errors = User.objects.validate(request.POST)
    print 'this process works', request.POST
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect("/")
    else:
        hashpwd = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
        newuser = User.objects.create(
            name=request.POST['name'],
            username=request.POST['username'],
            hiredate=request.POST['hiredate'],
            password=hashpwd)

        request.session['userid'] = newuser.id
        request.session['name'] = newuser.name
        print "session info", newuser.id, newuser.name
        return redirect("/success")

def login(request):
    # print postData['email']
    errors = User.objects.loginvalidate(request.POST)
    
    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect("/")
    else:
        user = User.objects.filter(username=request.POST['username'])[0]
        request.session['userid'] = user.id
        request.session['name'] = user.name
        return redirect("/success")

def success(request):
    userid = request.session['userid']
    print 'person in session: userid: ', userid
    user = User.objects.get(id=userid)
    favorite = user.upvote.all()
    mywish = Wish.objects.filter(created_by=user)
    items = Wish.objects.all().exclude(favorite=user).exclude(created_by=user) 
    # print 'success method: user, favorite, others: '
    context = {
        'user': user,
        'items': items,
        'favorite': favorite, 
        'mywish': mywish  
    }
    print 'this is context: ', context
    return render(request, 'wishlist.html', context)

def logout(request):
    request.session.clear()
    print 'goodbye'
    return redirect('/')   

def new(request):
    print 'we hit the new route'
    return render(request, 'newitem.html')    

def create(request):
    print 'create method: send the form to db'
    errors = Wish.objects.validate(request.POST)

    if len(errors) > 0:
        for error in errors:
            messages.error(request, error)
        return redirect('/new')
    else:
        userid = request.session['userid']
        user = User.objects.get(id=userid)
        Wish.objects.create(
            item=request.POST['item'],
            created_by=user)

        return redirect('/success')

def favorite(request, id):
    print 'arrived at favorite method with id #: ', id 
    userid = request.session['userid'] 
    mywish = Wish.objects.get(id=id)
    mywish.favorite.add(userid)  
    mywish.save()
    return redirect('/success')

def popback(request, id):
    print 'arrived at popback method with id#: ', id
    userid = request.session['userid'] 
    mywish = Wish.objects.get(id=id)
    mywish.favorite.remove(userid)  
    mywish.save()    
    return redirect('/success')

def show(request, id):
    print 'arrived at the show method'
    print 'need to add form in show'
    #oneuser = User.objects.filter()
    wish = Wish.objects.get(id=id)
    users = wish.favorite.all()
    creator = wish.created_by.name
    #creator = Wish.objects.filter(created_by=oneuser)
    print 'creator is: ', creator
    context = {
        'wish': wish,
        'users': users,
        'creator': creator
    }

    return render(request, 'show.html', context)

def remove(request, id):
    userid = request.session['userid']
    wish = Wish.objects.get(id=id)
    if wish.created_by_id == userid:
        return redirect('/'+id+'/delete')

    else:
        print 'need to show remove error'
        error = 'unauthorized user. you may only delete wishes you create'
        messages.error(request, error)
        return redirect('/success')   

def destroy(request, id):
    print 'delete / destroy method'
    destroy_a_wish = Wish.objects.get(id=id)
    destroy_a_wish.delete()
    return redirect('/success')


