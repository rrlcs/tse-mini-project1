from lark import Lark
import numpy as np
import networkx as nx

l = Lark('''start: int | bool
            int: "x" -> var1 | "y" -> var2 | NUMBER -> num
                | "+" int int -> plus
                | "+" int int int -> tplus
                | "-" int -> uminus
                | "-" int int -> minus
                | "*" int int -> mul1
                | "*" NUMBER int -> mul2
                | "div" int NUMBER -> div
                | "mod" int NUMBER -> mod
                | "ite" bool int int -> ite
                | "f" int int -> f
            bool: "true" | "false"
                | "and" bool bool -> and
                | "or" bool bool -> or
                | "=>" bool bool -> implies
                | "xor" bool bool -> xor
                | "xnor" bool bool -> xnor
                | "nand" bool bool -> nand
                | "nor" bool bool -> nor
                | "iff" bool bool -> iff
                | "not" bool -> not
                | "=" bool bool -> beq
                | "<=" int int -> leq
                | ">=" int int -> geq
                | "<" int int -> lt
                | ">" int int -> gt
                | "=" int int -> eq
            WHITESPACE: (" " | "(" | ")")+
            %import common.CNAME -> NAME
            %import common.NUMBER -> NUMBER
            %ignore WHITESPACE
         ''')


grammar_rules = dict([('var1', 1), ('var2', 2), ('num', 3), ('plus', 4), ('tplus', 5), ('uminus', 6), ('minus', 7),
                    ('mul1', 8), ('mul2', 9), ('div', 10), ('mod', 11), ('ite', 12),
                    ('true', 13), ('false', 14), ('and', 15), ('or', 16), 
                    ('implies', 17), ('xor', 18), ('xnor', 19), ('nand', 20), 
                    ('nor', 21), ('iff', 22), ('not', 23), ('beq', 24), ('leq', 25),
                    ('geq', 26), ('lt', 27), ('gt', 28), ('eq', 29),])

# print(grammar_rules)
ast_node_encoding = dict({'f':0, 'var1':1, 'var2':2, '=':3, '<':4, '>':5, '<=':6, '>=':7, 'and':8, 'or':9, 'not':10, '=>':12, '+':13, '-':14, '*':15, 'div':16})

import pandas as pd
import csv

df = pd.read_csv("datasetGeneratedForTSE50000.csv")
# print(df.head(10))
constraints = df['Constraints']
programs = df['ExtractedPrograms']

# parsetree = l.parse("( or ( = y ( f x y ) ) ( <= ( + ( f x y ) ( + ( f x y ) ( + ( + ( f x y ) ( + ( f x y ) x ) ) ( f x y ) ) ) ) ( f x y ) ) )").pretty("---")
# print(parsetree)

def getEdgeListAndNumOfNodes(parsetree):
    num_of_nodes = parsetree.count("\n") - 1
    # print(num_of_nodes)
    Adj_Matrix = np.zeros((num_of_nodes, num_of_nodes))

    f = open("constraint.ast", "w")
    f.write(parsetree)
    f.close()
    node_list = []
    f = open("constraint.ast", "r")
    # import os
    # os.remove("constraint.ast")
    i=0
    j=0
    while i<num_of_nodes:
        for line in f.readlines()[1:]:
            line.replace("---", "")
            if line.count("-") == (3*i):
                node_list.append(line.replace("-", "").replace("\n", ""))
                j+=1
                # print(node_list)
        i+=1
        f.seek(0) 
    f.close
    j=1
    for i in range(np.int((num_of_nodes-1)/2)+2):
        if node_list[i] == 'var1' or node_list[i] == 'var2':
            pass
        elif j < num_of_nodes:
            Adj_Matrix[i, j] = 1
            Adj_Matrix[i, j+1] = 1
            j+=2
        # elif j < num_of_nodes:
        #     Adj_Matrix[i, j] = 1
        #     j+=1
    # print(Adj_Matrix)
    # converts from adjacency matrix to edge list 
    def convertToEdgeList(a): 
        edgeList = []
        for i in range(len(a)): 
            for j in range(len(a[i])): 
                if a[i][j]== 1:
                    edgeList.append((i,j))
        return edgeList

    edgeList = convertToEdgeList(Adj_Matrix)

    featureMatrix = np.zeros((num_of_nodes, len(ast_node_encoding)))
    # node_list.remove('start')
    # print(node_list)

    for i in range(num_of_nodes):
        if node_list[i] == 'gt':
            node = '>'
        elif node_list[i] == 'lt':
            node = '<'
        elif node_list[i] == 'eq':
            node = '='
        elif node_list[i] == 'geq':
            node = '>='
        elif node_list[i] == 'leq':
            node = '<='
        elif node_list[i] == 'plus':
            node = '+'
        elif node_list[i] == 'minus':
            node = '-'
        elif node_list[i] == 'uminus':
            node = '-'
        elif node_list[i] == 'mul1':
            node = '*'
        elif node_list[i] == 'mul2':
            node = '*'
        elif node_list[i] == 'beq':
            node = '='
        elif node_list[i] == 'implies':
            node = '=>'
        else:
            node = node_list[i]
        featureMatrix[i, ast_node_encoding.get(node)] = 1
    # print("feature matrix = \n", featureMatrix)
    # print(node_list[0])
    return num_of_nodes, edgeList, featureMatrix

# print("Edge List:", edgeList)
import json

j=0
data = {}
data['TrainingExamples'] = []
for i in range(len(programs)):
    # print(programs[i])
    if programs[i] == "Timeout" or programs[i] == "unknown":# or programs[i] == "((+ 1 x y))" or programs[i] == "((+ 1 x (* (- 1) y)))" or programs[i] == "((+ 1 (* 2 x) y))" or programs[i] == "((+ 1 (* 2 x) (* (- 1) y)))" or programs[i] == "((ite (and (>= (+ x (* (- 1) y)) 1) (>= (+ x y) 2)) (div (+ 2 x y) 2) 1))" or programs[i] == "((ite (>= (+ x y) 1) (+ 1 x (* 2 y)) (+ 1 y)))" or programs[i] == "((+ 1 x (* (- 2) y)))":
        pass
    elif programs[i].count("let") > 0:
        pass
    else:
        j+=1
        program_parsetree = l.parse(programs[i]).pretty("...")
        # print(parsetree)

        rules_used = np.zeros((len(grammar_rules), 1))
        # print(rules_used)

        for k, v in grammar_rules.items():
            # print(k, v)
            if(program_parsetree.find(k)>0):
                # print(k, v)
                rules_used[v-1] = 1
        constraint_parsetree = l.parse(constraints[i]).pretty("---")
        # print(i, constraints[i])
        num_of_nodes, edgeList, featureMatrix = getEdgeListAndNumOfNodes(constraint_parsetree)
        # print(edgeList)
        data['TrainingExamples'].append({
            'exampleNum': str(j),
            'constraint': constraints[i],
            'num_of_nodes': num_of_nodes,
            'edgeList': edgeList,
            'featureMatrix': json.dumps(featureMatrix.tolist()),
            'program': programs[i],
            'GrammarRulesUsed': json.dumps(rules_used.tolist())+'\n'
        })
        with open('data50k.json', 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=False)
        # with open('datasetWithASTFeaturesAndGrammarRules.csv', 'a', newline='') as csvfile:
        #     writer = csv.writer(csvfile, delimiter=',')
        #     writer.writerow(["\n"+str(j),constraints[i], num_of_nodes, edgeList, featureMatrix, programs[i], rules_used.transpose()])
        # # print(rules_used)

# print(json.dumps(data, indent=4))