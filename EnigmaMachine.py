from EnigmaMechanism import *
from Helper import roman_list, pairs_to_dict, step_rotors

# Configuration

# Rotors
print("Input rotor types from left to right. Ex: (I II III)")
RotorOrder = input(">")
RotorOrder = roman_list(RotorOrder)

# Ring Settings
print("Input ring settings from left to right in rotor order. Ex: (A B C)")
RingSettings = input(">")
RingSettings = RingSettings.split()

# Plugboard Settings
print("Input plugboard settings in pairs.")
PB = input(">")
PB = pairs_to_dict(PB)

# Initial Rotor Positions
print("Input initial rotor positions. Ex (F D V)")
InitialRotorOrder = input(">")
InitialRotorOrder = InitialRotorOrder.split()

# Reflector
print("Choose Reflector B or C")
ReflectorType = input(">")

# Set Configuration
R_left = Rotor(RotorOrder[0], RingSettings[0], InitialRotorOrder[0], 1)
R_middle = Rotor(RotorOrder[1], RingSettings[1], InitialRotorOrder[1], 2)
R_right = Rotor(RotorOrder[2], RingSettings[2], InitialRotorOrder[2], 3)
Rotors = (R_left, R_middle, R_right)
reflector = Reflector(ReflectorType)

# Run Enigma

original_message = []

print("Input encrypted message:")
ciphertext = input("> ").upper()

for char in ciphertext:
    if not char.isalpha():
        continue  # Skip non-alphabetic characters

    # Step the rotors before each key press
    step_rotors(Rotors)

    # Pass through plugboard
    value = plugboard(char, PB)
    print(f"Plugboard → {value}")

    # Forward through rotors
    value = R_right.press(value)
    print(f"Right Rotor → {value}")
    value = R_middle.press(value)
    print(f"Middle Rotor → {value}")
    value = R_left.press(value)
    print(f"Left Rotor → {value}")

    # Reflector
    value = reflector.reflect(value)
    print(f"Reflector → {value}")

    # Backward through rotors
    value = R_left.returnal(value)
    print(f"Left Rotor ← {value}")
    value = R_middle.returnal(value)
    print(f"Middle Rotor ← {value}")
    value = R_right.returnal(value)
    print(f"Right Rotor ← {value}")

    # Pass again through plugboard
    value = plugboard(value, PB)
    print(f"Plugboard → {value}")

    original_message.append(value)

# Output decrypted message
decrypted = ''.join(original_message)
print("\nDecrypted message:")
print(decrypted)


