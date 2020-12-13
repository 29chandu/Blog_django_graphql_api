# Blog_django_graphql_api
Blog application graphql api with Django and graphene


# Example query and mutations:

# Queries

  query post {
    post(id: 2) {
      title
      description
    }
  }

  query post {
    post(id: 1) {
      title
      description
      commentSet {
        id
        text
      }
    }
  }


# Mutations

  mutation createPost {
    createPost(input: {
      title: "Fury"
      description: "Tank war movie"
      author: {
        name: "brad pitt"
      }
    }) {
      ok
      post {
        id
        publishDate
      }
    }
  }

  mutation updatePost {
    updatePost(id: 2
    input: {
      title: "enemy at the gates",
      author: {
        id: 5
      }
    }) {
      ok
      post {
        title
        description
        author {
          id
          name
        }
      }
    }
  }

  mutation createComment {
    createComment(
      input: {
        text: "This is a wonderfull movie"
        author: {
          id: 1
        }
        post: {
          id: 1
        }
      } 
    ) {
      ok
      comment {
        id
      }
    }
  }

  mutation {
    createComment(input: {
      text: "This is wonderfull movie"
      post: {
        id: 1
      }
      author: {
        name: "shama"
      }
    }) {
      ok
      comment {
        id
      }
    }
  }

  mutation deleteComment {
    deleteComment(id: 42) {
      ok
    }
  }

