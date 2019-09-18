#!/bin/sh
git checkout master

# generate documents
if [ "$1" = "apis" ]; then
  mkdir -p doc/apis
  for f in $(find src/apis -name "*.yaml"); do
    redoc-cli bundle $f -o doc/apis/$(basename $f .yaml).html
  done
  commit_msg="Update API documents [skip ci]"
else
  mkdir -p doc/umls
  for f in $(find src/umls -name "*.puml"); do
    curl http://www.plantuml.com/plantuml/png/$(cat $f | python pte.py) -Lo doc/umls/$(basename $f .puml).png
  done
  commit_msg="Update PlantUML documents [skip ci]"
fi

# commit & push
echo "machine github.com"   > ~/.netrc
echo "login $GIT_USER"     >> ~/.netrc
echo "password $GIT_TOKEN" >> ~/.netrc
git add doc -A
git config user.name "Travis.CI"
git config user.email "travis.auto.commit@localdomain"
git commit -m $commit_msg
git push -u origin master

# retry
if [ $? -ne 0 ]; then
  git fetch
  git rebase origin/master
  git push -u origin master
fi
