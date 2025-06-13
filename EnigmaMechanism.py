
# Helper Functions
def letter_to_index(letter):
    return ord(letter.lower()) - ord('a')

def index_to_letter(index):
    return chr(index + ord('a'))

def next_letter(letter):
    return chr((ord(letter.lower()) - ord('a') + 1) % 26 + ord('a'))

# Plug Board
A_PlugBoardRelations = {"A":"B", "C":"D"}
B_PlugBoardRelations = {v: k for k, v in A_PlugBoardRelations.items()}

def plugboard(letter):
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
        self.wiring = RotorWirings[type -1] # Encryption wiring
        self.ring_setting = letter_to_index(ring_setting) # Ring setting offset
        self.turnover_letter = letter_to_index(next_letter(Turnover[type - 1])) # Turnover values
        self.order = order # Rotor position, be it left, center, or right (1, 2, 3)
        self.rotor_position = letter_to_index(initial_position)
        
    def press(self, input):
        Input_index = letter_to_index(input)

        # Add additional rotation if rotor is on the right side
        if self.order == 3:
            self.rotor_position = self.rotor_position + 1
        else:
            self.rotor_position = self.rotor_position

        # Turnover
        if self.rotor_position == self.turnover_letter:
            self.turnover()

        # Calculate effective rotor shift
        self.effective_rotor_shift = self.rotor_position - self.ring_setting
        
        # Obtain index with applied offsets, encrypt according to rotor wiring, and substract effective rotor shift
        Encryption = (Input_index + self.rotor_position - self.ring_setting) % 26
        Encryption = self.wiring[Encryption]
        Encryption = (letter_to_index(Encryption) - self.effective_rotor_shift) % 26

        return index_to_letter(Encryption).upper()
    
    def turnover(self):
        if self.order > 0:
            Rotors[self.order - 2].rotor_position += 1

# Reflectors 
ReflectorsWiring = ("YRUHQSLDPXNGOKMIEBFZCWVJAT", "FVPJIAOYEDRZXWGCTKUQSBNMHL")

class Reflector():
    def __init__(self, type):
        self.wiring = ReflectorsWiring[letter_to_index(type) - 1]
    
    def reflect(self, input):
        return self.wiring[letter_to_index(input)]
    

R = Reflector("B")
I = Rotor(1, "A", "A", 1)
II = Rotor(2, "A", "A", 2)
III = Rotor(3, "A", "V", 3)



