from io import StringIO
import tokenize

def transform_tokens(code: str, fn) -> str:
    transformed = []
    result = ""
    tokens = tokenize.generate_tokens(StringIO(code).readline)

    for tok in tokens:
        tok_type, tok_str, start, end, line = tok
        new_type, new_str = fn(tok_type, tok_str)
        transformed.append((new_type, new_str))

    transformed_str = tokenize.untokenize(transformed)

    for line in transformed_str.split("\n"):
        if line != "":
            line += "\n"
        result += line
    
    return result
    

def comments(t: str,s: str):
    if t == tokenize.COMMENT: 
        return t, ""
    return t, s

with open("test.py") as f:
    step_1 = f.read()

step_2 = transform_tokens(step_1, comments)

print(step_2)

for tok in tokenize.generate_tokens(StringIO(step_2).readline):
    print(tok)