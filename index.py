import tkinter as tk
import random

class RPSGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Rock Paper Scissors')

        self.options = ['rock', 'paper', 'scissors']

        self.label = tk.Label(root, text='Choose rock, paper, or scissors:', font=('Arial', 14))
        self.label.pack(pady=10)

        # Buttons for each choice
        self.rock_button = tk.Button(root, text='Rock', command=lambda: self.play('rock'), width=10)
        self.rock_button.pack(side='left', padx=10, pady=10)

        self.paper_button = tk.Button(root, text='Paper', command=lambda: self.play('paper'), width=10)
        self.paper_button.pack(side='left', padx=10, pady=10)

        self.scissors_button = tk.Button(root, text='Scissors', command=lambda: self.play('scissors'), width=10)
        self.scissors_button.pack(side='left', padx=10, pady=10)

        self.result_label = tk.Label(root, text='', font=('Arial', 14))
        self.result_label.pack(pady=20)

    def play(self, user_choice):
        computer_choice = random.choice(self.options)
        if user_choice == computer_choice:
            result = "It's a tie!"
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
             (user_choice == 'paper' and computer_choice == 'rock') or \
             (user_choice == 'scissors' and computer_choice == 'paper'):
            result = "You win!"
        else:
            result = "Computer wins!"
        
        self.result_label.config(text=f'You chose {user_choice}, computer chose {computer_choice}. {result}')


if __name__ == "__main__":
    root = tk.Tk()
    game = RPSGameGUI(root)
    root.mainloop()
