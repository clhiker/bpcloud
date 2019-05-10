#!/bin/sh
token_path="$HOME/.bypy/bypy.json"
if [ ! -f "$token_path" ]; then 
    cd bpcloud; ./bpcloud
else 
    cd bpcloud; ./bpcloud >> log &
fi
