### Script runs with cli command
`python convert_table.py --source <table_A.csv or table_B.csv> --template <template.csv> --result <result.csv> `
### or just
`python convert_table.py`
### Which will use table_A as source and template.csv as template by default
### Results saved at ./data/results


## TO:DO
## 1) Inference data validation:
### a) generated data should exist in source files.
### b) check data types (like Premium should be int or float. 
### In case Premium is string it should be able to change dtype to float or int.
### c) check Date, PolicyNumber with regexp
### d) possible to train model to assure quality of the inference.

## 2) Optimize batching. Algorithm should count tokens in a given row and append it to current batch 
## until stack reaches limit.

## 3) Try augment more data and fine-tune open source LLMs to complete this task. 
