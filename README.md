# Sakuftator
## Python obfuscator made by me (Sakura)
This project is mostly to get better at python syntax and is not intended for production usage.
I also do not really think security through obscurity is that good anyways.

# Features
- Removes comments
- Strings and integers obfuscation
- Variable flattening
- Gzip for compression
- Obfuscates to a one-liner

# Installation
```bash
git clone https://github.com/Sakura-sx/Sakuftator.git
cd Sakuftator
```

# Usage
```bash
python3 main.py <input_file> [output_file]
```
Note: I have not tested too much for long files, if you get an error of `RecursionError: maximum recursion depth exceeded` try lowering the `obf_steps` variable to 1 in the `main.py` file.