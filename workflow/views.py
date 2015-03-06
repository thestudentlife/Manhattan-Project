from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login as do_login, logout as do_logout
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from mainsite.models import Issue
from workflow.models import Assignment
# Create your views here.
from workflow.models import RegisterForm

def register(request):
    if request.method == "POST":
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            registerForm.save()
            return HttpResponse('Thanks for registering')
    else:
        registerForm = RegisterForm()
    return render(request, 'register.html', {
        'form': registerForm
    })

def home(request):
    issue = Issue.objects.all()[:1].get()
    return HttpResponse('This should be the latest issue.')

# issues
def issues(request):
    if request.user.has_perm(Permission.objects.get(codename="edit")):
        issues = Issue.objects.all()
        return HttpResponse('These are the issues.')
    else:
        return HttpResponse('You do not have permissions to see the issues.')

def issue(request, issue_id):
    if request.user.has_perm(Permission.objects.get(codename="edit")):
        issue = Issue.objects.get(pk=issue_id)
        return HttpResponse('This is issue ' + str(issue_id))
    else:
        return HttpResponse('You do not have permissions to access this particular issue.')

def new_issue(request):
    if request.user.has_perm(Permission.objects.get(codename="edit")):
        return HttpResponse('Create a new issue')
    else:
        return HttpResponse('You do not have permissions to create this new issue.')

#articles
def article(request, issue_id, article_id, article_name="default"):
    if request.user.has_perm(Permission.objects.get(codename="edit")):
        return HttpResponse('This is issue ' + str(issue_id) + " and article " + str(article_id) + ' with name ' + article_name)
    else:
        return HttpResponse('You do not have permissions to view ' + article_name + ' in issue ' + str(issue_id))

def new_article(request, issue_id):
    if request.user.has_perm(Permission.objects.get(codename="edit")):
        return HttpResponse('Create a new article in issue ' + str(issue_id))
    else:
        return HttpResponse('You do not have permissions to create a new article in issue ' + str(issue_id))

def edit_article(request, issue_id, article_id, article_name="default"):
    if request.user.has_perm(Permission.objects.get(codename="edit")):
        return HttpResponse('You are going to edit article ' + str(article_id) + ' with name ' + article_name)
    else:
        return HttpResponse('You do not have permissions to edit this article.')

def delete_article(request, issue_id, article_id, article_name="default"):
    if request.user.has_perm(Permission.objects.get(codename="edit")):
        return HttpResponse('You are going to delete article ' + str(article_id) + ' with name ' + article_name)
    else:
        return HttpResponse('You do not have permissions to delete ' + article_name)

#photos
def photos(request):
    return HttpResponse('These are the photos.')

def photo(request, photo_id):
    return HttpResponse('This is photo ' + str(photo_id))

def new_photo(request):
    return HttpResponse('Create a new photo')

def edit_photo(request, photo_id):
    return HttpResponse('You are going to edit photo ' + str(photo_id))

#assignments
def assignments(request):
    return HttpResponse('This should return all the assignments')

def assignment(request, assignment_id):
    return HttpResponse('This is assignment ' + str(assignment_id))

def new_assignment(request):
    return HttpResponse('Create a new assignment')

def edit_assignment(request, assignment_id):
    return HttpResponse('You are going to edit assignment ' + str(assignment_id))

def filter_by_receiver(request, maker_id):
    return HttpResponse('The assignments of the maker ' + str(maker_id))

def filter_by_section(request, section_name):
    return HttpResponse('The assignments of the section ' + str(section_name))

def filter_by_type(request, type_name):
    return HttpResponse('The assignments of the type ' + str(type_name))