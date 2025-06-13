
# Plug Board
A_PlugBoardRelations = {"A":"B", "C":"D"}
B_PlugBoardRelations = {v: k for k, v in A_PlugBoardRelations.items()}
RotorWirings = ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "ESOVPZJAYQUIRHXLNFTGKDCMWB", "VZBRGITYUPSDNHLXAWMJQOFECK")
Notches = ("Y", "M", "D", "R", "H")

def plugboard(letter):
    if letter in A_PlugBoardRelations: # Check Foward Relations
        return A_PlugBoardRelations[letter]
    elif letter in B_PlugBoardRelations: # Check Backward Relations
        return B_PlugBoardRelations[letter]
    else: # No Relations
        return letter
    
print(plugboard("D"))

# Rotors

class Rotor():
    def __init__(self, type, ring_setting, initial_position):
        self.type = RotorWirings[type -1]
        self.ring_setting = ring_setting
        self.initial_position = initial_position
        self.notch = Notches[type - 1]
        
