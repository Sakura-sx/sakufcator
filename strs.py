import random

def split(string: str) -> tuple[str, str]:
    rand = random.randint(0, len(string))
    return string[:rand], string[rand:]

def chr_encode(string: str) -> str:
    return "".join([f"chr({ord(c)})+" for c in string])[:-1]

def hex_octal_encode(string: str) -> str:
    result = ""
    for c in string:
        rand = random.randint(0, 1)
        if rand == 0:
            result += f"\\x{ord(c):02x}"
        else:
            result += f"\\{ord(c):o}"
    
    return f"\"{result}\""

def reverse_encode(string: str) -> str:
    return f"\"{string[::-1]}\"[::-1]"

def obf_str(string: str, steps: int) -> str:
    if steps <= 0:
        rand = random.randint(0, 3)
        if rand <= 0:
            return f"({chr_encode(string)})"
        elif rand <= 1:
            return f"({hex_octal_encode(string)})"
        elif rand <= 2:
            return f"(str({string}))"
        else:
            return f"({reverse_encode(string)})"
        
    str1, str2 = split(string)
    return f"({obf_str(str1, steps-1)} + {obf_str(str2, steps-1)})"

def main():
    string = "lorem ipsum dolor sit amet"
    str1, str2 = split(string)
    print(f"\"{str1}\" and \"{str2}\"")

    str1 = chr_encode(string)
    print(f"{str1}")

    str1 = hex_octal_encode(string)
    print(f"{str1}")

    str1 = reverse_encode(string)
    print(f"{str1}")

    str1 = obf_str(string, 3)
    print(f"{str1}")



if __name__ == "__main__":
    main()