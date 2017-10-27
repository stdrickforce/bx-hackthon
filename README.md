# bx-hackthon
二楼大柱子旁边队

## Development

```bash
make dev
```

## Python requirements

* tensorflow
* numpy
* thriftpy
* gunicorn\_thrift

## Run python server

```bash
cd python
gunicorn_thrift -b 0.0.0.0:9099 -c gnicorn_thrift.py
```

## Run python client demo

```bash
cd python
python client.py
```

## Toggle from image to bytes

see `str2image` and `image2str`

## Go RPC

There is a simple demo in `golang/main.go`

You can rebuild thrift helper classes by the following command:

```bash
generator hackthon.thrift golang/src
```

Maybe you have to install some dependencies at first:

```bash
go get github.com/samuel/go-thrift/generator
go get github.com/samuel/go-thrift/thrift
```

`$GOPATH` is also required to be set

```bash
export GOPATH=$GOPATH:`pwd`/golang
```

Well, I really recommend to use `direnv` command to manage $GOPATH.

There is also a .envrc file under the golang directory.
