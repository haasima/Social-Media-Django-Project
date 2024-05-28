from .base_case import BaseTest
from base.models import Comment
from base.forms import CommentForm


class TestComment(BaseTest):
    def test_comment(self):
        self.client.login(username=self.user.username, password='testing123321')
        
        comments_before = self.post.comments.first()
        
        self.assertEqual(comments_before, None)
        
        data = {
            "content": "Test Comment"
        }
        
        form = CommentForm(data=data)
        
        self.assertTrue(form.is_valid())
        
        Comment.objects.create(username=self.user,
                                content=data["content"],
                                post=self.post)
            
        comments_after = self.post.comments.first()
        
        self.assertNotEqual(comments_after, None)
        self.assertEqual(comments_after.content, data["content"])