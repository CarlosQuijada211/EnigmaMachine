import tkinter as tk
from tkinter import ttk
from EnigmaMechanism import *
from Helper import roman_to_int, pairs_to_dict, step_rotors

class EnigmaConfigFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.reflectors = ["UKW-B", "UKW-C"]
        self.rotors = ["I", "II", "III", "IV", "V"]
        self.letters = [chr(i) for i in range(ord("A"), ord("Z")+1)]

        self.reflector_var = tk.StringVar(value=self.reflectors[0])
        self.rotor_vars = []
        self.ring_vars = []
        self.pos_vars = []

        self.build_ui()

    def build_ui(self):
        # Row 0: Reflector + Rotor Labels
        tk.Label(self, text="Reflector:").grid(row=0, column=0)
        ttk.Combobox(self, textvariable=self.reflector_var, values=self.reflectors, state="readonly", width=7).grid(row=0, column=1)

        for i, label in enumerate(["1st Rotor:", "2nd Rotor:", "3rd Rotor:"]):
            tk.Label(self, text=label).grid(row=0, column=2+i*2, columnspan=2)

        # Row 1: Rotor Selection
        tk.Label(self, text="Rotor Type").grid(row=1, column=0, columnspan=2)
        for i in range(3):
            var = tk.StringVar(value=self.rotors[i])
            ttk.Combobox(self, textvariable=var, values=self.rotors, state="readonly", width=5).grid(row=1, column=2+i*2, columnspan=2)
            self.rotor_vars.append(var)

        # Row 2: Ring Setting
        tk.Label(self, text="Ring Setting").grid(row=2, column=0, columnspan=2)
        for i in range(3):
            var = tk.StringVar(value="A")
            ttk.Combobox(self, textvariable=var, values=self.letters, state="readonly", width=5).grid(row=2, column=2+i*2, columnspan=2)
            self.ring_vars.append(var)

        # Row 3: Initial Position
        tk.Label(self, text="Initial Position").grid(row=3, column=0, columnspan=2)
        for i in range(3):
            var = tk.StringVar(value="A")
            ttk.Combobox(self, textvariable=var, values=self.letters, state="readonly", width=5).grid(row=3, column=2+i*2, columnspan=2)
            self.pos_vars.append(var)

        # Row 4: Plugin Label
        tk.Label(self, text="Input plugboard settings in pairs:").grid(row=4, column=0, columnspan=8, pady=5)

        # Row 5: Plug in entry
        self.plugin = tk.Entry(self, width=30)
        self.plugin.grid(row=5, column=0, columnspan=8)

        # Row 6: Warning
        self.warning = tk.Label(self, text="", fg="red")
        self.warning.grid(row=6, column=0, columnspan=8)

        # Row 7: Submit Button
        tk.Button(self, text="Submit", command=self.on_submit).grid(row=7, column=0, columnspan=8, pady=10)

    def clean_up(self):
        self.warning.config(text="")

    def on_submit(self):
        config = self.get_configuration()

        # No error -> Send information and go to next frame
        if config[0] is True:
            config = config[1]
            self.controller.show_frame("ResultFrame", config)

        # If error found, display error message
        elif config[0] is False:
            self.warning.config(text=config[1])

    def get_configuration(self):
        # Get Values
        reflector =  self.reflector_var.get()
        rotors = [roman_to_int(v.get()) for v in self.rotor_vars]
        ring_settings = [v.get() for v in self.ring_vars]
        initial_positions = [v.get() for v in self.pos_vars]

        # Check validity of plugin value
        try:
            plugin = pairs_to_dict(self.plugin.get())
        except ValueError as e:
            return (False, str(e))
        
        # Create dictionary with values
        configuration = {
            "reflector": reflector,
            "rotors": rotors,
            "ring_settings": ring_settings,
            "initial_positions": initial_positions,
            "plugin": plugin
        }

        # Return if no error was found
        return (True, configuration)

class ResultFrame(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.R_left = None
        self.R_middle = None
        self.R_right = None
        self.Rotors = None
        self.reflector = None
        self.plugboard_settings = None

        # UI elements — created once
        tk.Label(self, text="Enigma Machine", font=("Helvetica", 10, "bold")).grid(row=0, column=0)
        tk.Label(self, text="Input encrypted message:").grid(row=1, column=0)

        self.cyphertext = tk.Entry(self, width=30)
        self.cyphertext.grid(row=3, column=0, padx=30, pady=5)

        self.result_var = tk.StringVar()
        self.result = tk.Label(self, textvariable=self.result_var)
        self.result.grid(row=4, column=0)

        button_frame = tk.Frame(self)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Return", command=lambda: self.controller.show_frame("EnigmaConfigFrame")).pack(side="left", padx=10)
        tk.Button(button_frame, text="Decrypt", command=self.decrypt_process).pack(side="left", padx=10)

        self.data = None  # To store current machine config


    def display_data(self, data):
        # Save the config data for later use in decryption
        self.data = data
        self.configure_machine(data)
        self.result_var.set("")  # Clear previous output
        self.cyphertext.delete(0, tk.END)  # Clear previous input


    def decrypt_process(self):
        self.configure_machine(self.data)  # Make sure machine is in correct state

        cyphertext = self.cyphertext.get()
        if cyphertext.strip() == "":
            self.result_var.set("Please enter a valid message to decrypt.")
            self.result.config(fg="red")
        else:
            result = self.decrypt_message(cyphertext)
            self.result_var.set(f"Decrypted Message: {result}")
            self.result.config(fg="black")

    def configure_machine(self, data):
        # Reflector 
        self.reflector = Reflector(data["reflector"])

        # Rotors
        self.R_left = Rotor(data["rotors"][0], data["ring_settings"][0], data["initial_positions"][0], 1)
        self.R_middle = Rotor(data["rotors"][1], data["ring_settings"][1], data["initial_positions"][1], 2)
        self.R_right = Rotor(data["rotors"][2], data["ring_settings"][2], data["initial_positions"][2], 3)
        self.Rotors = (self.R_left, self.R_middle, self.R_right)

        # PlugBoard
        self.plugboard_settings = data["plugin"]

    def decrypt_message(self, text):
        """
        Decrypts the ciphertext entered in the input field using the configured Enigma machine settings.
        Iterates through each character, steps the rotors, passes the character through the plugboard, rotors, reflector,
        and then back through the rotors and plugboard to reconstruct the original message.
        Non-alphabetic characters are ignored.
        """
        original_message = []

        ciphertext = text

        for char in ciphertext:
            if not char.isalpha():
                continue # Skip non-alphabetic characters

            char = char.upper()  # Ensure uppercase for consistency

            # Step the rotors before each "key press"
            step_rotors(self.Rotors)

            # Pass through plugboard
            value = plugboard(char, self.plugboard_settings)

            # Forward through rotors
            value = self.R_right.press(value)
            value = self.R_middle.press(value)
            value = self.R_left.press(value)

            # Reflector
            value = self.reflector.reflect(value)

            # Backward through rotors
            value = self.R_left.returnal(value)
            value = self.R_middle.returnal(value)
            value = self.R_right.returnal(value)

            # Pass through plugboard again
            value = plugboard(value, self.plugboard_settings)

            # Add to original message
            original_message.append(value)

        # Output decrypted message
        decrypted = ''.join(original_message)
        return decrypted



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enigma UI Navigation")

        # Dictionary to hold frames
        self.frames = {}

        container = tk.Frame(self)
        container.pack(fill="both", expand=False)

        # Initialize frames
        self.frames["EnigmaConfigFrame"] = EnigmaConfigFrame(container, self)
        self.frames["ResultFrame"] = ResultFrame(container, self)

        # Pack only the initial frame
        self.current_frame = None
        self.show_frame("EnigmaConfigFrame")

    def show_frame(self, frame_name, data=None):
        if self.current_frame:
            self.current_frame.pack_forget()

        frame = self.frames[frame_name]
        frame.pack(fill="both", expand=False)
        self.current_frame = frame

        # Optional data injection
        if frame_name == "ResultFrame" and data:
            frame.display_data(data)
        
        # Clean up previous frame
        if frame_name == "EnigmaConfigFrame":
            frame.clean_up()

if __name__ == "__main__":
    app = App()
    app.mainloop()
