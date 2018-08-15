# wgadmin

```
python setup.py install
export WGADMIN_SESSION_KEY=`uuidgen`
wg-manage -c -d
wg-manage -l -s 192.168.0.0/24
wg-api
```

```
curl -X PUT -H 'Content-type: application/json' --data '{ "password": "123" }' http://localhost:5000/api/v1.0/user/admin
mysql -u root wgadmin -e 'UPDATE users SET role="admin" WHERE username="admin";'
TOKEN=$(curl -s -X POST -H 'Content-type: application/json' --data '{ "username": "admin", "password": "123" }' http://localhost:5000/api/v1.0/session | jq -r '.token')
curl -X POST -H 'Content-type: application/json' -H "Authorization: $TOKEN" --data '{"pubkey": "xTIBA5rboUvnH4htodjb6e697QjLERt1NAB4mZqp8Dg="}' http://localhost:5000/api/v1.0/user/me/pubkeys
curl -X POST -H 'Content-type: application/json' -H "Authorization: $TOKEN" --data '{"pubkey": "xTIBA5rboUvnH4htodjb6e697QjLERt1NAB4mZqp8Dg="}' http://localhost:5000/api/v1.0/user/me/lease
curl -X PUT -H 'Content-type: application/json' -H "Authorization: $TOKEN"  --data '{ "password": "123", "role": "server" }' http://localhost:5000/api/v1.0/user/aaaa
```
