package main

import (
	"hackthon_thrift"
	"net"

	"github.com/stdrickforce/go-thrift/thrift"
)

const (
	IMAGE = "/Users/stdrickforce/workspace/bx-hackthon/python/mosaic"
)

func client() hackthon_thrift.Hackthon {
	conn, err := net.Dial("tcp", "localhost:9099")
	if err != nil {
		panic(err)
	}

	var t = thrift.NewTransport(
		conn,
		thrift.BinaryProtocol,
	)
	var c = thrift.NewClient(t, false)
	var client = hackthon_thrift.HackthonClient{Client: c}
	return &client
}

func main() {
	var c = client()
	c.Ping()
}
