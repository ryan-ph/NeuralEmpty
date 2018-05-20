#!/bin/bash


# $1 - The output directory.
# $2 - The title of the directories to check. For instance, 'train' will check
#      'train.en/' and 'train.jp/'
# $3 - The subset of subdirectories to use. Uses all of them if left blank.

out_dir=$1
main_dir=$2
sub_dirs=$3


# Function that appends $1 (gzip file) to corresponding file in $2 (folder)
append_gzip() {
    file_name=${1##*/}
    # echo $1
    # echo $2/$file_name

    # Appends gz file to the appropriate output file
    zcat $1 | gzip -c >> $2/$file_name
}


# Iterates through all subdirectories of $main_dir and concatenates them to
# corresponding output file.
for lang in "en" "jp"; do
    output_dir=$out_dir.$lang

    # Creates the output directory if it does not exist
    if [ ! -d $output_dir ]; then
        mkdir $output_dir
    fi

    # Finds nested gz files to append
    dir="$main_dir.$lang"
    if [ -d $dir ]; then
        if [ -z ${3+x} ]; then
            ls $dir/ | while read SUB; do
                ls $dir/$SUB*/*.gz | while read F; do
                    append_gzip $F $output_dir
                done
            done
        else
            for dataset in $sub_dirs; do
                ls $dir/$dataset*/*.gz | while read F; do
                    append_gzip $F $output_dir
                done
            done
        fi
    else
        echo "$dir does not exist. Exiting."
        exit 1
    fi
done
