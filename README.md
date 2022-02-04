Creación usuarios y posts:
```
python manage.py shell
from blog.models import Post
from django.contrib.auth.models import User
for i in range(5):
    user = User.objects.create(username='test%s' % i, is_staff=True)
    user.set_password("asdfasdfasdf")
    user.save()
    for n_post in range(20): #(20 por usuario = 100 posts)
        post = Post.objects.create(author=user, title='Sample title%s' % n_post, text='Test')
        post.publish()
```
