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
