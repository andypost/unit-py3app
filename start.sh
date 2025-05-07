#/bin/sh

docker run --rm -it \
    -v $(pwd):/opt -w /opt \
    -p 8080:8080 -p 8081:8081 \
    alpine:edge \
    /bin/ash up.sh