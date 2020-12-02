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
Download "datasetGeneratedForTSE50000.csv" and open it with MS Excel

```
S No.,    Constraints,                                                  Programs
1,        (and (> (- (- y x) (f x y)) y) (> (- (- y x) (f x y)) y)),    Timeout
2,        (and (<= (f x y) (f x y)) (<= y x)),                          Timeout
3,        (and (< (+ (f x y) y) x) (< (+ (f x y) y) x)),                (define-fun f ((x Int) (y Int)) Int (+ (- 1) x (* (- 1) y)))
```

## To view the preprocessed data
Download and extract "data118618.json.gz"
It consists of 1118618 preprocessed data points.

```
            # Store data in json format
            data['TrainingExamples'].append({
                'exampleNum': str(j),
                'constraint': constraints[i],
                'num_of_nodes': num_of_nodes,
                'edgeList': np.array(edgeList).tolist(),
                'featureMatrix': featureMatrix.tolist(),
                'program': programs[i],
                'GrammarRulesUsed': rules_used.tolist()
            })
```

### Parser used to parse the programs is Lark Parser 
Follow the instructions on https://github.com/lark-parser/lark to install lark parser




This project is being done under the course Topics in Software Engineering offered at Indian Institute of Science, Bangalore.

**Project Members: Ravi Raja**

**Guided By: Aditya Kanade & Shirish Shevde**
