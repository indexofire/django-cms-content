# -*- coding: utf-8 -*-
from django.core.cache import cache


def get_cache_or_query(cache_key, model, seconds_to_cache=900, **kwargs):
    """Cache key or get queryset
    
    Gets the query from cache or returns the orm.
        
    Example: 
    the_game = get_cache_or_query('game1', Game,
        seconds_to_cache=60*24*5, id=1)
        
    """

    q = cache.get(cache_key)
    if not q:
        q = model.objects.get(**kwargs)
        cache.set(cache_key, q, seconds_to_cache)
    return q
