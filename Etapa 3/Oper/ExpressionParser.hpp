#ifndef EXPRESSION_PARSER_HPP
#define EXPRESSION_PARSER_HPP

#include <string>

class ExpressionParser {
private:
    std::string prepend = "";
    std::string append = "";
    std::string subExpression = "";

    int checkUnmatchedParens(std::string expression);

    void removeOps(std::string expression);

    void simplifySubExpression();

public:
    std::string simplifyExpression(std::string expression);
};

#endif
