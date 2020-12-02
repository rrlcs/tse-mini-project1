# tse-mini-project1
Dataset Generation for SyGuS

## Download repository
```
git clone https://github.com/rrlcs/tse-mini-project1.git
```

## To generate raw data using Random Constraint Generation
This would generate 50k raw data points of (constraint, program) pair.
```
./generate-dataset.sh
```

## To preprocess the raw data and store it in json format
```
python preprocessor.py
```

## To view the raw data
Download datasetGeneratedForTSE50000.csv and open it with MS Excel

## To view the preprocessed data
Download and extract data118618.json.gz

### Parser used to parse the programs is Lark Parser 
Follow the instructions on https://github.com/lark-parser/lark to install lark parser

### This project is being done under the course Topics in Software Engineering offered at Indian Institute of Science, Bangalore

## Project Members: Ravi Raja
