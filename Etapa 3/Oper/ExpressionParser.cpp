#include "ExpressionParser.hpp"
#include <algorithm>

int ExpressionParser::checkUnmatchedParens(std::string expression) {
    int unmatchedParens = 0;

    for (auto character : expression) {
        if (character == '(') {
            ++unmatchedParens;
        } else if (character == ')') {
            --unmatchedParens;
        }
    }

    return unmatchedParens;
}

std::string ExpressionParser::removeOps(std::string expression) {
    // Valid operators: +, -, *, /, ^, sqrt(x), (, ).

    int unmatchedParens = checkUnmatchedParens(expression);

    bool start = true;
    for (auto character : expression) {
        if (character == '+' || character == '-' || character == '*'
        || character == '/' || character == '^') {
            if (start) {
                prepend += character;
            } else {
                subExpression += character;
            }
        } else if (character == '(') {
            if (unmatchedParens > 0) {
                prepend += character;
                --unmatchedParens;
            } else {
                start = false;
                subExpression += character;
            }
        } else {
            if (unmatchedParens <= 0) {
                start = false;
                subExpression += character;
            }
        }
    }

    std::reverse(expression.begin(), expression.end());
    bool end = true;
    for (auto character : expression) {
        if (character == '+' || character == '-' || character == '*'
        || character == '/' || character == '^') {
            if (end) {
                append = character + append;
            }
        } else if (character == ')') {
            if (unmatchedParens < 0) {
                append = character + append;
                ++unmatchedParens;
            } else {
                end = false;
            }
        } else {
            if (unmatchedParens >= 0) {
                end = false;
            }
        }
    }

    int lastPos = subExpression.length() - append.length();
    subExpression = subExpression.substr(0, lastPos);

    return subExpression;
}

std::string ExpressionParser::simplifyExpression(std::string expression) {
    prepend = "";
    append = "";
    subExpression = "";

    //removeOps(expression);
    //simplifySubExpression();

    //return prepend + subExpression + append;

    return expression;
}
