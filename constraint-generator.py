from nltk import CFG, ChartParser
from random import choice

def produce(grammar, symbol):
    words = []
    productions = grammar.productions(lhs = symbol)
    production = choice(productions)
    for sym in production.rhs():
        if isinstance(sym, str):
            words.append(sym)
        else:
            words.extend(produce(grammar, sym))
    return words

def define_grammar():
    grammar = CFG.fromstring(
    '''
    R -> Lp LgOp S S Rp
    S -> Lp CmOp Fun I Rp | Lp CmOp I Fun Rp
    I -> 'x' | 'y' | Fun | Lp ArOp Fun I Rp | Lp ArOp I Fun Rp
    Fun -> Lp 'f' 'x' 'y' Rp
    ArOp -> '+' | '-'
    CmOp -> '<=' | '>=' | '<' | '>' | '='
    LgOp -> 'and' | 'or'
    Lp -> '('
    Rp -> ')'
    '''
    )

    return grammar

def define_parser(grammar):
    parser = ChartParser(grammar)
    return parser

def get_grammar_obj(parser):
    gr = parser.grammar()
    return gr

def generate_constraint(gr):
    words = produce(gr, gr.start())
    constraint = ' '.join(words)
    return constraint

if __name__ == "__main__":
    grammar = define_grammar()
    parser = define_parser(grammar)
    gr = get_grammar_obj(parser)
    constraint = generate_constraint(gr)
    print(constraint)
