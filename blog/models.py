from django.db import models

class Author(models.Model):
  name =  models.CharField(max_length=50)

  def __str__(self):
    return f'{self.name}'

class Post(models.Model):
  title = models.CharField(max_length=120)
  description = models.TextField(max_length=256)
  publish_date = models.DateField(auto_now_add=True)
  author = models.ForeignKey(Author, on_delete=models.CASCADE)
  # author = models.CharField(max_length=200)

  def __str__(self):
    return self.title

class Comment(models.Model):
  text = models.CharField(max_length=150)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  author = models.ForeignKey(Author, on_delete=models.CASCADE)
  # author = models.CharField(max_length=200)

  def __str__(self):
    return f'{self.text[:15]}... {self.author}'


