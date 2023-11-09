# api-gateway-reverse-proxy-python-flask
A simple API Gateway (reverse proxy) implementation in [python](https://www.python.org) using [requests](https://github.com/psf/requests) and [Flask](https://github.com/pallets/flask)

```bash
flask --app main run --port 8000
curl --location 'http://localhost:8000/does_not_exist/v1'
```
```
endpoint '/does_not_exist/v1' not found
```

```bash
curl --location 'http://localhost:8000/test_post_request/v1' \
--header 'Content-Type: application/json' \
--data '{
    "test": 123
}'
```

```
<returns response from https://httpbin.org/post>
```

Because an API-Gateway is by nature I/O-bound (i.e. it spends most of it's time waiting, as opposed to doing computation), it will strongly benefit from asynchronous workers, for example using [gunicorn](https://github.com/benoitc/gunicorn):

```bash
pip install gunicorn
pip install gevent
gunicorn --bind :8000 --workers 3 --worker-class=gevent --worker-connections=999 main:app
```

(refer to [gunicorn design docs](https://docs.gunicorn.org/en/stable/design.html) for more information)
