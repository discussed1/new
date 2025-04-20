from core.models import Post, Comment
posts = Post.objects.all()
for p in posts:
    count = Comment.objects.filter(post=p).count()
    if count > 0:
        print(f'ID: {p.id}, Title: {p.title}, Comments: {count}')
