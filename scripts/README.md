# Graph Simplification and Recovery
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

# Postprocessing Model Predictions
Use `postprocess_predictions.py` to recover the simplified predictions that the
model outputs. Note that any non-well-formed graphs will be replaced with
`(999999999 / invalid)`. This will eventually underestimate how well the model
performs since it will result in the invalid graph having a F1 score of 0.

Use the `--include-features` flag to filter out any unwanted features for
evaluation.

```
usage: postprocess_predictions.py [-h] [--remove-all-features]
                                  [--include-features INCLUDE_FEATURES [INCLUDE_FEATURES ...]]
                                  input output

Takes predicted file and converts it into a format that can be evaluated using
SMATCH.

positional arguments:
  input                 Input file.
  output                Output file.

optional arguments:
  -h, --help            show this help message and exit
  --remove-all-features
                        Removes all features.
  --include-features INCLUDE_FEATURES [INCLUDE_FEATURES ...]
                        Features to include separated by spaces.
```

# Using Custom Data
I've also included a couple other small scripts for using your own custom
dataset.

## Segmenting Japanaese Raw Text
Segmentation is done using MeCab. You are free to augment the MeCab dictionary
with any external dictionaries that you want.

```
usage: segment.py [-h] source target output_dir

Tokenizes inputs and filters out any sentences that are too short (i.e. just
titles, etc.) and invalid sentences.

positional arguments:
  source      Source language file.
  target      Target language path.
  output_dir  Directory where the output should go. The files will have the
              same name as source and target.

optional arguments:
  -h, --help  show this help message and exit
```

## Cleaning Parses
There are two files that will be useful here: `clean_parse.py` and
`aggregate_cleaner.py`.

`clean_parse.py` will remove any output from the parser that does not
correspond to a valid parse.

```
usage: clean_parse.py [-h] [--full] input_lang1 input_lang2 output

Takes parallel penman graphs and removes entries in which graphs could not be
generated. Output format will be a translation pair per line where the
translations are separated by a tab character.

positional arguments:
  input_lang1  File for original graphs in 1st language.
  input_lang2  File for original graphs in 2st language.
  output       Output folder for the cleaned data. Filename will be the same
               as the inputs

optional arguments:
  -h, --help   show this help message and exit
  --full       Keeps all features of the DMRS graph. Defaults to false.
```

`aggregate_cleaner.py` will align the translation pairs and remove any pairs of
sentences in which graphs could not be parsed in both languages.

```
usage: aggregate_cleaner.py [-h] input_lang1 input_lang2 output1 output2

Takes parallel penman graphs and removes entries in which graphs could not be
generated. Keeps only graphs with were able to be parsed in both languages

positional arguments:
  input_lang1  File for the first language graphs.
  input_lang2  File for the second language graphs.
  output1      Output file for the first language.
  output2      Output file for the second language.

optional arguments:
  -h, --help   show this help message and exit
```
