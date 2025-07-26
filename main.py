from io import StringIO
import tokenize
from ints import obf_int
from strs import obf_str
import base64
import ast
import hashlib

str_steps = 2
int_steps = 0

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
        return t, f"{obf_int(int(s), int_steps)}"
    return t, s

def str_obfuscation(t: str, s: str):
    if t == tokenize.STRING and ((s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'"))):
        s = s[1:-1]
        new_str = obf_str(str(s), str_steps)
        # print(f"old: {s} new: {new_str}")
        return t, f"str({new_str})"
    return t, s

def replace_vars(t: str, s: str):
    if t == tokenize.NAME:
        if s in user_vars:
            print(f"Replacing variable: {s} with {hashlib.sha256(s.encode()).hexdigest()[:8]}")
            return t, hashlib.sha256(s.encode()).hexdigest()[:8]
    return t, s

with open("test2.py") as f:
    step_1 = f.read()
step_2 = "import sys; sys.setrecursionlimit(99999999) \n" + transform_tokens(step_1, comments)

print(step_2)

#for tok in tokenize.generate_tokens(StringIO(step_2).readline):
    #print(tokenize.tok_name[tok.exact_type])
    #print(tok)

for tok in tokenize.generate_tokens(StringIO(step_2).readline):
    if tokenize.tok_name[tok.exact_type] == "NAME":
        print(tok.string)
        
step_2_parsed = ast.parse(step_2)
print(ast.dump(step_2_parsed))
user_vars = []
for node in ast.walk(step_2_parsed):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                user_vars.append(target.id)
    elif isinstance(node, ast.AugAssign):
        if isinstance(node.target, ast.Name):
            user_vars.append(node.target.id)

user_vars = list(set(user_vars))

class VariableFlattener(ast.NodeTransformer):
    def __init__(self, var_names):
        self.var_names = set(var_names)
        self.global_var_name = "g" + hashlib.sha256("_g".encode()).hexdigest()[:7]
        self.var_name_map = {}
        self.string_var_map = {}
        self.builtin_var_map = {}
        self.string_counter = 0
        self.builtin_counter = 0
        
        for var in var_names:
            self.var_name_map[var] = "v" + hashlib.sha256(var.encode()).hexdigest()[:7]
    
    def get_string_var_name(self, string_value):
        if string_value not in self.string_var_map:
            string_key = f"str_{self.string_counter}"
            self.string_var_map[string_value] = "s" + hashlib.sha256(string_key.encode()).hexdigest()[:7]
            self.string_counter += 1
        return self.string_var_map[string_value]
    
    def get_builtin_var_name(self, builtin_name):
        if builtin_name not in self.builtin_var_map:
            builtin_key = f"builtin_{self.builtin_counter}_{builtin_name}"
            self.builtin_var_map[builtin_name] = "b" + hashlib.sha256(builtin_key.encode()).hexdigest()[:7]
            self.builtin_counter += 1
        return self.builtin_var_map[builtin_name]
    
    def visit_Assign(self, node):
        self.generic_visit(node)
        if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            if var_name in self.var_names:
                new_target = ast.Subscript(
                    value=ast.Name(id=self.global_var_name, ctx=ast.Load()),
                    slice=ast.Constant(value=self.var_name_map[var_name]),
                    ctx=ast.Store()
                )
                node.targets = [new_target]
        return node
    
    def visit_AugAssign(self, node):
        self.generic_visit(node)
        if isinstance(node.target, ast.Name) and node.target.id in self.var_names:
            node.target = ast.Subscript(
                value=ast.Name(id=self.global_var_name, ctx=ast.Load()),
                slice=ast.Constant(value=self.var_name_map[node.target.id]),
                ctx=ast.Store()
            )
        return node
    
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            if node.id in self.var_names:
                return ast.Subscript(
                    value=ast.Name(id=self.global_var_name, ctx=ast.Load()),
                    slice=ast.Constant(value=self.var_name_map[node.id]),
                    ctx=ast.Load()
                )
            else:
                builtin_var_name = self.get_builtin_var_name(node.id)
                return ast.Subscript(
                    value=ast.Name(id=self.global_var_name, ctx=ast.Load()),
                    slice=ast.Constant(value=builtin_var_name),
                    ctx=ast.Load()
                )
        return node
    
    def visit_Constant(self, node):
        if isinstance(node.value, str) and len(node.value) > 0:
            if len(node.value) > 2:
                string_var_name = self.get_string_var_name(node.value)
                return ast.Subscript(
                    value=ast.Name(id=self.global_var_name, ctx=ast.Load()),
                    slice=ast.Constant(value=string_var_name),
                    ctx=ast.Load()
                )
        return node

flattener = VariableFlattener(user_vars)
print(f"Applying flattening for variables: {user_vars}")

try:
    step_2_parsed = flattener.visit(step_2_parsed)
    print("Flattening completed successfully")
except Exception as e:
    print(f"Error during flattening: {e}")
    exit(1)

global_var_name = flattener.global_var_name
dict_keys = []
dict_values = []

for string_value, string_var_name in flattener.string_var_map.items():
    dict_keys.append(ast.Constant(value=string_var_name))
    dict_values.append(ast.Constant(value=string_value))
    print(f"Extracted string: '{string_value}' -> {string_var_name}")

for builtin_name, builtin_var_name in flattener.builtin_var_map.items():
    dict_keys.append(ast.Constant(value=builtin_var_name))
    dict_values.append(ast.Name(id=builtin_name, ctx=ast.Load()))
    print(f"Extracted built-in: '{builtin_name}' -> {builtin_var_name}")

global_init = ast.Assign(
    targets=[ast.Name(id=global_var_name, ctx=ast.Store())],
    value=ast.Dict(keys=dict_keys, values=dict_values)
)

step_2_parsed.body.insert(0, global_init)

ast.fix_missing_locations(step_2_parsed)


step_2 = ast.unparse(step_2_parsed)
print("=== TRANSFORMED CODE ===")
print(step_2)
print("=== END TRANSFORMED CODE ===")

step_3 = transform_tokens(step_2, replace_vars)
print("=== VARIABLE REPLACED CODE ===")
print(step_3)
print("=== END VARIABLE REPLACED CODE ===")


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
step_5 = f"import sys; print(\"This program has been obfuscated with Sakufcator 1.0-beta\"); import base64; exec(base64.b64decode('{base64.b64encode(step_4.encode()).decode()}'))"

print(step_5)
for tok in tokenize.generate_tokens(StringIO(step_5).readline):
    if tok[0] == tokenize.STRING:
        print(tok[1])

print("TEST STEP 5")


print("STEP 6")
str_steps = 3
step_6 = transform_tokens(step_5, str_obfuscation)
print(step_6)
for tok in tokenize.generate_tokens(StringIO(step_6).readline):
    if tok[0] == tokenize.STRING or tok[0] == tokenize.NUMBER:
        print(tok[1])

print("TEST STEP 6")



print("STEP 7")
int_steps = 1
step_7 = transform_tokens(step_6, int_obfuscation)

print(step_7)
step_8 =f"import sys \nsys.setrecursionlimit(99999999); import time; time.sleep(10); print(sys.getrecursionlimit()); time.sleep(3) \nimport base64; exec(base64.b64decode('{base64.b64encode(step_7.encode()).decode()}'))"

with open("aaaa.py", "w") as f:
    f.write(step_8)