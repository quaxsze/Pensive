from app.models.post import Post


def test_create_post_model(app):
    with app.app_context():
        post = Post(title='test creation', content='test content creation',
                    remote_url='http://creation.local')
        post.save()

        fresh_post = Post.objects(id=post.id).first()
        assert fresh_post.title == 'test creation'
        assert fresh_post.content == 'test content creation'
        assert fresh_post.remote_url == 'http://creation.local'
