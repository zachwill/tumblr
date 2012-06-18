"""
Functionality for Tumblr's API.
"""

import os
import requests as req
import simplejson as json
from oauth_hook import OAuthHook


def auth():
    """Return an authorized requests client."""
    key = os.getenv('TUMBLR_CONSUMER_KEY')
    secret = os.getenv('TUMBLR_CONSUMER_SECRET')
    oauth_token = os.getenv('TUMBLR_OAUTH_KEY')
    oauth_secret = os.getenv('TUMBLR_OAUTH_SECRET')
    oauth =  OAuthHook(key, secret, oauth_token, oauth_secret, True)
    return req.session(hooks={'pre_request': oauth})


def endpoint(name, *args):
    """Return a Tumblr API endpoint."""
    name = "%s.tumblr.com" % name
    url = ["http://api.tumblr.com/v2/blog", name]
    url.extend(args)
    return "/".join(url)


def post(name, *args, **params):
    """Perform a POST request on the Tumblr API."""
    client = auth()
    url = endpoint(name, *args)
    response = client.post(url, params=params)
    return json.loads(response.text)


def submit(name, **params):
    """Submit a blog post."""
    if 'type' not in params:
        params['type'] = 'text'
    if 'tags' in params:
        tags = params.pop('tags')
        params['tags'] = ','.join(tags)
    return post(name, 'post', **params)
