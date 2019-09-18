#!/bin/sh
yarn global add redoc-cli
apk add python curl

for f in $(find src/apis -name "*.yaml"); do
  redoc-cli bundle $f -o docs/apis/$(basename $f .yaml).html
done

for f in $(find src/umls -name "*.puml"); do
  curl http://www.plantuml.com/plantuml/png/$(cat $f | python pte.py) -Lo docs/umls/$(basename $f .puml).png
done
