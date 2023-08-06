#!/usr/bin/env python3

"""Provides generic methods for accessing version 1 of the API."""

from typing import Callable, List, Union

import wrapt

from .base import BaseApi


class NoNonPaginatedVersionError(Exception):
    """Raised when a non-paginated of a paginated-only method is called."""


def endpoint(endpoint_url):
    """Decorator for API methods. Denotes the URL endpoint."""

    @wrapt.decorator
    def wrapper(method, instance, args, kwargs):
        return instance.request(endpoint_url, *method(*args, **kwargs))

    return wrapper


def get_default_data(**kwargs):
    """Returns a POST data dict using default values."""
    limit = kwargs.get('limit', 20)
    offset = kwargs.get('offset', 0)
    direction = kwargs.get('direction', 'asc')
    if not isinstance(limit, int):
        raise TypeError("`limit` must be int")
    if not isinstance(offset, int):
        raise TypeError("`offset` must be int")
    if not direction in ('asc', 'desc'):
        raise ValueError("`direction` must be one of 'asc', 'desc'")
    return {'limit': limit, 'offset': offset, 'direction': direction}


class PaginatedMethod:
    """Object representing a method that has a POST paginated version (with
    args like limit, offset, direction) as well as optionally a GET
    non-paginated version. The GET version is accessed by calling the object as
    if it were a method. The POST version is accessed by calling the `verbose`
    attribute.
    """

    def __init__(self, method: Callable, verbose_only: bool = False):
        self._method = method
        self._verbose_only = verbose_only

    def __call__(self, *args, **kwargs):
        # Check if this method is only paginated
        # Pop the kwarg first as it must not reach the original method
        if not kwargs.pop('__verbose', False) and self._verbose_only:
            raise NoNonPaginatedVersionError(
                "{} does not have a non-paginated version - use {}.verbose() instead"
            )
        return self._method(*args, **kwargs)

    def verbose(self, *args, **kwargs):
        data = get_default_data(**kwargs)
        return self.__call__(*args, data=data, __verbose=True)


class Api(BaseApi):
    """API version 1"""

    version = 1

    def __init__(self, *args):
        super().__init__(*args)
        self.pages_since = PaginatedMethod(self._pages_since)
        self.page_revisions = PaginatedMethod(self._page_revisions)
        self.forum_threads_since = PaginatedMethod(
            self._forum_threads_since, True
        )
        self.thread_posts = PaginatedMethod(self._thread_posts)
        self.thread_posts_since = PaginatedMethod(
            self._thread_posts_since, True
        )
        self.wikidotuser_pages = PaginatedMethod(self._wikidotuser_pages)
        self.wikidotuser_posts = PaginatedMethod(self._wikidotuser_posts)
        self.wikidotuser_revisions = PaginatedMethod(
            self._wikidotuser_revisions
        )
        self.tags_pages = PaginatedMethod(self._tags_pages, True)

    def verbose(self, method: Callable, *args, **kwargs):
        """Returns a generator that iterates over a paginated method.

        callable `method`: The paginated method to iterate.
        Remaining arguments will be passed to this method.


        Pass this function int `limit`, an initial int `offset`, and str
        `direction`. Each time the returned generator is called, it will
        increment `offset` by `limit` and return the method for the resulting
        set of parameters. Effectively, applied to a paginated method, this
        generator is the same as turning the page.

            wiki = scuttle(domain, API_KEY, 1)
            generator = wiki.verbose(wiki.thread_posts, thread_id, limit=5)
            for posts in generator:
                print(len(posts))  # will be 5, except at very end

        Note that at the end of the data, the length of the final 'page' will
        very likely be less than `limit`.
        """
        if not isinstance(method, PaginatedMethod):
            raise TypeError("Iterated method must be a paginated method")
        data = get_default_data(**kwargs)

        def paginated_generator():
            limit: int = data['limit']
            length: int = limit
            offset: int = data['offset']
            direction: str = data['direction']
            while True:
                result = method.verbose(
                    *args, limit=limit, offset=offset, direction=direction
                )
                yield result
                if length < data['limit']:
                    return
                length = len(result)
                offset += length

        return paginated_generator()

    @endpoint("wikis")
    def wikis(self):
        return [None], None

    @endpoint("wiki")
    def wiki(self):
        return [None], None

    @endpoint("page")
    def pages(self):
        return [None], None

    @endpoint("page/since/{}")
    def _pages_since(self, since: int, *, data=None):
        if not isinstance(since, int):
            raise TypeError("`since` must be a UNIX timestamp")
        return [since], data

    @endpoint("page/{}")
    def page_by_id(self, page_id: int):
        return [page_id], None

    @endpoint("page/slug/{}")
    def page_by_slug(self, page_slug: str):
        return [page_slug], None

    @endpoint("page/{}/revisions")
    def _page_revisions(self, page_id: int, *, data=None):
        return [page_id], data

    @endpoint("page/{}/votes")
    def page_votes(self, page_id: int):
        return [page_id], None

    @endpoint("page/{}/tags")
    def page_tags(self, page_id: int):
        return [page_id], None

    @endpoint("page/{}/files")
    def page_files(self, page_id: int):
        return [page_id], None

    @endpoint("revision/{}")
    def revision(self, revision_id: int):
        return [revision_id], None

    @endpoint("revision/{}/full")
    def full_revision(self, revision_id: int):
        return [revision_id], None

    @endpoint("forum")
    def forums(self):
        return [None], None

    @endpoint("forum/{}")
    def forum(self, forum_id: int):
        return [forum_id], None

    @endpoint("forum/{}/threads")
    def forum_threads(self, forum_id: int):
        return [forum_id], None

    @endpoint("forum/{}/since/{}")
    def _forum_threads_since(self, forum_id: int, since: int, *, data):
        if not isinstance(since, int):
            raise TypeError("`since` must be a UNIX timestamp")
        return [forum_id, since], data

    @endpoint("thread/{}")
    def thread(self, thread_id: int):
        return [thread_id], None

    @endpoint("thread/{}/posts")
    def _thread_posts(self, thread_id: int, *, data=None):
        return [thread_id], data

    @endpoint("thread/{}/since/{}")
    def _thread_posts_since(self, thread_id: int, since: int, *, data):
        if not isinstance(since, int):
            raise TypeError("`since` must be a UNIX timestamp")
        return [thread_id, since], data

    @endpoint("post/{}")
    def post(self, post_id: int):
        return [post_id], None

    @endpoint("post/{}/children")
    def post_children(self, post_id: int):
        return [post_id], None

    @endpoint("post/{}/parent")
    def post_parent(self, post_id: int):
        return [post_id], None

    @endpoint("wikidotuser/{}")
    def wikidotuser(self, user_id: int):
        return [user_id], None

    @endpoint("wikidotuser/username/{}")
    def wikidotuser_name(self, wikidot_username: str):
        return [wikidot_username], None

    @endpoint("wikidotuser/{}/avatar")
    def wikidotuser_avatar(self, wikidot_user_id: int):
        return [wikidot_user_id], None

    @endpoint("wikidotuser/{}/pages")
    def _wikidotuser_pages(self, wikidot_user_id: int, *, data=None):
        if not isinstance(wikidot_user_id, int):
            raise TypeError("Wikidot user ID must be an int")
        return [wikidot_user_id], data

    @endpoint("wikidotuser/{}/posts")
    def _wikidotuser_posts(self, wikidot_user_id: int, *, data=None):
        if not isinstance(wikidot_user_id, int):
            raise TypeError("Wikidot user ID must be an int")
        return [wikidot_user_id], data

    @endpoint("wikidotuser/{}/revisions")
    def _wikidotuser_revisions(self, wikidot_user_id: int, *, data=None):
        if not isinstance(wikidot_user_id, int):
            raise TypeError("Wikidot user ID must be an int")
        return [wikidot_user_id], data

    @endpoint("wikidotuser/{}/votes")
    def wikidotuser_votes(self, wikidot_user_id: int):
        if not isinstance(wikidot_user_id, int):
            raise TypeError("Wikidot user ID must be an int")
        return [wikidot_user_id], None

    @endpoint("tag")
    def tags(self):
        return [None], None

    @endpoint("tag/{}/pages")
    def tag_pages(self, tag: str):
        """
        str `tag`: One tag, finds page IDs with that tag.
        """
        if not isinstance(tag, str):
            raise TypeError("A single tag must be a string")
        return [tag], None

    @endpoint("tag/pages")
    def _tags_pages(
        self, tags: Union[List[int], List[str]], operator: str = 'and', *, data
    ):
        """
        str[] `tags`: A list of tag names.
        int[] `tags`: A list of SCUTTLE tag IDs.
        str `operator`: 'and' or 'or'; defines how tags are combined.
        """
        if isinstance(tags, str):
            raise TypeError(
                "`tags` must be a list of at least one tag; use tag_pages() for a single tag name"
            )
        data['operator'] = operator
        if all(isinstance(tag, str) for tag in tags):
            data['names'] = tags
        elif all(isinstance(tag, int) for tag in tags):
            data['ids'] = tags
        else:
            raise TypeError("`tags` must be a list of str or int")
        return self.request("tag/pages", None, data)
