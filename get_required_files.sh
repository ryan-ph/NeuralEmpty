site='https://homes.cs.washington.edu/~ryanp97/'
data='datasets.tar'

echo 'downloading and unzipping data'
wget $site.$data
tar -xvf $data
rm $data
