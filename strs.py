import random
import base64

def split_b64(string: str) -> tuple[str, str]:
    rand = random.randint(0, len(string))
    str1 = base64.b64encode(string[:rand].encode()).decode()
    str2 = base64.b64encode(string[rand:].encode()).decode()
    return f"str(base64.b64decode('{str1}').decode())", f"str(base64.b64decode('{str2}').decode())"

def chr_encode(string: str) -> str:
    result = "".join([f"chr({ord(c)})+" for c in string])[:-1]
    return f"({str(result)})"

def hex_octal_encode(string: str) -> str:
    result = []
    for c in string:
        result.append(f"chr({ord(c)})")
    
    return f"({'+'.join(result)})"

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
        rand = random.randint(0, 2)
        if rand <= 0:
            return f"({chr_encode(string)})"
        elif rand <= 1:
            return f"({hex_octal_encode(string)})"
        #elif rand <= 2:
        #    return f"(str(\"{string}\"))"
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
    string = 'print(str(((((((chr(((6-(-86))+((int((int((int(4334148/81))/(49)))/((202+26)-(150))))+(int(((223+-103))/-60)))))+chr(101)+chr((((+int((258+16)))+-98)+((---10)-58)))+chr(108)+chr((((int((int(3108/37)))-(int((688+643)/(int(-836/76)))))+int(int(-10)))+((+-242)-((int(-11)-int(19))+((int(-256/2)))))))+chr(32)))) + (((chr(int(int(119)))+chr((--(int((--(+(2213+3448)))/(96+int(int(-45)))))))))))) + ((("dlr"[::-((((+(-45--27)))-int(int(-18)))+(int(int((+(+-71)))/-71)))]))))))\nprint(((+1)-(int(0/(+(int(2233/(-28-1))))))) + ((1)-int((int(-31)+(int((int(98890/-55))/(-46-12)))))))\nprint(1.1)'
    str1, str2 = split_b64(string)
    print(f"\"{str1}\" and \"{str2}\"")
    assert eval(f"({str1}) + ({str2})") == string

    str1 = chr_encode(string)
    print(f"{str1}")
    assert eval(str1) == string

    str1 = hex_octal_encode(string)
    print(f"{str1}")
    assert eval(str1) == string

    str1 = reverse_encode(string)
    print(f"{str1}")
    assert eval(str1) == string

    str1 = obf_str(string, 3)
    print(f"{str1}")
    assert eval(str1) == string



if __name__ == "__main__":
    main()