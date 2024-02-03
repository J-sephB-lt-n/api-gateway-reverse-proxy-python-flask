# api-gateway-reverse-proxy-python-flask
A simple API Gateway (reverse proxy) implementation in [python](https://www.python.org) using [requests](https://github.com/psf/requests) and [Flask](https://github.com/pallets/flask)

Note that there are certain HTTP functions which have not been handled in this simple implementation (e.g.forwarding client headers). 

```bash
~$ flask --app gateway run --port 5000 &
~$ curl --location 'http://localhost:5000/does_not_exist/v1'
endpoint '/does_not_exist/v1' not found
~$ curl -X POST --location 'http://localhost:5000/test_post_request/v1' --header 'Content-Type: application/json' --data '{"test": 123}'
<returns response from https://httpbin.org/post>
~$ pkill -f flask -SIGTERM
```

Because an API-Gateway is by nature I/O-bound (i.e. it spends most of it's time waiting, as opposed to doing computation), it will strongly benefit from asynchronous workers, for example using [gevent](https://github.com/gevent/gevent):

```bash
pip install gunicorn
pip install gevent
gunicorn --bind :8000 --workers 3 --worker-class=gevent --worker-connections=999 main:gateway
```

(refer to [gunicorn design docs](https://docs.gunicorn.org/en/stable/design.html) for more information)

Here is a more complete gateway example:

```bash
# start local flask servers (in the background) #
flask --app gateway run --port 5000 &
flask --app endpoints run --port 8000 &

# send some requests through the gateway #
curl -X POST --location 'http://localhost:5000/return_to_sender/v1?key=test' --header 'Content-Type: application/json' --data '{"test": 123}'

# stop local flask servers #
pkill -f flask -SIGTERM
```
