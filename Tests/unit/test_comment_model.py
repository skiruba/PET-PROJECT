from models import Comment

def test_comment_model():
    comment = Comment('Hello World', 1, 1)

    assert comment.comment_content == 'Hello World'
    assert comment.author_id == 1
    assert comment.post_id == 1
    