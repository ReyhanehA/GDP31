import ccsitemaps
from omblog.models import Post


class PostSiteMap(ccsitemaps.SiteMap):
    model = Post

    @staticmethod
    def last_mod():
        try:
            last_mod = Post.objects\
                .published()\
                .order_by('-created')[0]
            return last_mod.created
        except IndexError:
            return None

    @staticmethod
    def get_objects():
        return Post.objects.published()

ccsitemaps.register(PostSiteMap)
