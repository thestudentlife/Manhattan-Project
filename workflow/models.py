from django.db import models
from django.contrib.auth.models import User, Group
import datetime
from django.forms import ModelForm, EmailInput, TextInput, Textarea, PasswordInput, CharField, DateField
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse, reverse_lazy

class Profile(models.Model):
    user = models.OneToOneField(User,null=True)
    POSITIONS_CHOICES = (
        ('chief_editor', 'Editor-in-Chief'),
        ('editor', 'Section Editor'),
        ('photographer', 'Photographer'),
        ('author', 'Author'),
        ('graphic_designer', 'Graphic Designer'),
        ('web_developer', 'Web Developer'),
    )
    position = models.CharField(choices=POSITIONS_CHOICES, max_length=50, default='author')
    display_name = models.CharField(blank=True,max_length=50)
    legacy_id = models.PositiveIntegerField(null=True)

    def slug(self):
        return slugify(self.get_profile().display_name())

    def __str__(self):
        return self.display_name

    def is_editor(self):
        return "editor" in self.position

    def ideal_group_names(self):
        if self.position == 'chief_editor' or self.position == 'web_developer':
            return ['gold','silver','bronze']
        elif self.position == 'editor':
            return ['silver','bronze']
        else:
            return ['bronze']

    def get_absolute_url(self):
        return reverse('person', kwargs={'person_id': self.id})

    def get_highest_group(self):
        groups = self.user.groups.all();
        if Group.objects.all()[3] in groups:
            return 'gold'
        elif Group.objects.all()[2] in groups:
            return 'silver'
        elif Group.objects.all()[1] in groups:
            return 'bronze'
        elif Group.objects.all()[0] in groups:
            return 'plastic'
        else:
            return 'none'

class WArticle(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    article = models.OneToOneField('mainsite.Article')
    status = models.TextField()

    def __str__(self):
        return self.article.title

    def get_absolute_url(self):
        return reverse('warticle', kwargs={'issue_id': self.article.issue.id, 'pk': self.article.id})

class Revision(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    article = models.ForeignKey('mainsite.Article')
    editor = models.ForeignKey(Profile)
    body = models.TextField()

    def __str__(self):
        return str(self.date)

class Comment(models.Model):
    article = models.ForeignKey('mainsite.Article')
    author = models.ForeignKey(User)
    created_date = models.DateTimeField(default=datetime.datetime.now)

class Review(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    article = models.ForeignKey('mainsite.Article')
    reviewer = models.CharField(max_length=50)
    comment = models.TextField(blank=True)

class Assignment(models.Model):
    TYPES_CHOICES = (
        ('photo', 'Photo Assignment'),
        ('article', 'Article Assignment')
    )
    sender = models.ForeignKey(Profile, related_name="assignment_created")
    receiver = models.ForeignKey(Profile, related_name="assignment_received", null=True)
    title = models.CharField(max_length=200)
    type = models.CharField(choices=TYPES_CHOICES, max_length=50, default='photo_assignment')
    content = models.TextField(blank=True)
    section = models.ForeignKey('mainsite.Section')
    created_date = models.DateTimeField(default=datetime.datetime.now)
    due_date = models.DateTimeField(default=datetime.datetime.now)
    response_article = models.ForeignKey('mainsite.Article', related_name="assignment", null=True)
    response_photo = models.ForeignKey('mainsite.Photo', related_name="assignment", null=True)

    def progress(self):
        if self.response_article is not None or self.response_photo is not None:
            return "finished"
        elif self.receiver is not None:
            return "in progress"
        else:
            return "not started"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('assignment', kwargs={'assignment_id': self.id})

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={
                'required': True
            }),
            'password': PasswordInput(attrs={
                'required': True
            })
        }

class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'email': EmailInput(attrs={
                'required': True
            }),
            'first_name': TextInput(attrs={
                'required': True
            }),
            'last_name': TextInput(attrs={
                'required': True
            }),
            'password': PasswordInput(attrs={
                'required': True
            }),
        }

class RegisterForm2(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'email': EmailInput(attrs={
                'required': True
            }),
            'first_name': TextInput(attrs={
                'required': True
            }),
            'last_name': TextInput(attrs={
                'required': True
            }),
        }

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['position']

