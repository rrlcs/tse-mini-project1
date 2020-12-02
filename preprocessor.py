from lark import Lark
import numpy as np
import pandas as pd
import csv
import json
import re
import nltk
nltk.download('punkt')

def getNumofNodes(parsetree):
    return parsetree.count("\n") - 1

def getNodeList(parsetree, num_of_nodes):
    f = open("constraint.ast", "w")
    f.write(parsetree)
    f.close()
    node_list = []
    f = open("constraint.ast", "r")
    i=0
    j=0
    while i<num_of_nodes:
        for line in f.readlines()[1:]:
            line.replace("---", "")
            if line.count("-") == (3*i):
                node_list.append(line.replace("-", "").replace("\n", ""))
                j+=1
        i+=1
        f.seek(0) 
    f.close
    return node_list

def getAdjMatrix(num_of_nodes, node_list):
    Adj_Matrix = np.zeros((num_of_nodes, num_of_nodes))
    j=1
    for i in range(np.int((num_of_nodes-1)/2)+2):
        if node_list[i] == 'var1' or node_list[i] == 'var2':
            pass
        elif j < num_of_nodes:
            Adj_Matrix[i, j] = 1
            Adj_Matrix[i, j+1] = 1
            j+=2
    return Adj_Matrix

def convertToEdgeList(Adj_Matrix): 
    '''
    Converts Adjacency matrix to edge list
    '''
    edgeList = []
    for i in range(len(Adj_Matrix)): 
        for j in range(len(Adj_Matrix[i])): 
            if Adj_Matrix[i][j]== 1:
                edgeList.append(tuple([i,j]))
    return edgeList

def getFeatureMatrix(num_of_nodes, node_list, ast_node_encoding):
    '''
    feature matrix for each node in contraint ast
    '''
    featureMatrix = np.zeros((num_of_nodes, len(ast_node_encoding)+1))
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
    return featureMatrix

if __name__ == "__main__":

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
    ast_node_encoding = dict({'f':0, 'var1':1, 'var2':2, '=':3, '<':4, '>':5, '<=':6, '>=':7, 'and':8, 'or':9, 'not':10, '=>':12, '+':13, '-':14, '*':15, 'div':16, 'PAD1':17, 'PAD2':18, 'PAD3': 19})
    # program_encoding = dict({'f':0, 'var1':1, 'var2':2, '=':3, '<':4, '>':5, '<=':6, '>=':7, 'and':8, 'or':9, 'not':10, 'ite':12, '+':13, '-':14, '*':15, 'div':16, '(':17, ')':18, 'num':19})

    df = pd.read_csv("datasetGeneratedForTSE50000.csv")
    constraints = df['Constraints']
    programs = df['ExtractedPrograms']

    j=0
    data = {} # Initialize data in json format
    data['TrainingExamples'] = []
    for i in range(len(programs)):
        if programs[i] == "Timeout" or programs[i] == "unknown":
            pass
        elif programs[i].count("let") > 0:
            pass
        else:
            j+=1
            program_parsetree = l.parse(programs[i]).pretty("...")
            rules_used = np.zeros((len(grammar_rules), 1))
            for k, v in grammar_rules.items():
                # print(k, v)
                if(program_parsetree.find(k)>0):
                    # print(k, v)
                    rules_used[v-1] = 1
            
            constraint_parsetree = l.parse(constraints[i]).pretty("---") # AST for constraints

            num_of_nodes = getNumofNodes(constraint_parsetree) # Number of nodes in constraint AST
            node_list = getNodeList(constraint_parsetree, num_of_nodes) # List of nodes in AST : level order
            Adj_Matrix = getAdjMatrix(num_of_nodes, node_list) # Adjacency Matrix for constraint AST
            edgeList = convertToEdgeList(Adj_Matrix) # Edge List of constraint AST
            featureMatrix = getFeatureMatrix(num_of_nodes, node_list, ast_node_encoding) # Initial feature matrix for the constraints

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
with open('data1lakh.json', 'w') as outfile:
    json.dump(data, outfile, indent=4, sort_keys=False)