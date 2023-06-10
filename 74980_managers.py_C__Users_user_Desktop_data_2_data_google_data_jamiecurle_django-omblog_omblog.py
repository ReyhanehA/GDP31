import operator
from collections import OrderedDict

from django.core.cache import cache
from django.db import models

from omblog.cache import get_key
from omblog import settings as o_settings


class TagManager(models.Manager):

    def tags_and_counts(self):
        """returns tags with count of how many posts are tagged with it"""
        if o_settings.CACHE_ENABLED:
            key = get_key('tags_and_counts')
            cached = cache.get(key)
            if cached:
                return cached
        tags = []
        tag_models = super(TagManager, self).get_query_set().all()

        for tag in tag_models:
            tags.append(
                (tag, tag.post_set.filter(status=3).count())
            )
        tags = sorted(tags, key=operator.itemgetter(1), reverse=True)

        if o_settings.CACHE_ENABLED:
            cache.set(key, tags, o_settings.CACHE_TIMEOUT)
        return tags


class PostManager(models.Manager):
    #
    # TODO: figure out how to decorate these
    # @cached('archive_dates)
    #
    def dates(self):
        """returns the years and months for which there are posts"""
        if o_settings.CACHE_ENABLED:
            key = get_key('posts_dates')
            cached = cache.get(key)
            if cached:
                return cached

        posts = self.published()
        dates = OrderedDict()
        for post in posts:
            key = post.created.strftime('%Y_%m')
            try:
                dates[key][1] = dates[key][1] + 1
            except KeyError:
                dates[key] = [post.created, 1]

        if o_settings.CACHE_ENABLED:
            cache.set(key, dates, o_settings.CACHE_TIMEOUT)
        return dates

    def published(self):
        """returns all published blog post"""
        if o_settings.CACHE_ENABLED:
            key = get_key('posts_published')
            cached = cache.get(key)
            if cached:
                return cached

        posts = super(PostManager, self).get_query_set().filter(
            status=self.model.PUBLISHED)

        if o_settings.CACHE_ENABLED:
            cache.set(key, posts, o_settings.CACHE_TIMEOUT)
        return posts

    def hidden(self):
        """returns all hidden blog posts"""
        if o_settings.CACHE_ENABLED:
            key = get_key('posts_hidden')
            cached = cache.get(key)
            if cached:
                return cached
        posts = super(PostManager, self).get_query_set().filter(
            status=self.model.HIDDEN)

        if o_settings.CACHE_ENABLED:
            cache.set(key, posts, o_settings.CACHE_TIMEOUT)
        return posts

    def visible(self, user):
        """returns all posts that are visible to the user"""
        posts = self.published()

        if o_settings.SHOW_HIDDEN_IF_LOGGED_IN and user.is_authenticated():
            posts = posts | self.hidden()

        return posts
