django-websocket
================

Introduction
------------

WSGI is thought to be largely incompatible with WebSockets, but that's not necessarily the case. As is shown by `gevent-websocket <https://pypi.python.org/pypi/gevent-websocket/>`_, you can get a really easy WSGI/WebSocket server running using gunicorn.


However, it would be really nice to be able to integrate a WebSocket server with Django. That is, not just have access to the Django models, but access to the whole Django infrastructure. Whilst it may not make much sense to use the template rendering, it certainly would be convenient to get access to the middleware and authentication from your django project. And being able to use the django form handling to validate user input means you can write more robust code.


This module allows you to do just that. You run a server alongside your normal WSGI server, that listens for WebSocket connection requests. An incoming connection is handled initially by the Django url routing facility (but with a seperate urlconf), and the Django middleware is applied. Then, your WebSocket view function is called, that handles the connection from that point on.


.. warning::

  This is still a work in progress. I'm not using it in any projects other than for testing. It may actually turn out not to be feasible to use this for production-level WebSockets, but I am still hopeful.


Playground
----------

Go into test_project::

  $ virtualenv .
  . bin/activate
  pip install -r requirements.txt

You will then need to have two shells open::

  ./project/manage.py runserver 0.0.0.0
  gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" project.wsgi:websocket -b 0.0.0.0:8001


Visit http://localhost:8000/chat/ to open a chat window.
  
You can have multiple windows in multiple browsers open, and chat between them.
You may change the user name, and the colour that the name should appear in.

There are a couple of other example WebSocket servers:

* http://localhost:8000/echo/ - Repeats back to you whatever you send to it.
* http://localhost:8000/ping/ - Respond with 'pong' if you send 'ping', and vice versa. Otherwise, don't respond at all.


Installation
------------

Install from PyPI using::

  $ pip install django-gevent-websocket

It will install it's various dependencies:

* django
* gevent-websocket
* gunicorn

Usage
-----

Settings
~~~~~~~~

Add the following to your ``$PROJECT_DIR/wsgi.py``::

  from django_websocket.wsgi import get_wsgi_websocket_application
  websocket = get_wsgi_websocket_application()

Add the following to your ``$PROJECT_DIR/settings.py``::

  WEBSOCKET_URLCONF = '<path-to-websocket-urlconf>'
  
A suggested urlconf would be ``$PROJECT_DIR/websocket_urls.py``.

You then need to add your WebSocket urls to that file: they will be very similar to your normal urls, but will only contain the endpoints that should accept a WebSocket connection::

  from django.conf.urls import patterns, url
  
  urlpatterns = patterns('',
      url(r'^chat/$', 'path.to.view', name='chat'),
  )

If you want to use ``{% websocket_url %}`` to get absolute urls that point to the correct WebSocket server and port, then you'll need to set

Views
~~~~~

A WebSocket view function looks very much like a normal django view function, indeed, it is called by the regular django request cycle, but it does not return an HttpResponse object. Instead, you grab the websocket object from the request, and ``.receive()`` data from it, or ``.send(data)`` to it.

To make things easier, you can use the decorators to wrap your views::

    from django_websocket.decorators import websocket
    
    @websocket
    def view_function(request, websocket, *args, **kwargs):
        # do stuff here.

This decorator adds the websocket as the second argument to your view: you still have the request object, allowing you to do things like permissions checking. You can still use any of the regular django decorators if you wish.

Asynchronicity in views
***********************

A WebSocket view should listen for incoming data from the client that needs to be processed, but will probably also want to be listening for data coming from another source, that will be sent back to the client.

A simple way to do this is to use the `select.select` function, and use this to write non-blocking code that waits for a signal to proceed. Typically, you'll want to loop until the websocket is closed, and then wait for a signal::

    from select import select
    
    from django_websocket.decorators import websocket
    
    @websocket
    def view_function(request, websocket):
        ws_sock = websocket.handler.socket.fileno()
        other_sock = ... # other socket to listen on.
        
        while not websocket.closed():
            fd = select([ws_sock, other_sock], [], [])[0][0]
            
            if fd == ws_sock:
                data = websocket.receive()
                # Deal with incoming data.
            else: ## fd == other_sock:
                # Deal with data from the other source
                websocket.send(message)

A good 'other' source might be a Redis PubSub subscription, which allows you to subscribe to channels, and will notify you when new data is available on any of these.

From ``django_websocket.servers.chat``::

    from select import select

    import redis

    from ..decorators import websocket

    @websocket
    def chat(request, websocket, *args, **kwargs):

        conn = redis.StrictRedis()
        subs = conn.pubsub()
        subs.subscribe('CHAT')
    
        def incoming():
            data = websocket.receive()
            if data:
                conn.publish('CHAT', data)
    
        def outgoing():
            msg_type, channel, message = subs.parse_response()
            if msg_type == 'message':
                websocket.send(message)
    
        sockets = {
            websocket.handler.socket.fileno(): incoming,
            subs.connection._sock.fileno(): outgoing
        }
    
        while not websocket.closed:
            fd = select(sockets.keys(), [], [])[0][0]
            sockets[fd]()


Template Tag
~~~~~~~~~~~~

Because you should have a different urlconf for your WebSocket views, you will need to use a slightly different template tag to get access to the WebSocket urls::

    {% load websockets %}
    
    <script>
      var ws = new WebSocket("{% websocket_url 'urlname' %}");
      
      // Do something with your shiny new WebSocket!
      // ws.send('foo');
    </script>



Starting the Server
~~~~~~~~~~~~~~~~~~~

You will need to start the ``geventwebsocket`` server seperately: there is no django management command (which mirrors the deprecation of run_gunicorn)::

  gunicorn -k "geventwebsocket.gunicorn.workers.GeventWebSocketWorker" $PROJECT_DIR.wsgi:websocket -b 127.0.0.1:8001

Note this runs on a different port than your django development server (or gunicorn in production). In production you will probably stick both of them behind an nginx proxy or similar. If you want to do this, you may have to do some tricky to get the splitting out of the websocket connections to work. I did something like::


  server {
    listen  80;
    proxy_set_header Host $host;
    
    location /static/ {
      alias ...
    }
    
    if ($http_upgrade) {
      rewrite ^(.*)$ /__ws__/$1 break;
    }
  
    location /__ws__/ {
      proxy_pass http://127.0.0.1:8001;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
      rewrite ^/__ws__/(.*)$ $1 break;
      return;
    }
    
    location / {
      proxy_pass http://127.0.0.1:8000;
    }
  }

Notice the double rewrite. It rewrites the url when the Upgrade header is present, and then rewrites it back, so that the url matches within django.
