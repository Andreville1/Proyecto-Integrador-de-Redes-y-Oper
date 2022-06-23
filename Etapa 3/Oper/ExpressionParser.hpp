#ifndef EXPRESSION_PARSER_HPP
#define EXPRESSION_PARSER_HPP

#include <string>

// #include <pybind11/pybind11.h>

// namespace py = pybind11;

class ExpressionParser {
private:
    std::string prepend = "";
    std::string append = "";
    std::string subExpression = "";

    
public:
    int checkUnmatchedParens(std::string expression);

    void removeOps(std::string expression);

    void simplifySubExpression();

    std::string simplifyExpression(std::string expression);
};

#endif
