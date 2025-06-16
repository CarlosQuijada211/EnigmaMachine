def roman_to_int(roman):
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 
                    'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_value = 0
    for char in reversed(roman):
        value = roman_values[char]
        if value < prev_value:
            total -= value
        else:
            total += value
            prev_value = value
    return total

def roman_list(roman_string):
    return [roman_to_int(r) for r in roman_string.split()]

def pairs_to_dict(s):
    pairs = s.split()

    seen_letters = set()
    mapping = {}

    for pair in pairs:
        if len(pair) != 2:
            raise ValueError(f"Invalid pair length: '{pair}'")
        a, b = pair[0], pair[1]
        if a in seen_letters or b in seen_letters:
            raise ValueError(f"Repeated letter found: '{a}' or '{b}'")
        seen_letters.update([a, b])
        mapping[a] = b

    return mapping

def step_rotors(rotors):
    right = rotors[2]
    middle = rotors[1]
    left = rotors[0]

    # Double-stepping: if middle rotor is at its notch, it AND left rotor will step
    if middle.at_turnover():
        middle.step()
        left.step()
        print("MIDDLESTEP, LEFTSTEP")

    # If right rotor is at its notch, middle rotor steps
    elif right.at_turnover():
        middle.step()
        print("MIDDLE STEP")

    # Right rotor always steps
    right.step()
    print("RIGHT STEP")
    