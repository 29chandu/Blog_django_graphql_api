import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField

from .models import Post, Author, Comment

class PostType(DjangoObjectType):
  class Meta:
    model = Post
    # fields = ['title', 
    # 'description', 'publish_date', 'author']

class CommentType(DjangoObjectType):
  class Meta:
    model = Comment
    # fields = ['text', 'post', 'author']

class AuthorType(DjangoObjectType):
  class Meta:
    model = Author
    # fields = ['name']

class Query(graphene.ObjectType):
  posts = graphene.List(PostType)
  post = graphene.Field(PostType, id=graphene.Int())

  def resolve_posts(root, info):
    return Post.objects.all()

  def resolve_post(root, info, **kwargs):
    id = kwargs.get('id')
    post_obj = None

    if id is not None:
      try:
        post_obj = Post.objects.get(pk=id)
      except:
        pass
    
    return post_obj


# Mutations
class AuthorInput(graphene.InputObjectType):
  id = graphene.ID()
  name = graphene.String()

class PostInput(graphene.InputObjectType):
  id = graphene.ID()
  title = graphene.String()
  description = graphene.String()
  publish_date = graphene.Date()
  author = graphene.Field(AuthorInput)

class CommentInput(graphene.InputObjectType):
  id = graphene.ID()
  text = graphene.String()
  post = graphene.Field(PostInput)
  author = graphene.Field(AuthorInput)


class CreatePost(graphene.Mutation):
  class Arguments:
    input = PostInput(required=True)

  ok = graphene.Boolean()
  post = graphene.Field(PostType)

  @staticmethod
  def mutate(root, info, input=None):
    ok = True
    if input.author:
      if input.author.id:
        try:
          author_obj = Author.objects.get(pk=input.author.id)
        except:
          pass
      if input.author.name:
        author_obj = Author(name=input.author.name)
        author_obj.save()
    post_obj = Post(title=input.title, description=input.description,
    publish_date=input.publish_date, author=author_obj)
    post_obj.save()
    return CreatePost(ok=ok, post=post_obj)

class UpdatePost(graphene.Mutation):
  class Arguments:
    id = graphene.Int(required=True)
    input = PostInput(required=True)

  ok = graphene.Boolean()
  post = graphene.Field(PostType)

  @staticmethod
  def mutate(root, info, id, input=None):
    ok = False
    post_obj = None
    author_obj = None
    try: 
      post_obj = Post.objects.get(pk=id)
    except:
      pass

    if post_obj:
      ok = True
      if input.title:
        post_obj.title = input.title
      if input.description:
        post_obj.description = input.description
      if input.publish_date:
        post_obj.publish_date = input.publish_date

      if input.author:
        if input.author.id:
          try:
            author_obj = Author.objects.get(pk=input.author.id)
          except:
            pass
          if author_obj:
            post_obj.author = author_obj

      post_obj.save()
      return UpdatePost(ok=ok, post=post_obj)
    return UpdatePost(ok=ok, post=None)

class CreateComment(graphene.Mutation):
  class Arguments:
    input = CommentInput(required=True)

  ok = graphene.Boolean()
  comment = graphene.Field(CommentType)

  @staticmethod
  def mutate(root, info, input=None):
    ok = False
    author_obj = None
    post_obj = None
    comment_obj = None

    if input.author:
      if input.author.id:
        try:
          author_obj = Author.objects.get(pk=input.author.id)
        except:
          pass
      if input.author.name:
        author_obj = Author(name=input.author.name)
        author_obj.save()
    else:
      comment_obj = None

    if input.post.id:
      try:
        post_obj = Post.objects.get(pk=input.post.id)
      except:
        pass

    if author_obj and post_obj:
      comment_obj = Comment(text=input.text, post=post_obj, author=author_obj)
      comment_obj.save()
      ok = True
    
    return CreateComment(ok=ok, comment=comment_obj)

class DeleteComment(graphene.Mutation):
  class Arguments:
    id = graphene.Int()

  ok = graphene.Boolean()
  # comment = graphene.Field(CommentType)

  @staticmethod
  def mutate(root, info, id):
    ok = False
    comment_obj = None
    
    if id:
      try:
        comment_obj = Comment.objects.get(pk=id)
      except:
        pass

      if comment_obj:
        comment_obj.delete()
        ok = True

    return DeleteComment(ok=ok)

class Mutation(graphene.ObjectType):
  create_post = CreatePost.Field()
  update_post = UpdatePost.Field()
  create_comment = CreateComment.Field()
  delete_comment = DeleteComment.Field()



schema = graphene.Schema(query=Query, mutation=Mutation)
