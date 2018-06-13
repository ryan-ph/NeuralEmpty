#!/bin/bash


# $1 - The output directory.
# $2 - The directory of the data. Should contain train.{en,jp}, dev.{en,jp}, test.{en,jp}
# $3 - The subset of subdirectories to use. Uses all of them if left blank.

out_dir=$1
data=$2
sub_dirs=$3


if [ ! -d $data ]; then
    echo "$data does not exist. Exiting."
    exit 1
fi


for dataset in "train" "dev" "test"; do
    echo "aggregating $dataset"

    en_dir="$data$dataset.en"
    jp_dir="$data$dataset.jp"

    # Finds graphs in nested subdirectories
    if [ -d $en_dir ]; then
        if [ -z ${3+x} ]; then
            ls $en_dir/ | while read SUB; do
                if [[ -e $en_dir/$SUB/graphs ]] && [[ -e $jp_dir/$SUB/graphs ]]; then
                    python aggregate_cleaner.py $en_dir/$SUB/graphs $jp_dir/$SUB/graphs $out_dir/$dataset.en $out_dir/$dataset.jp
                fi
            done
        else
            for sub_dir in $sub_dirs; do
                find $en_dir/$sub_dir* -maxdepth 1 -type d | while read SUB; do
                    SUB=${SUB##*/}
                    if [[ -e $en_dir/$SUB/graphs ]] && [[ -e $jp_dir/$SUB/graphs ]]; then
                        python aggregate_cleaner.py $en_dir/$SUB/graphs $jp_dir/$SUB/graphs $out_dir/$dataset.en $out_dir/$dataset.jp
                    fi
                done
            done
        fi
    fi
done
