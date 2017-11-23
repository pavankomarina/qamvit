from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect,HttpResponseRedirect
from .forms import UserdetailsForm,UserForm,QuestionForm,AnswerForm,BlogForm,TagForm
from .models import *
from django.contrib import messages

def logout_user(request):

    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'qa/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                name=request.user.username
                tags=Tags.objects.all()
                recent_questions=Questions.objects.all().order_by('id').reverse()[:4]
                most_likes=Answers.objects.all().order_by('likes').reverse()[:4]
                context={
                    'tags':tags,
                    'questions':recent_questions,
                    'most_likes':most_likes,
                        }

                return render(request, 'qa/home.html', context)
            else:
                return render(request, 'qa/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'qa/login.html', {'error_message': 'Invalid login'})
    return render(request, 'qa/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/userdetails/')

    context = {
        "form": form,
    }
    return render(request, 'qa/register.html', context)


def home(request):
    if request.method=="POST":
            form=TagForm(request.POST or None)
            if form.is_valid():
                tag_names=form.cleaned_data['tag_name']
                a=Tags(tag_name=tag_names)
                a.save()
    if request.user.is_authenticated():
        recent_questions=Questions.objects.all().order_by('id').reverse()[:4]
        most_likes=Answers.objects.all().order_by('likes').reverse()[:4]
        
        tags=Tags.objects.all()
        context={
        'tags':tags,
        'questions':recent_questions,
        'most_likes':most_likes,
        }
        return render(request, 'qa/home.html',context)
    else:
        return render(request,'qa/login.html')
    
def blog(request):
    if request.method=="POST":
        form=BlogForm(request.POST or None)
        if form.is_valid():

            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            users=Userdetails.objects.filter(user=request.user)
            # print(request.user)
            for i in users:
                usn=i.USN
            a=Userdetails.objects.filter(USN=usn)
            for i in a:
                id_user=i.user_id
            a=Blog(author=usn,title=title,content=content,user_details_id=id_user)
            a.save()
            messages.success(request,"Thank you for writing blog!")
            tags=Tags.objects.all()
            recent_questions=Questions.objects.all().order_by('id').reverse()[:4]
            most_likes=Answers.objects.all().order_by('likes').reverse()[:4]
            context={
                    'tags':tags,
                    'questions':recent_questions,
                    'most_likes':most_likes,
                        }
            return render(request,'qa/home.html',context)

    else:

        if request.user.is_authenticated():
            form=BlogForm(request.POST or None)
            blogs=Blog.objects.all()
            context={
            'blogs':blogs,
            'form':form,
            }
            return render(request,'qa/blog.html',context)
        else:
            return render(request,'qa/login.html')



def questions(request,tag_id):
    if request.method == "POST":
        form=QuestionForm(request.POST or None)
        if form.is_valid():
            users=Userdetails.objects.filter(user=request.user)
            for i in users:
                usn=i.USN
            question=form.cleaned_data['questionfield']
            c=Questions(questionfield=question,question_tag=Tags.objects.get(tag_id=tag_id),
                user_usn=Userdetails.objects.get(USN=usn))
            c.save()
            t=Tags.objects.get(tag_id=tag_id)
            t.no_of_questions=t.no_of_questions+1
            t.save()
            messages.success(request,"Thank you for asking question!")
            tags=Tags.objects.all()
            recent_questions=Questions.objects.all().order_by('id').reverse()[:4]
            most_likes=Answers.objects.all().order_by('likes').reverse()[:4]
            context={
                    'tags':tags,
                    'questions':recent_questions,
                    'most_likes':most_likes,
                        }
            return render(request,'qa/home.html',context)
    else:

        if request.user.is_authenticated():
            question_list=Questions.objects.filter(question_tag_id=tag_id)
            form=QuestionForm(request.POST or None)
            tag_here=Tags.objects.filter(tag_id=tag_id)
            context={
            'question_list':question_list,
            'form':form,
            'tag_id':tag_id,
            'tag_here':tag_here,

            }
            return render(request,'qa/questions.html',context)
        else:
            return render(request,'qa/login.html')



def answers(request,question_id):
    if request.method == "POST":
        form=AnswerForm(request.POST or None)
        if form.is_valid():
            users=Userdetails.objects.filter(user=request.user)
            for i in users:
                usn=i.USN
            question_details=Questions.objects.filter(id=question_id)
            for k in question_details:
                question_usn=k.user_usn_id
            if(usn==question_usn):
                messages.success(request,"Sorry you cannot answer the question you asked!!!")
                tags=Tags.objects.all()
                recent_questions=Questions.objects.all().order_by('id').reverse()[:4]
                most_likes=Answers.objects.all().order_by('likes').reverse()[:4]
                context={
                            'tags':tags,
                            'questions':recent_questions,
                            'most_likes':most_likes,
                        }
                return render(request,'qa/home.html',context)
            else:
                answer=form.cleaned_data['answer']
                p=Answers(answer=answer,written_by=Userdetails.objects.get(USN=usn),question_id=question_id)
                p.save()
                messages.success(request,"Thank you for answering question!")
                tags=Tags.objects.all()

                recent_questions=Questions.objects.all().order_by('id').reverse()[:4]


                most_likes=Answers.objects.all().order_by('likes').reverse()[:4]

                context={
                'tags':tags,
                'questions':recent_questions,
                'most_likes':most_likes,
                }
                return render(request,'qa/home.html',context)
    else:
        if request.user.is_authenticated():
            answers_list=Answers.objects.filter(question_id=question_id)
            question_here=Questions.objects.filter(id=question_id)
            form=AnswerForm(request.POST or None)
            # form2=CommentForm(request.POST or None)
            context={
            'answers_list':answers_list,
            'form':form,
            # 'form2':form2,
            'question_here':question_here,
            }
            return render(request,'qa/answers.html',context)
        else:
            return render(request,'qa/login.html')


def userdetails(request):
    if request.method == "POST":
        form=UserdetailsForm(request.POST or None)
        if form.is_valid():
            USN=form.cleaned_data['USN']
            name=form.cleaned_data['name']
            semester=form.cleaned_data['semester']
            branch=form.cleaned_data['branch']
            p=Userdetails(USN=USN,name=name,semester=semester,branch=branch,user=request.user)
            p.save()
            tags=Tags.objects.all()
            recent_questions=Questions.objects.all().order_by('id').reverse()[:4]
            most_likes=Answers.objects.all().order_by('likes').reverse()[:4]
            context={
                    'tags':tags,
                    'questions':recent_questions,
                    'most_likes':most_likes,
                        }
            return render(request,'qa/home.html',context)
    else:
        if request.user.is_authenticated():
            form=UserdetailsForm(request.POST or None)
            context={
            'form':form,
            }
            return render(request,'qa/userdetails.html',context)
        else:
            return render(request,'qa/login.html',{})


def like(request,answer_id):
    users=Userdetails.objects.filter(user=request.user)
    for i in users:
        usn=i.USN
    if Like.objects.filter(answer_id=answer_id,liked_user_usn=usn).exists():
        messages.success(request,"You had already liked the answer!")
        users=Userdetails.objects.filter(user=request.user)
        for i in users:
            usn=i.USN
        a=Answers.objects.get(id=answer_id)
        question_id=a.question_id
        answers_list=Answers.objects.filter(question_id=question_id)
        question_here=Questions.objects.filter(id=question_id)
        form=AnswerForm(request.POST or None)
        context={
            'answers_list':answers_list,
            'form':form,
            'question_here':question_here,
            }

        return render(request,'qa/answers.html',context)
    a=Answers.objects.get(id=answer_id)
    a.likes+=1
    a.save()
    users=Userdetails.objects.filter(user=request.user)
    for i in users:
        usn=i.USN
    k=Like(answer_id=answer_id,liked_user_usn=Userdetails.objects.get(USN=usn))
    k.save()
    a=Answers.objects.get(id=answer_id)
    question_id=a.question_id
    answers_list=Answers.objects.filter(question_id=question_id)
    question_here=Questions.objects.filter(id=question_id)
    form=AnswerForm(request.POST or None)
    context={
        'answers_list':answers_list,
        'form':form,
        'question_here':question_here,
        }
    return render(request,'qa/answers.html',context)


def profile(request):
    users=Userdetails.objects.filter(user=request.user)
    for i in users:
        usn=i.USN
    que_user=Questions.objects.filter(user_usn=usn)
    ans_user=Answers.objects.filter(written_by=usn)
    user_details=Userdetails.objects.filter(USN=usn)
    context={
    'que_user':que_user,
    'ans_user':ans_user,
    'userdetails':user_details,
    }
    return render(request,'qa/profile.html',context)