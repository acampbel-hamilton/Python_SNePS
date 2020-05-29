# From https://gist.github.com/roberthoenig/30f08b64b6ba6186a2cdee19502040b4 ##

import sys

from typing import Any, List

# Parse input string into a list of all parentheses and atoms (int or str),
# exclude whitespaces.
def normalize_str(string: str) -> List[str]:
    str_norm = []
    last_c = None
    for c in string:
        if c.isalnum():
            if last_c.isalnum():
                str_norm[-1] += c
            else:
                str_norm.append(c)
        elif not c.isspace():
            str_norm.append(c)
        last_c = c
    return str_norm

# Generate abstract syntax tree from normalized input.
def get_ast(input_norm: List[str]) -> List[Any]:
    ast = []
    # Go through each element in the input:
    # - if it is an open parenthesis, find matching parenthesis and make recursive
    #   call for content in-between. Add the result as an element to the current list.
    # - if it is an atom, just add it to the current list.
    i = 0
    while i < len(input_norm):
        symbol = input_norm[i]
        if symbol == '(':
            list_content = []
            match_ctr = 1 # If 0, parenthesis has been matched.
            while match_ctr != 0:
                i += 1
                if i >= len(input_norm):
                    raise ValueError("Invalid input: Unmatched open parenthesis.")
                symbol = input_norm[i]
                if symbol == '(':
                    match_ctr += 1
                elif symbol == ')':
                    match_ctr -= 1
                if match_ctr != 0:
                    list_content.append(symbol)
            ast.append(get_ast(list_content))
        elif symbol == ')':
                raise ValueError("Invalid input: Unmatched close parenthesis.")
        else:
            try:
                ast.append(int(symbol))
            except ValueError:
                ast.append(symbol)
        i += 1
    return ast

def parse(str):
    return get_ast(normalize_str(str))

def main():
    input_str = sys.stdin.read()
    input_norm = normalize_str(input_str)
    ast = get_ast(input_norm)
    print(ast)

if __name__ == '__main__':
    main()
