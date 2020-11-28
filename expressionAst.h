#ifndef EXPR_AST_H
#define EXPR_AST_H

#include <iostream>

// #include "expressionVisitors.h"

// class FormulaBinaryExp;
// class FormulaVar;

class Formula
{
    public:
        // virtual void accept(FormulaVisitor* visitor){};
        virtual void prettyPrinter(){};
        virtual std::string formulaToString(){};
};

class Operator
{
    public:
        virtual void prettyPrinter(){};
        virtual std::string formulaToString(){};
};

class ArithmaticOperator : public Operator
{
    private:
        std::string op;
    public:
        ArithmaticOperator(std::string op) //Constructor
        {
            if(op == "+" || op == "-")
            {
                this->op = op;
            }
            else
            {
                std::cerr<<"Error: Wrong Operator Type \n";
                exit(EXIT_FAILURE);
            }
            
        }
        std::string formulaToString()
        {
            return getOp();
        }
        void prettyPrinter()
        {
            std::cout<<getOp();
        }
        std::string getOp()
        {
            return op;
        }
};

class ComparisonOperator : public Operator
{
    private:
        std::string op;
    public:
        ComparisonOperator(std::string op) //Constructor
        {
            if(op == "<" || op == ">" || op == "<=" || op == ">=" || op == "=")
            {
                this->op = op;
            }
            else
            {
                std::cerr<<"Error: Wrong Operator Type \n";
                exit(EXIT_FAILURE);
            }
            
        }
        std::string formulaToString()
        {
            return getOp();
        }
        void prettyPrinter()
        {
            std::cout<<getOp();
        }
        std::string getOp()
        {
            return op;
        }
};

class LogicalOperator : public Operator
{
    private:
        std::string op;
    public:
        LogicalOperator(std::string op) //Constructor
        {
            if(op == "and" || op == "or")
            {
                this->op = op;
            }
            else
            {
                std::cerr<<"Error: Wrong Operator Type \n";
                exit(EXIT_FAILURE);
            }
            
        }
        std::string formulaToString()
        {
            return getOp();
        }
        void prettyPrinter()
        {
            std::cout<<getOp();
        }
        std::string getOp()
        {
            return op;
        }
};

class FunctionOperator : public Operator
{
    private:
        std::string op;
    public:
        FunctionOperator(std::string op) //Constructor
        {
            if(op == "f" || op == "fun")
            {
                this->op = op;
            }
            else
            {
                std::cerr<<"Error: Wrong Operator Type \n";
                exit(EXIT_FAILURE);
            }
            
        }
        std::string formulaToString()
        {
            return getOp();
        }
        void prettyPrinter()
        {
            std::cout<<getOp();
        }
        std::string getOp()
        {
            return op;
        }
};

class FormulaVar : public Formula
{
    private:
        std::string var;
    public:
        FormulaVar(std::string var)//Constructor
        {
            this->var = var;
        }
        // void accept(FormulaVisitor* visitor)
        // {
        //     visitor->visit(this);
        // }
        std::string formulaToString()
        {
            return getVar();
        }
        void prettyPrinter() //Printer
        {
            std::cout<<var;
        }
        std::string getVar()
        {
            return var;
        }
};

class FormulaBinaryExp : public Formula
{
    private:
        Formula *left;
        Formula *right;
        Operator *op;
    public:
        FormulaBinaryExp(Formula* left, Formula* right, Operator* op)
        {
            this->left = left;
            this->right = right;
            this->op = op;
        }
        // void accept(FormulaVisitor* visitor)
        // {
        //     visitor->visit(this);
        // }
        std::string formulaToString()
        {
            std::string constraint 
                = "("+op->formulaToString()+" "+left->formulaToString()+" "+right->formulaToString()+")";
            return constraint;
        }
        void prettyPrinter() //Printer
        {
            std::cout<<"(";
            op->prettyPrinter();
            std::cout<<" ";
            left->prettyPrinter();
            std::cout<<" ";
            right->prettyPrinter();
            std::cout<<")";
        }
        
        Formula* getLeft()
        {
            return left;
        }
        void setLeft(Formula* formula)
        {
            this->left = formula;
        }
        Formula* getRight()
        {
            return right;
        }
        void setRight(Formula* formula)
        {
            this->right = formula;
        }
        Operator* getOp()
        {
            return op;
        }
        void setOp(Operator* op)
        {
            this->op = op;
        }
};

#endif //EXPR_AST_H