from django.db import models
from authen.models import User
from model_utils import Choices


class Tag(models.Model):
    name = models.CharField(max_length=50)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tag_creator')
    create_on = models.DateTimeField(auto_now_add=True)
    update_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='tag_editor')
    update_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cat_creator')
    create_on = models.DateTimeField(auto_now_add=True)
    update_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cat_editor')
    update_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    STATUS = Choices('draft', 'published', 'deleted')

    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    create_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(blank=True, null=True)
    private = models.BooleanField(default=False)
    category = models.ForeignKey(Category, to_field='id', on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="blogs")
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='author')
    update_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='editor', null=True, blank=True)
    status = models.CharField(choices=STATUS, default=STATUS.draft, max_length=20)

    class Meta:
        ordering = ["-create_on"]

    def __str__(self):
        return self.title
