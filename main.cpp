#include <iostream>
#include <vector>
#include <random>
#include <iterator>
#include <fstream>
#include <chrono>
#include <algorithm>
#include "expressionAst.h"

template<typename Iter, typename RandomGenerator>
Iter select_randomly(Iter start, Iter end, RandomGenerator& g) {
    std::uniform_int_distribution<> dis(0, std::distance(start, end) - 1);
    std::advance(start, dis(g));
    return start;
}

template<typename Iter>
Iter select_randomly(Iter start, Iter end) {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    return select_randomly(start, end, gen);
}

std::string insertConstraint(std::string templateFile, std::string constraint)
{
    size_t index = 0;
    while (true) {
        /* Locate the substring to replace. */
        index = templateFile.find("$$", index);
        if (index == std::string::npos) break;

        /* Make the replacement. */
        templateFile.replace(index, 2, constraint);

        /* Advance index forward so the next iteration doesn't pick it up as well. */
        index += 3;
    }
    return templateFile;
}

std::string runCVC4(std::string command) {
   char buffer[128];
   std::string result = "";

   // Open pipe to file
   FILE* pipe = popen(command.c_str(), "r");
   if (!pipe) {
      return "popen failed!";
   }

   // read till end of process:
   while (!feof(pipe)) {
      // use buffer to read and add to result
      if (fgets(buffer, 128, pipe) != NULL)
         result += buffer;
   }
   pclose(pipe);
   return result;
}

void writeToCSV(const std::string& name, const std::string& content, bool append = false) {
    std::ofstream outfile;
    if (append)
        outfile.open(name, std::ios_base::app);
    else
        outfile.open(name);
    outfile << content;
}

std::string getRandomConstraint(int numOfOperator, std::vector<Formula *> ArithmaticOperandList, std::vector<ArithmaticOperator *> ArithmaticOperatorList, std::vector<Formula *> ComparisonOperandList, std::vector<ComparisonOperator *> ComparisonOperatorList, std::vector<Formula *> LogicalOperandList, std::vector<LogicalOperator *> LogicalOperatorList)
{
    FormulaBinaryExp *exp1;
    for(int i = 0; i<numOfOperator; i+=3)
        {
            // Generate expressions with arithmatic operators
            exp1 = new FormulaBinaryExp(*select_randomly(ArithmaticOperandList.begin(), ArithmaticOperandList.end()), *select_randomly(ArithmaticOperandList.begin(), ArithmaticOperandList.end()), *select_randomly(ArithmaticOperatorList.begin(), ArithmaticOperatorList.end()));
            ArithmaticOperandList.push_back(exp1); // Add expression generated to the operand list
            // Generate expressions with comparison operators
            exp1 = new FormulaBinaryExp(*select_randomly(ArithmaticOperandList.begin(), ArithmaticOperandList.end()), *select_randomly(ArithmaticOperandList.begin(), ArithmaticOperandList.end()), *select_randomly(ComparisonOperatorList.begin(), ComparisonOperatorList.end()));
            ComparisonOperandList.push_back(exp1); // Add expression generated to a new operand list
            // Generate expressions with logical operators
            exp1 = new FormulaBinaryExp(*select_randomly(ComparisonOperandList.begin(), ComparisonOperandList.end()), *select_randomly(ComparisonOperandList.begin(), ComparisonOperandList.end()), *select_randomly(LogicalOperatorList.begin(), LogicalOperatorList.end()));
            LogicalOperandList.push_back(exp1); // Add expression generated to a new operand list
        }
    std::string constraint = LogicalOperandList.back()->formulaToString();
    return constraint;
}

int main(int argc, char* argv[])
{
    auto t1 = std::chrono::high_resolution_clock::now();

    std::string filenum = argv[1]; // number of sygus files already created in the Dataset directory
    std::string datapoints = argv[2]; // Number of data points to generate
    int numOfOperator = 6;
    
    // Define Operand Lists
    std::vector<Formula *> ArithmaticOperandList;
    std::vector<Formula *> ComparisonOperandList;
    std::vector<Formula *> LogicalOperandList;
    
    // Define Operator Lists
    std::vector<ArithmaticOperator *> ArithmaticOperatorList;
    std::vector<ComparisonOperator *> ComparisonOperatorList;
    std::vector<LogicalOperator *> LogicalOperatorList;

    // Initialize x and y operands
    FormulaVar *x = new FormulaVar("x");
    FormulaVar *y = new FormulaVar("y");
    
    // Push x and y to arithmatic operand list
    ArithmaticOperandList.push_back(x);
    ArithmaticOperandList.push_back(y);
    
    // Initialize arithmatic operators
    ArithmaticOperator *Plus = new ArithmaticOperator("+");
    ArithmaticOperator *Minus = new ArithmaticOperator("-");
    
    // Push arith. operators to arith. operator list
    ArithmaticOperatorList.push_back(Plus);
    ArithmaticOperatorList.push_back(Minus);

    // Initialize comparison operators
    ComparisonOperator *LT = new ComparisonOperator("<");
    ComparisonOperator *GT = new ComparisonOperator(">");
    ComparisonOperator *LEQ = new ComparisonOperator("<=");
    ComparisonOperator *GEQ = new ComparisonOperator(">=");
    ComparisonOperator *EQ = new ComparisonOperator("=");
    
    // Push comparison operators to comparison operator list
    ComparisonOperatorList.push_back(LT);
    ComparisonOperatorList.push_back(GT);
    ComparisonOperatorList.push_back(LEQ);
    ComparisonOperatorList.push_back(GEQ);
    ComparisonOperatorList.push_back(EQ);

    // Initialize logical operators
    LogicalOperator *And = new LogicalOperator("and");
    LogicalOperator *Or = new LogicalOperator("or");
    
    // Push logical operators to logical operator list
    LogicalOperatorList.push_back(And);
    LogicalOperatorList.push_back(Or);

    FunctionOperator *f = new FunctionOperator("f");
    FormulaBinaryExp *exp1;
    exp1 = new FormulaBinaryExp(x, y, f);
    ArithmaticOperandList.push_back(exp1);
    exp1 = new FormulaBinaryExp(y, x, f);
    ArithmaticOperandList.push_back(exp1);
    
    std::string templateFile = "(set-logic LIA)\n(synth-fun f ((x Int) (y Int)) Int)\n(declare-var x Int)\n(declare-var y Int)\n(constraint $$)\n(check-synth)";
    int tmp = 1;
    std::string func = "f";
    std::string constraint;
    std::string sygusFile;
    std::string cmd1 = "python constraint-generator.py";
    std::string program_ext;
    while(tmp)
    {
        // Generate Random Constraints
        constraint = getRandomConstraint(numOfOperator, ArithmaticOperandList, ArithmaticOperatorList, ComparisonOperandList, ComparisonOperatorList, LogicalOperandList, LogicalOperatorList);
        constraint.erase(std::remove(constraint.begin(), constraint.end(), '\n'), constraint.end());
        
        if (constraint.find(func) != std::string::npos)
        {
            sygusFile = insertConstraint(templateFile, constraint);
            std::string name = "randomlyGeneratedBenchmark_"+filenum+".sl"; // Create a SyGuS file for each randomly generated constraint
            std::ofstream slFile("Dataset50000/"+name);
            slFile << sygusFile; 
            slFile.close();
            std::string program="\0";
            std::string cmd = "timeout 0.1s cvc4 ./Dataset50000/"+name+" 2> /dev/null";
            std::string result = runCVC4(cmd); // Pick the SyGuS files and run CVC4 on them

            auto t2 = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::microseconds>( t2 - t1 ).count(); // Compute the execution time for cvc4
            std::string execTime = std::to_string(duration);
            
            // Write the (constraint, program) pairs in a csv file,
            // along with their execution times
            name = "datasetGeneratedForTSE"+datapoints+".csv";
            if(result == "\0")
            {
                writeToCSV(name, "\n"+filenum+","+constraint+","+"Timeout"+","+"Timeout"+","+execTime, true);
            }
            else if (result == "unknown\n")
            {
                writeToCSV(name, "\n"+filenum+","+constraint+","+"unknown"+","+"unknown"+","+execTime, true);
            }
            else
            {
                program = result.substr(6, result.size() - 6);
                program.erase(std::remove(program.begin(), program.end(), '\n'), program.end());
                program_ext = program;
                program_ext.erase(1, 35);
                writeToCSV(name, "\n"+filenum+","+constraint+","+program+","+program_ext+","+execTime, true);
            }

            tmp = 0;
        }
    }
    
    // free memory
    delete x;
    delete y;
    delete Plus;
    delete Minus;
    delete LT;
    delete GT;
    delete LEQ;
    delete GEQ;
    delete EQ;
    delete And;
    delete Or;
    delete exp1;
}
