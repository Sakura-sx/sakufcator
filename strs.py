import random
import base64
import gzip

def split_base64(string: str) -> tuple[str, str]:
    rand = random.randint(0, len(string))
    str1 = base64.b64encode(string[:rand].encode()).decode()
    str2 = base64.b64encode(string[rand:].encode()).decode()
    return f"str(base64.b64decode('{str1}').decode())", f"str(base64.b64decode('{str2}').decode())"

def chr_encode(string: str) -> str:
    result = "".join([f"chr({ord(c)})+" for c in string])[:-1]
    return f"({str(result)})"

def b16(string: str) -> str:
    string = base64.b16encode(string.encode()).decode()
    return f"str(base64.b16decode('{string}').decode())"

def b32(string: str) -> str:
    string = base64.b32encode(string.encode()).decode()
    return f"str(base64.b32decode('{string}').decode())"

def b64(string: str) -> str:
    string = base64.b64encode(string.encode()).decode()
    return f"str(base64.b64decode('{string}').decode())"

def b64_gzip(string: str) -> str:
    return f"str(gzip.decompress(base64.b64decode('{str(base64.b64encode(gzip.compress(string.encode())).decode())}')).decode())"

def reverse_encode(string: str) -> str:
    # Check if string contains characters that could cause issues
    if '\n' in string or '\\' in string or '"' in string or "'" in string:
        # Use chr() for all characters to avoid any escaping issues
        result = []
        for c in reversed(string):
            result.append(f"chr({ord(c)})")
        return f"({'+'.join(result)})"
    else:
        return f"{repr(string[::-1])}[::-1]"

def obf_str(string: str, steps: int) -> str:
    if steps <= 0:
        rand = random.randint(0, 6)
        if rand <= 0:
            return f"({chr_encode(string)})"
        elif rand <= 1:
            return f"(str(\"{string}\"))"
        elif rand <= 2:
            return f"({b16(string)})"
        elif rand <= 3:
            return f"({b32(string)})"
        elif rand <= 4:
            return f"({b64(string)})"
        elif rand <= 5:
            return f"({b64_gzip(string)})"
        else:
            return f"({reverse_encode(string)})"
        
    rand = random.randint(0, len(string))
    str1 = string[:rand]
    str2 = string[rand:]
    
    if len(str1) > 0 and len(str2) > 0:
        return f"(({obf_str(str1, steps-1)}) + ({obf_str(str2, steps-1)}))"
    elif len(str1) > 0:
        return f"({obf_str(str1, steps-1)})"
    elif len(str2) > 0:
        return f"({obf_str(str2, steps-1)})"
    else:
        return f"({string})"

def main():
    string = "lorem ipsum dolor sit amet"
    str1, str2 = split_base64(string)
    print(f"\"{str1}\" and \"{str2}\"")
    assert eval(f"({str1}) + ({str2})") == string

    str1 = chr_encode(string)
    print(f"{str1}")
    assert eval(str1) == string

    str1 = b16(string)
    print(f"{str1}")
    assert eval(str1) == string

    str1 = b32(string)
    print(f"{str1}")
    assert eval(str1) == string

    str1 = b64(string)
    print(f"{str1}")
    assert eval(str1) == string

    str1 = b64_gzip(string)
    print(f"{str1}")
    print(eval(str1))
    assert eval(str1) == string

    str1 = reverse_encode(string)
    print(f"{str1}")
    assert eval(str1) == string

    str1 = obf_str(string, 3)
    print(f"{str1}")
    assert eval(f"({str1})") == string



if __name__ == "__main__":
    main()