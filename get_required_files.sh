site='https://homes.cs.washington.edu/~ryanp97/'

echo 'downloading and unzipping data'
wget ${site}'data.tar'
tar -xvf data.tar
rm data.tar
