PornHub Unofficial API
======================

Unofficial API for pornhub.com in Python

Usage
-----

**Create client**

.. code-block:: python

    import pornhub
    client = pornhub.PornHub()
    
**Create client with proxy**

.. code-block:: python

    import pornhub
    client = pornhub.PornHub("5.135.164.72", 3128)
    #With proxy, given a Proxy IP and Port. For the countries with restricted access like Turkey, etc.

**Grab stars**

.. code-block:: python

    for star in client.getStars(10):
        print(star)
        print(star["name"])

**Create client with search keywords**

.. code-block:: python

    keywords = ["word1", "word2"]
    client = pornhub.PornHub(keywords)

    for video in client.getVideos(10,page=2):
        print(video)
        print(video["url"])


License
-------

MIT license
