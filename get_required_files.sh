site='https://homes.cs.washington.edu/~ryanp97/'
data='datasets.tar'
models='models.tar'

echo 'downloading and unzipping data'
wget $site.$data
tar -xvf $data
rm $data


echo 'downloading and unzipping pretrained models'
wget $site.$models
tar -xvf $models
rm $models
