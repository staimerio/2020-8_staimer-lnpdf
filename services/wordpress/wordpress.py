"""Services for wordpress controller"""

# Retic
from retic import env, App as app

# Requests_oauthlib
from requests_oauthlib import OAuth1

# Requests
import requests

# Services
from retic.services.responses import error_response_service, success_response_service

# Constants
URL_API_BASE = app.apps['backend']['lnpdf']['base_url']
URL_API_BASE_POSTS = URL_API_BASE+"/posts"


OAUTH_SESSION = OAuth1(
    app.config.get('OAUTH_CONSUMER_KEY'),
    app.config.get('OAUTH_CONSUMER_SECRET'),
    app.config.get('OAUTH_TOKEN'),
    app.config.get('OAUTH_TOKEN_SECRET'),
)


def create_resource(
    name,
    slug="",
    meta=None,
    resource="tags",
):
    """Define the metadata"""
    try:
        _metadata = {
            "name": str(name).lower(),
            "slug": slug,
            "meta": meta if meta else {}
        }
        """Prepare payload for the request"""
        _url = "{0}/{1}".format(
            URL_API_BASE,
            resource
        )
        """Create the resource, if it has any problem, return None"""
        req_resource = requests.post(
            _url,
            auth=OAUTH_SESSION,
            json=_metadata
        )
        """Return the data"""
        return req_resource.json()
    except Exception as e:
        return None


def create_post(
        title,
        slug,
        content,
        excerpt,
        categories,
        tags,
        types,
        genres,
        meta,
        date,
):
    try:
        """Get and create the ids tag list, if it already exist, don't create it"""
        _tags_id = create_resources_from_list(tags, 'tags')

        """Get and create the ids category list, if it already exist, don't create it"""
        _categories_id = create_resources_from_list(categories, 'categories')

        """Get and create the ids type list, if it already exist, don't create it"""
        _types_id = create_resources_from_list(types, 'types')

        """Get and create the ids genre list, if it already exist, don't create it"""
        _genres_id = create_resources_from_list(genres, 'genres')

        """Prepare payload request"""
        _payload = {
            "content": content,
            "title": title,
            "excerpt": excerpt,
            "status": "draft",
            "categories": _categories_id,
            "tags": _tags_id,

            u'types': _types_id,
            u'genres': _genres_id,

            "meta": meta,
            "slug": slug
            # "date": date
        }
        """Create a new post"""
        _req_post = requests.post(
            URL_API_BASE_POSTS,
            auth=OAUTH_SESSION,
            json=_payload
        )
        """Return the created post"""
        return success_response_service(
            data=_req_post.json()
        )
    except Exception as err:
        return error_response_service(
            msg=str(err)
        )


def update_post(
        post_id,
        data
):
    try:
        """Prepare payload"""
        _url = "{0}/{1}".format(URL_API_BASE_POSTS, post_id)
        _payload = {
            **data
        }
        """Update a post"""
        _req_post = requests.post(
            _url,
            auth=OAUTH_SESSION,
            json=_payload
        )
        """Return the created post"""
        return success_response_service(
            data=_req_post.json()
        )
    except Exception as err:
        return error_response_service(
            msg=str(err)
        )


def get_post_by_id(
        post_id,
):
    try:
        """Prepare payload"""
        _url = "{0}/{1}".format(URL_API_BASE_POSTS, post_id)
        """Update a post"""
        _req_post = requests.get(
            _url,
            auth=OAUTH_SESSION,
        )
        """Return the created post"""
        return success_response_service(
            data=_req_post.json()
        )
    except Exception as err:
        return error_response_service(
            msg=str(err)
        )


def create_resources_from_list(items, resource):
    """Create resource in based a list

    : param items: List of items that you can created o find
    : param resource: Tag of the kind of resource
    """
    _items = []
    for _item in items:
        _value = create_resource(**_item, resource=resource)
        _items.append(
            _value['data']['term_id'] if (
                "data" in _value) else _value['id']
        )
    return _items
