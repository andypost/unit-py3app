#/bin/sh

apk add uv unit-python3 curl py3-psutil py3-flask py3-fastapi

uv venv --system-site-packages

unitd --no-daemon --log /dev/stdout &

while [ ! -S /run/control.unit.sock ]; do sleep 1; done

curl -v -X PUT --data-binary @conf.json --unix-socket /run/control.unit.sock http://localhost/config
curl --unix-socket /run/control.unit.sock http://localhost/status

curl http://localhost:8080/status
curl http://localhost:8081/status

curl --unix-socket /run/control.unit.sock http://localhost/control/applications/fastapi/restart

curl --unix-socket /run/control.unit.sock http://localhost/status

curl http://localhost:8080/stats
curl http://localhost:8081/stats

sleep infinite
