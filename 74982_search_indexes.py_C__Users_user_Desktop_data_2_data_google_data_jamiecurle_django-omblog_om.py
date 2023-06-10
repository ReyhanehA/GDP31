from haystack import indexes
from haystack import site
from omblog.models import Post


class PostIndex(indexes.SearchIndex):
    text = indexes.CharField(
        document=True,
        use_template=True)
    title = indexes.CharField(
        model_attr='title')
    description = indexes.CharField(
        model_attr='description')
    created = indexes.DateTimeField(
        model_attr='created')

    def index_queryset(self):
        return Post.objects.filter(status=Post.PUBLISHED)

site.register(Post, PostIndex)
