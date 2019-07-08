from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

import datetime


class Userdetails(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    USN = models.CharField(max_length=100, primary_key=True)
    semester = models.IntegerField(max_length=1)
    name = models.CharField(max_length=50)
    branch = models.CharField(max_length=20)

    def __str__(self):
        return self.USN


class Tags(models.Model):
    tag_id = models.AutoField(default=None, primary_key=True)
    tag_name = models.CharField(max_length=50)
    no_of_questions = models.IntegerField(default=0)

    def __str__(self):
        return self.tag_name


class Comments(models.Model):
    text = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    comment = GenericForeignKey()


class Questions(models.Model):
    question_tag = models.ForeignKey(
        Tags, on_delete=models.CASCADE, default=1, related_name='questions')
    user_usn = models.ForeignKey(Userdetails, on_delete=models.CASCADE)
    questionfield = models.CharField(max_length=200)
    no_of_answers = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today())
    comments = GenericRelation(Comments, related_query_name='questions')

    def __str__(self):
        return self.questionfield


class Answers(models.Model):
    answer = models.CharField(max_length=1000)
    question = models.ForeignKey(
        Questions, related_name="questions_id", on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    written_by = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today())
    comments = GenericRelation(Comments, related_query_name='answers')

    def __str__(self):
        return self.written_by


class Blog(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)
    user_details = models.ForeignKey(Userdetails, on_delete=models.CASCADE)
    comments = GenericRelation(Comments, related_query_name='blog')

    def __str__(self):
        return self.title


class Like(models.Model):
    answer_id = models.CharField(max_length=100)
    liked_user_usn = models.ForeignKey(Userdetails, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_id
