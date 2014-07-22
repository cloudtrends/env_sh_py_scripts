#!/bin/bash


cd ${GOPATH}/src/github.com/robfig/revel/revel

rm -f  ${GOPATH}/bin/revel

go build
go install


