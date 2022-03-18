#!/bin/bash

files=($(ls ./docs | grep "_doc.txt"))
mkdir output
for file in ${files[@]}; do
  echo $file
  /metamap/public_semrep/bin/semrep.v1.8 -L 2018 -Z 2018AA -F ./docs/$file output/$file
done
