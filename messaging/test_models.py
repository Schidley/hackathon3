from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class CustomUserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', first_name='Test', last_name='User', password='password')

    def test_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'Test User')


class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(author=self.user, content='This is a test post', interests='Testing')

    def test_post_creation(self):
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertEqual(self.post.content, 'This is a test post')
        self.assertEqual(self.post.interests, 'Testing')
        self.assertIsNotNone(self.post.created_at)

    def test_post_str(self):
        self.assertEqual(str(self.post), f"Post by {self.post.author.username} at {self.post.created_at}")


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(author=self.user, content='This is a test post')
        self.comment = Comment.objects.create(post=self.post, author=self.user, content='This is a test comment')

    def test_comment_creation(self):
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.author.username, 'testuser')
        self.assertEqual(self.comment.content, 'This is a test comment')
        self.assertIsNotNone(self.comment.created_at)

    def test_comment_str(self):
        self.assertEqual(str(self.comment), f"Comment by {self.comment.author.username} at {self.comment.created_at}")