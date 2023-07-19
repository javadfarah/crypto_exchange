#crypto_exchange
this repository represent the sample of ordering crypto.

how to run:

```
sudo docker-compose build
sudo docker-compose up -d
```

then open your browser on :

```
https://127.0.0.1:8000
https://0.0.0.0:8000
```

set crypto order end-point:

```
http://127.0.0.1:8000/api/v1/exchange/set_orders/
sample_post_data:

{
"crypto_name": "Bitcoin","crypto_amount": 1,
"user_id": 1
}
```

NOTICE:

```
1. the username and password is : username:admin password:123

1.at the first the user has no money you should increase money from admin panel

2.the api takes user_id as input it should be changed to take user_id from authenticated user

```
tests:
```
in the src root run folliwng command:
pytest -s  --reuse-db
```