# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt, re


class UserManager(models.Manager):
    def validate(self, postData):
        errors = []
        if len(postData['name']) < 3:
            errors.append("Name can not be less than 3 characters")
        
        if len(postData['username']) < 3:
            errors.append("Username can not be less than 3 characters") 
        
        if (User.objects.filter(username=postData['username'])):
            errors.append("Username already in use")

        if len(postData["password"]) < 8:
            hashpwd = bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt())
            # set old password to hashpwd and save to db, BUT HOW?    
            errors.append("Password must be at least 8 characters")

        if postData["password"] != postData["password2"]:
            errors.append("Passwords do not match")  
        
        return errors

    def loginvalidate(self, postData): # check db username with submitted username
        # print postData['username']
        errors = []
        
        if len(postData['username']) < 1:
            errors.append("Please enter your username")

        if len(postData["password"]) < 8:
            errors.append("Please enter your password")

        if (User.objects.filter(username=postData['username'])):
            print 'TRUE for username'
            currentuser = User.objects.get(username=postData['username'])
            existingpwd = currentuser.password
        
            if not bcrypt.checkpw(postData["password"].encode(), existingpwd.encode()):
                errors.append("Password does not match")
        else:
            errors.append("Username does not match")
        
        return errors

class WishManager(models.Manager):
    def validate(self, postData):
        errors = []

        if len(postData['item']) < 1:
            errors.append("Please enter an item name")

        if len(postData['item']) < 4:
            errors.append("Please enter an item name with more than 3 characters")  

        return errors    

class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    hiredate = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()

class Wish(models.Model):
    item = models.CharField(max_length=45)
    favorite = models.ManyToManyField(User, related_name='upvote')
    created_by = models.ForeignKey(User, related_name='admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WishManager()