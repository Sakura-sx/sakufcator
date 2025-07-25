import random

def sum(integer: int):
    if integer == 0:
        modifier = random.randint(-100, 100)
        return modifier, modifier*-1
    if integer > 0:
        modifier = random.randint(integer*-1, integer)
    else:
        modifier = random.randint(integer, integer*-1)

    return integer-modifier, modifier

def subtract(integer: int):
    if integer == 0:
        modifier = random.randint(-100, 100)
        return modifier, modifier
    if integer > 0:
        modifier = random.randint(integer*-2, integer*2)
    else:
        modifier = random.randint(integer*2, integer*-2)

    return integer+modifier, modifier
    
def divide(integer: int):
    modifier = random.randint(-100, 100)
    if modifier == 0:
        modifier = -1
    return integer*modifier, modifier

def obf_int(integer: int, steps: int):
    if steps <= 0:
        return int(integer)
    type = random.randint(0,100)
    if type <= 8:
        return f"int({obf_int(integer, steps-1)})"
    if type <= 16:
        return f"({obf_int(integer, steps-1)})"
    if type <= 32:
        num1, num2 = sum(integer)
        return(f"({obf_int(num1, steps-1)}+{obf_int(num2, steps-1)})")
    if type <= 48:
        num1, num2 = subtract(integer)
        return(f"({obf_int(num1, steps-1)}-{obf_int(num2, steps-1)})")
    if type <= 64:
        num1, num2 = divide(integer)
        return(f"(int({obf_int(num1, steps-1)}/{obf_int(num2, steps-1)}))")
    if type <= 72:
        return f"(+{obf_int(integer, steps-1)})"
    if type <= 80:
        return f"(--{obf_int(integer, steps-1)})"
    else:
        return int(integer)
def main():
    integer = 69

    num1, num2 = sum(integer)
    result = f"({num1}+{num2})"
    print(result)
    print(num1+num2)

    num1, num2 = subtract(integer)
    result = f"({num1}+{num2})"
    print(result)
    print(num1+num2)


    num1, num2 = divide(integer)
    result = f"(int({num1}/{num2}))"
    print(result)
    print(int(num1/num2))

    print(f"{obf_int(integer, 15)}")

if __name__ == "__main__":
    main()