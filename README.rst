==========
Socialfeed
==========

Usage
=====
1. Add ``socialfeed`` to ``INSTALLED_APPS``
2. Run ``./manage.py migrate``
3. Define your providers in settings::

    SOCIALFEED_PROVIDERS = (
        'socialfeed.providers.instagram_hashtag',
        'socialfeed.providers.twitter_stream',
        'socialfeed.providers.youtube_channel',
    )
