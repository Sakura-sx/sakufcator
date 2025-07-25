from io import StringIO
import tokenize
from ints import obf_int
from strs import obf_str
import base64

def transform_tokens(code: str, fn) -> str:
    result = ""
    transformed_str_builder = []
    tokens = tokenize.generate_tokens(StringIO(code).readline)

    last_line = 1
    last_col = 0

    for tok in tokens:
        tok_type, tok_str, start, end, line = tok
        if tok_type == tokenize.ENCODING:
            continue
        if start[0] > last_line:
            transformed_str_builder.append('\n' * (start[0] - last_line))
            last_col = 0
        if start[1] > last_col:
            transformed_str_builder.append(' ' * (start[1] - last_col))
        new_type, new_str = fn(tok_type, tok_str)
        transformed_str_builder.append(new_str)
        
        last_line = end[0]
        last_col = end[1]

    transformed_str = "".join(transformed_str_builder)

    for line in transformed_str.split("\n"):
        if line != "":
            line += "\n"
        result += line
    
    return result
    

def comments(t: str,s: str):
    if t == tokenize.COMMENT: 
        return t, ""
    return t, s

def int_obfuscation(t: str, s: str):
    if t == tokenize.NUMBER and (s.isdigit() or (s.startswith('-') and s[1:].isdigit())) and "." not in s:
        return t, f"{obf_int(int(s), 8)}"
    return t, s

def str_obfuscation(t: str, s: str):
    if t == tokenize.STRING and ((s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'"))):
        s = s[1:-1]
        new_str = obf_str(str(s), 4)
        # print(f"old: {s} new: {new_str}")
        return t, f"str({new_str})"
    return t, s

with open("test.py") as f:
    step_1 = f.read()

step_2 = transform_tokens(step_1, comments)

print(step_2)

for tok in tokenize.generate_tokens(StringIO(step_2).readline):
    print(tok)


print("STEP 3")

step_3 = transform_tokens(step_2, int_obfuscation)

print(step_3)

print("STEP 4")

step_4 = transform_tokens(step_3, str_obfuscation)
step_4 = transform_tokens(step_4, int_obfuscation)

print(step_4)
for tok in tokenize.generate_tokens(StringIO(step_4).readline):
    print(tok)

print("STEP 5")
step_5 = f"import base64; exec(base64.b64decode('{base64.b64encode(step_4.encode()).decode()}'))"

print(step_5)
for tok in tokenize.generate_tokens(StringIO(step_5).readline):
    if tok[0] == tokenize.STRING:
        print(tok[1])

print("TEST STEP 5")


print("STEP 6")

step_6 = transform_tokens(step_5, str_obfuscation)
print(step_6)
for tok in tokenize.generate_tokens(StringIO(step_6).readline):
    if tok[0] == tokenize.STRING or tok[0] == tokenize.NUMBER:
        print(tok[1])

print("TEST STEP 6")



print("STEP 7")
step_7 = transform_tokens(step_6, int_obfuscation)

print(step_7)

with open("aaa.py", "w") as f:
    f.write(step_7)