#!/bin/bash

released=$(curl --silent https://archive.apache.org/dist/activemq/ | grep href | grep -v apache | grep -v KEYS | grep -v activemq | grep -v artemis | grep -v pre | awk '{print $5}' | sed -e 's/.*>\(.*\)\/<\/a>/\1/' | sort -t "." -k1,1n -k2,2n -k3,3n)
echo Released versions: $released

remote=$(curl -L -s 'https://registry.hub.docker.com/v2/repositories/butkovic/activemq/tags?page_size=1024')
# if no tags pushed yet
if [[ "$remote" == *"object not found"* ]]; then
    # empty array
    declare -a pushed=()
else
    pushed=$( | jq --raw-output '."results"[]["name"]' )
fi
echo Pushed docker tags $pushed

# remove all the pushed ones from the released ones
# see: https://www.golinuxcloud.com/delete-elements-of-one-array-from-another-array/
for pushed_one in ${pushed[@]}; do
    released=( "${released[@]/$pushed_one}" )
done

echo To be pushed docker tags $released
echo To tagged latest ${released[-1]}

echo $released > all
echo ${released[-1]} > latest