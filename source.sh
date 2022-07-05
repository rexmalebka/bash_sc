#!/bin/bash

export PYTHONPATH="$PYTHONPATH:$PWD"
export CWD="$PWD"

for ugen in $(ls ugens/sources/*.py)
do
	# Load Ugen sources
	command=$(echo ${ugen##*/} | awk -F '.py' '{print $1}')
	eval '$command(){
	python '$CWD'/'$ugen' "$@" 
}'
done
