rm -rf app  &&
mkdir app  &&
cp ../run.py app/run.py  &&
cp ../sprider.py app/sprider.py  &&
cp -r ../conf app/conf  &&
cp -r ../entity app/entity  &&
cp -r ../template app/template  &&
mkdir app/log  &&
mkdir app/files  &&
cp ../requirement.txt app/requirement.txt  &&
docker build -t dockerhub.datagrand.com/data-dev/dingding_sprider:20200114:1140 . &&
rm -rf app