from Helper import letter_to_index, index_to_letter

# Plug Board
def plugboard(letter, A_PlugBoardRelations):

    B_PlugBoardRelations = {v: k for k, v in A_PlugBoardRelations.items()}

    if letter in A_PlugBoardRelations: # Check Foward Relations
        return A_PlugBoardRelations[letter]
    elif letter in B_PlugBoardRelations: # Check Backward Relations
        return B_PlugBoardRelations[letter]
    else: # No Relations
        return letter

# Rotors
RotorWirings = ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "BDFHJLCPRTXVZNYEIWGAKMUSQO", "ESOVPZJAYQUIRHXLNFTGKDCMWB", "VZBRGITYUPSDNHLXAWMJQOFECK")
Turnover = ("Q", "E", "V", "J", "Z")

class Rotor():
    def __init__(self, type, ring_setting, initial_position, order):
        self.type = type
        self.wiring = RotorWirings[int(type) -1] # Encryption wiring
        self.ring_setting = letter_to_index(ring_setting) # Ring setting offset
        self.turnover_letter = letter_to_index(Turnover[type - 1]) # Turnover values
        self.order = order # Rotor position, be it left, center, or right (1, 2, 3)
        self.rotor_position = letter_to_index(initial_position)

        # Reverse wiring for signal's return
        self.reverse_wiring = [''] * 26
        for i, letter in enumerate(self.wiring):
            self.reverse_wiring[letter_to_index(letter)] = index_to_letter(i)
    
    def __str__(self):
        return self.type
        
    def press(self, input):
        Input_index = letter_to_index(input)

        # Calculate effective rotor shift
        self.effective_rotor_shift = self.rotor_position - self.ring_setting
        
        # Obtain index with applied offsets, encrypt according to rotor wiring, and substract effective rotor shift
        Encryption = (Input_index + self.rotor_position - self.ring_setting) % 26
        Encryption = self.wiring[Encryption]
        Encryption = (letter_to_index(Encryption) - self.effective_rotor_shift) % 26

        return index_to_letter(Encryption).upper()
    
    def returnal(self, input):
        Input_index = letter_to_index(input)

        # Calculate effective rotor shift
        self.effective_rotor_shift = self.rotor_position - self.ring_setting
        
        # Obtain index with applied offsets, encrypt according to rotor wiring, and substract effective rotor shift
        Encryption = (Input_index + self.rotor_position - self.ring_setting) % 26
        Encryption = self.reverse_wiring[Encryption]
        Encryption = (letter_to_index(Encryption) - self.effective_rotor_shift) % 26

        return index_to_letter(Encryption).upper()
    
    def at_turnover(self):
        return self.rotor_position == self.turnover_letter

    def step(self):
        self.rotor_position = (self.rotor_position + 1) % 26

# Reflectors 
ReflectorsWiring = ("YRUHQSLDPXNGOKMIEBFZCWVJAT", "FVPJIAOYEDRZXWGCTKUQSBNMHL")

class Reflector():
    def __init__(self, type):
        self.type = type
        self.wiring = ReflectorsWiring[0] if type == "UKW-B" else ReflectorsWiring[1]
    
    def __str__(self):
        return self.type
        
    def reflect(self, input):
        return self.wiring[letter_to_index(input)]






