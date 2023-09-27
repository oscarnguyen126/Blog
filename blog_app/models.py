from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    create_on = models.DateField(auto_now_add=True)
    update_on = models.DateField(blank=True, null=True)
    private = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ["create_on"]

    def __str__(self):
        return self.title
