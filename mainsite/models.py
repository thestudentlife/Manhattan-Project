import os
import autocomplete_light
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.forms import ModelForm, TextInput
from django.template.defaultfilters import slugify
from workflow.models import Profile, Assignment, WArticle
from django.core.urlresolvers import reverse, reverse_lazy
from workflow.models import Profile, Assignment, WArticle, Revision
import re
from django.core.exceptions import ValidationError
from geoposition.fields import GeopositionField

autocomplete_light.autodiscover()

class Section(models.Model):
    name = models.CharField(max_length=50)
    priority = models.IntegerField(blank=True, null=True)
    legacy_id = models.PositiveIntegerField(blank=True, null=True)
    def __str__(self):
        return self.name

    def slug(self):
        return slugify(self.name)

    def get_absolute_url(self):
        return reverse('section', kwargs={'section_slug': self.slug()})

class Subsection(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('section', kwargs={'section_name': self.name})

class Issue(models.Model):
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    legacy_id = models.IntegerField(null=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('issue', kwargs={'issue_id': self.id})

class Copy(models.Model):
    created_date = models.DateTimeField(default=datetime.datetime.now)
    file = models.FileField(upload_to='archives/')
    def __str__(self):
        return os.path.basename(self.file.name)

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    section = models.ForeignKey(Section, related_name='articles')
    issue = models.ForeignKey(Issue)
    authors = models.ManyToManyField(Profile)
    clicks = models.IntegerField(default=0)
    subsections = models.ManyToManyField(Subsection, null=True)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    updated_date = models.DateTimeField(default=datetime.datetime.now)
    legacy_id = models.PositiveIntegerField(null=True)
    position = GeopositionField(blank=True,null=True)
    edited_by = models.ManyToManyField(User,null=True,related_name='edited_article')
    def __str__(self):
        return self.title

    def content_with_no_images(self):
        return re.sub("<img[^>]*>","", re.sub("<a[^>]*>","", self.content));

    def has_photo(self):
        return self.album.photo_set is not None

    def disqus_id(self):
        if self.legacy_id:
            return "aardvark_"+str(self.legacy_id)
        else:
            return 'wolverine_'+str(self.id)

    def slug(self):
        return slugify(self.title)

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_id': self.id, 'section_name': self.section.slug()})

    def click(self):
        self.clicks += 1

    def length(self):
        str = self.content
        str_without_img_tags = re.sub("<img[^>]*>","", str)
        str_without_tags = re.sub("<[/]*\w+>","", str_without_img_tags)
        str_without_special_char = re.sub("&[^;]*;","", str_without_tags)
        return len(str_without_special_char.split())

class FrontArticle(models.Model):
    article = models.OneToOneField(Article)

    def __str__(self):
        return self.article.title

class CarouselArticle(models.Model):
    article = models.OneToOneField(Article)

    def __str__(self):
        return self.article.title

class Album(models.Model):
    article = models.OneToOneField(Article)

    def __str__(self):
        return self.article.title

class Photo(models.Model):
    def validate_image(fieldfile_obj):
        file_size = fieldfile_obj.file.size
        if file_size > 4096*4096:
            raise ValidationError("Max file size is 4MB")
    def validate_height(value):
        if value > 3000:
            raise ValidationError("Max height is 3000px")
    def validate_width(value):
        if value > 4000:
            raise ValidationError("Max width is 4000px")
    image = models.ImageField(upload_to='photo/',height_field = 'height',
                              width_field = 'width',validators=[validate_image])
    height = models.IntegerField(blank=True,validators=[validate_height])
    width = models.IntegerField(blank=True,validators=[validate_width])
    date = models.DateTimeField(default=datetime.datetime.now)
    thumbnail = models.ImageField(upload_to='thumbs/',blank=True,null=True)
    caption = models.TextField(max_length=100, blank=True)
    credit = models.ForeignKey(Profile)
    album = models.ForeignKey(Album, null=True)

    # Adapted from http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/
    def create_thumbnail(self):

        if not self.image:
            return

        from io import BytesIO
        from PIL import Image
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        THUMBNAIL_SIZE = (300,300)

        from mimetypes import MimeTypes
        mime = MimeTypes()
        mime_type = mime.guess_type(self.image.url)

        DJANGO_TYPE = mime_type
        if DJANGO_TYPE[0] == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE[0] == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
        else:
            return

        r = BytesIO(self.image.read())
        fullsize_image = Image.open(r)
        image = fullsize_image.copy()

        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)
        self.thumbnail.save('{}_thumbnail.{}'.format(os.path.splitext(suf.name)[0], FILE_EXTENSION), suf, save=False)


    def save(self):
        self.create_thumbnail()
        super(Photo, self).save()

    def __str__(self):
        return self.image.url

# The assignment form is currently in the mainsite
# because of a circular dependency on Section.
# Ideally, this class should be moved back to workflow/models.
class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'content', 'type', 'receiver', 'due_date']
        widgets = {
            'due_date': TextInput(attrs={
                'type': 'date',
            })
        }

class ArticleForm(autocomplete_light.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'section', 'issue','authors','position']
        autocomplete_fields = ('authors')








