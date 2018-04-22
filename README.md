# NeuralEmpty

This is the repository for Team NeuralEmpty for UW CSE NLP Capstone Spring 2018.

## Preprocessed Data

Run `./get_required_files.sh` to download the preprocessed data as well as the
files used to parse the data.

This will result in two folders: `parser/` and `data`. `parser/` contains the
[script](https://github.com/goodmami/mrs-to-penman) used to parse the graphs
from the Tanaka data. `data/` contains directories for the simplified data for
the Tanaka corpus and may be updated to contained processed data for the Kyoto
corpus. Note that this data must be processed once more by OpenNMT's scripts
before being used to train the model.
