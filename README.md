# NeuralEmpty

This is the repository for Team NeuralEmpty for UW CSE NLP Capstone Spring 2018.

## Preprocessed Data

Run `./get_required_files.sh` to download the preprocessed data as well as the
files used to parse the data.

This will result in two folders: `parser/` and `data/`. `parser/` contains the
[script](https://github.com/goodmami/mrs-to-penman) used to parse the graphs
from the Tanaka data. `data/` contains directories for the simplified data for
the Tanaka corpus and may be updated to contained processed data for the Kyoto
corpus. Note that this data must be processed once more by OpenNMT's scripts
before being used to train the model.

## Graph Simplification and Recovery
Use `simplify_graph.py` to create simple graphs for the model to process. The
data downloaded from the previous step is already simplified, so you do not
have to worry about it (`data/tanaka/simplified/`). However, if you want to use
your own dataset, you can use the script to simplify your own input.

```
usage: simplify_graph.py [-h] [--reverse]
                         [--feature-type {squash,expand,stable}]
                         input output

Takes penman graphs and simplifies it for Neural Net use or recovers it for
SMatch evaluation.

positional arguments:
  input                 Input file.
  output                Output file.

optional arguments:
  -h, --help            show this help message and exit
  --reverse             Recovers a DMRS graph given the simplified version.
  --feature-type {squash,expand,stable}
                        Determines what the format the output features should
                        have. "squash" will concatenate features into a single
                        token. "expand" will unsquash squashed features.
                        "stable" will keep the format of the features.
                        (default="stable")
```

## Postprocessing Model Predictions
Use `postprocess_predictions.py` to recover the simplified predictions that the
model outputs. Note that any non-well-formed graphs will be replaced with
`(999999999 / invalid)`. This will eventually underestimate how well the model
performs since it will result in the invalid graph having a F1 score of 0.

```
usage: postprocess_predictions.py [-h] input output

Takes predicted file and converts it into a format that can be evaluated using
SMATCH.

positional arguments:
  input       Input file.
  output      Output file.

optional arguments:
  -h, --help  show this help message and exit
```
