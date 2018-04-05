site='https://homes.cs.washington.edu/~ryanp97/'

echo 'downloading and unzipping data'
wget ${site}'data.tar'
tar -xvf data.tar
rm data.tar

echo 'downloading and unzipping parser'
wget ${site}'parser.tar'
tar -xvf parser.tar
rm parser.tar
