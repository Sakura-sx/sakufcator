import random
import base64
import lzma
import bz2

def split_base64(string: str) -> tuple[str, str]:
    rand = random.randint(0, len(string))
    str1 = base64.b64encode(string[:rand].encode()).decode()
    str2 = base64.b64encode(string[rand:].encode()).decode()
    return f"str(base64.b64decode('{str1}').decode())", f"str(base64.b64decode('{str2}').decode())"

def chr_encode(string: str) -> str:
    result = "".join([f"chr({ord(c)})+" for c in string])[:-1]
    return f"({str(result)})"

def b16_lzma(string: str) -> str:
    string = base64.b16encode(lzma.compress(string.encode())).decode()
    return f"str(lzma.decompress(base64.b16decode('{string}')).decode())"

def b16_bz2(string: str) -> str:
    string = base64.b16encode(bz2.compress(string.encode())).decode()
    return f"str(bz2.decompress(base64.b16decode('{string}')).decode())"

def b32_lzma(string: str) -> str:
    string = base64.b32encode(lzma.compress(string.encode())).decode()
    return f"str(lzma.decompress(base64.b32decode('{string}')).decode())"

def b32_bz2(string: str) -> str:
    string = base64.b32encode(bz2.compress(string.encode())).decode()
    return f"str(bz2.decompress(base64.b32decode('{string}')).decode())"

def b64_lzma(string: str) -> str:
    string = base64.b64encode(lzma.compress(string.encode())).decode()
    return f"str(lzma.decompress(base64.b64decode('{string}')).decode())"

def b64_bz2(string: str) -> str:
    string = base64.b64encode(bz2.compress(string.encode())).decode()
    return f"str(bz2.decompress(base64.b64decode('{string}')).decode())"

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

def obf_str(string: str, steps: int, fast_compression: bool) -> str:
    if steps <= 0:
        if fast_compression:
            rand = random.randint(0, 6)
            if rand <= 0:
                return f"({chr_encode(string)})"
            elif rand <= 1:
                return f"(str(\"{string}\"))"
            elif rand <= 2:
                return f"({random.choice([b16_lzma, b16_bz2])(string)})"
            elif rand <= 3:
                return f"({random.choice([b32_lzma, b32_bz2])(string)})"
            elif rand <= 4:
                return f"({random.choice([b64_lzma, b64_bz2])(string)})"
            else:
                return f"({reverse_encode(string)})"
        else:
            encodings = [
                chr_encode(string),
                f'str("{string}")',
                b16_lzma(string),
                b16_bz2(string),
                b32_lzma(string),
                b32_bz2(string),
                b64_lzma(string),
                b64_bz2(string),
                reverse_encode(string)
            ]
            lengths = [len(e) for e in encodings]
            max_len = max(lengths)
            weights = [(max_len - l + 1) for l in lengths]
            chosen = random.choices(encodings, weights=weights, k=1)[0]
            return f"({chosen})"
        
    rand = random.randint(0, len(string))
    str1 = string[:rand]
    str2 = string[rand:]
    
    if len(str1) > 0 and len(str2) > 0:
        return f"(({obf_str(str1, steps-1, fast_compression)}) + ({obf_str(str2, steps-1, fast_compression)}))"
    elif len(str1) > 0:
        return f"({obf_str(str1, steps-1, fast_compression)})"
    elif len(str2) > 0:
        return f"({obf_str(str2, steps-1, fast_compression)})"
    else:
        return f"({string})"

def main():
    fast_compression = False
    string = "lorem ipsum dolor sit amet naoehunhaoeuhtnaoehuhanoehuhaonehuhnhoneu hnahoeudthnudihtdeuothdit dthued htdoeuhtidtoeudutihdeuhtditdeuhtnidtoeuditoeuditeuditdtho  deuhtidoehtuidthoeduthid"
    str1, str2 = split_base64(string)
    print(f"\"{str1}\" and \"{str2}\"")
    assert eval(f"({str1}) + ({str2})") == string

    chr_encoded = chr_encode(string)
    print(f"{chr_encoded}")
    assert eval(chr_encoded) == string

    b16_lzma_encoded = b16_lzma(string)
    print(f"{b16_lzma_encoded}")
    print(eval(b16_lzma_encoded))
    assert eval(b16_lzma_encoded) == string

    b16_bz2_encoded = b16_bz2(string)
    print(f"{b16_bz2_encoded}")
    assert eval(b16_bz2_encoded) == string

    b32_lzma_encoded = b32_lzma(string)
    print(f"{b32_lzma_encoded}")
    assert eval(b32_lzma_encoded) == string

    b32_bz2_encoded = b32_bz2(string)
    print(f"{b32_bz2_encoded}")
    assert eval(b32_bz2_encoded) == string

    b64_lzma_encoded = b64_lzma(string)
    print(f"{b64_lzma_encoded}")
    assert eval(b64_lzma_encoded) == string

    b64_bz2_encoded = b64_bz2(string)
    print(f"{b64_bz2_encoded}")
    assert eval(b64_bz2_encoded) == string

    reverse_encoded = reverse_encode(string)
    print(f"{reverse_encoded}")
    assert eval(reverse_encoded) == string

    obf_str_encoded = obf_str(string, 3, fast_compression)
    print(f"{obf_str_encoded}")
    assert eval(f"({obf_str_encoded})") == string

    print(f"Length of string: {len(string)} (100%)")
    print(f"Length of chr_encoded: {len(chr_encoded)} ({len(chr_encoded)/len(string)*100:.2f}%)")
    print(f"Length of b16_lzma_encoded: {len(b16_lzma_encoded)} ({len(b16_lzma_encoded)/len(string)*100:.2f}%)")
    print(f"Length of b16_bz2_encoded: {len(b16_bz2_encoded)} ({len(b16_bz2_encoded)/len(string)*100:.2f}%)")
    print(f"Length of b32_lzma_encoded: {len(b32_lzma_encoded)} ({len(b32_lzma_encoded)/len(string)*100:.2f}%)")
    print(f"Length of b32_bz2_encoded: {len(b32_bz2_encoded)} ({len(b32_bz2_encoded)/len(string)*100:.2f}%)")
    print(f"Length of b64_lzma_encoded: {len(b64_lzma_encoded)} ({len(b64_lzma_encoded)/len(string)*100:.2f}%)")
    print(f"Length of b64_bz2_encoded: {len(b64_bz2_encoded)} ({len(b64_bz2_encoded)/len(string)*100:.2f}%)")
    print(f"Length of reverse_encoded: {len(reverse_encoded)} ({len(reverse_encoded)/len(string)*100:.2f}%)")
    print(f"Avg: {(len(chr_encoded)+len(b16_lzma_encoded)+len(b16_bz2_encoded)+len(b32_lzma_encoded)+len(b32_bz2_encoded)+len(b64_lzma_encoded)+len(b64_bz2_encoded)+len(reverse_encoded))/8} ({((len(chr_encoded)+len(b16_lzma_encoded)+len(b16_bz2_encoded)+len(b32_lzma_encoded)+len(b32_bz2_encoded)+len(b64_lzma_encoded)+len(b64_bz2_encoded)+len(reverse_encoded))/8)/len(string)*100:.2f}%)")
    print(f"Real avg: {len(obf_str_encoded)} ({len(obf_str_encoded)/len(string)*100:.2f}%)")

if __name__ == "__main__":
    main()