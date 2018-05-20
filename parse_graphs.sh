#!/bin/bash


# $1 - ace binary
# $2 - erg
# $3 - jacy
# $4 - data folder. should contain train.{en,jp}, dev.{en,jp}, test.{en,jp}


ace=$1
erg=$2
jacy=$3
data=$4


for lang in "jp" "en"; do
    for dataset in "train" "dev" "test"; do
        ls $data/$dataset.$lang | while read SUB; do
            if [ $lang = "en" ]; then
                grammar=$erg
            else
                grammar=$jacy
            fi
            full_path=$data/$dataset.$lang/$SUB
            echo "python parser/mrs_to_penman.py --ace-binary $ace -g $grammar -i $full_path > $full_path/graphs"
        done
    done
done
