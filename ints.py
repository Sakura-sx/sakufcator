import random
import math

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

def calculate_dynamic_weights(original_length, steps):
    fixed_overheads = {
        'int_wrap': 5,
        'paren_wrap': 2,
        'plus_wrap': 3,
        'minus_wrap': 4,
        'sum_op': 3,
        'subtract_op': 3,
        'divide_op': 7,
    }
    
    length_multipliers = {
        'sum_op': 1.89,
        'subtract_op': 2.15,
        'divide_op': 3.75
    }
    
    simple_lengths = {
        'int_wrap': original_length + fixed_overheads['int_wrap'],
        'paren_wrap': original_length + fixed_overheads['paren_wrap'],
        'plus_wrap': original_length + fixed_overheads['plus_wrap'],
        'minus_wrap': original_length + fixed_overheads['minus_wrap'],
        'base_case': original_length
    }
    
    recursive_factor = 1.0
    for step in range(steps):
        recursive_factor *= 0.8
    
    estimated_recursive_length = original_length * recursive_factor
    
    complex_lengths = {}
    for op_type in ['sum_op', 'subtract_op', 'divide_op']:
        estimated_total = (length_multipliers[op_type] * estimated_recursive_length * 2) + fixed_overheads[op_type]
        complex_lengths[op_type] = estimated_total
    
    all_lengths = {**simple_lengths, **complex_lengths}
    
    weights = {}
    total_inverse = 0
    
    for transform_type, est_length in all_lengths.items():
        inverse_length = 1.0 / max(est_length, 1)
        weights[transform_type] = inverse_length
        total_inverse += inverse_length
    
    cumulative = 0
    ranges = {}
    
    for transform_type in ['int_wrap', 'paren_wrap', 'sum_op', 'subtract_op', 'divide_op', 'plus_wrap', 'minus_wrap', 'base_case']:
        if transform_type in weights:
            normalized_weight = (weights[transform_type] / total_inverse) * 100
            ranges[transform_type] = (cumulative, cumulative + normalized_weight)
            cumulative += normalized_weight
    
    return ranges

def obf_int(integer: int, steps: int):
    if steps <= 0:
        return str(int(integer))
    
    original_length = len(str(integer))
    weight_ranges = calculate_dynamic_weights(original_length, steps)
    rand_val = random.uniform(0, 100)
    
    if rand_val <= weight_ranges['int_wrap'][1]:
        return f"int({obf_int(integer, steps-1)})"
    elif rand_val <= weight_ranges['paren_wrap'][1]:
        return f"({obf_int(integer, steps-1)})"
    elif rand_val <= weight_ranges['sum_op'][1]:
        num1, num2 = sum(integer)
        return f"({obf_int(num1, steps-1)}+{obf_int(num2, steps-1)})"
    elif rand_val <= weight_ranges['subtract_op'][1]:
        num1, num2 = subtract(integer)
        return f"({obf_int(num1, steps-1)}-{obf_int(num2, steps-1)})"
    elif rand_val <= weight_ranges['divide_op'][1]:
        num1, num2 = divide(integer)
        return f"(int({obf_int(num1, steps-1)}/{obf_int(num2, steps-1)}))"
    elif rand_val <= weight_ranges['plus_wrap'][1]:
        return f"(+{obf_int(integer, steps-1)})"
    elif rand_val <= weight_ranges['minus_wrap'][1]:
        return f"(--{obf_int(integer, steps-1)})"
    else:
        return str(int(integer))
def main():
    integer = 69

    num1, num2 = sum(integer)
    sum_result = f"({num1}+{num2})"
    print(sum_result)
    print(num1+num2)

    num1, num2 = subtract(integer)
    subtract_result = f"({num1}+{num2})"
    print(subtract_result)
    print(num1+num2)


    num1, num2 = divide(integer)
    divide_result = f"(int({num1}/{num2}))"
    print(divide_result)
    print(int(num1/num2))

    obf_int_result = f"{obf_int(integer, 15)}"
    print(obf_int_result)
    print(eval(obf_int_result))

    print(f"Length of integer: {len(str(integer))} (100%)")
    print(f"Length of sum: {len(str(sum_result))} ({len(str(sum_result))/len(str(integer))*100:.2f}%)")
    print(f"Length of subtract: {len(str(subtract_result))} ({len(str(subtract_result))/len(str(integer))*100:.2f}%)")
    print(f"Length of divide: {len(str(divide_result))} ({len(str(divide_result))/len(str(integer))*100:.2f}%)")
    print(f"Avg: {((len(str(sum_result))+len(str(subtract_result))+len(str(divide_result)))/3)/len(str(integer))*100:.2f}%")
    print(f"Real avg: {len(str(obf_int_result))/len(str(integer))*100:.2f}%")

if __name__ == "__main__":
    main()