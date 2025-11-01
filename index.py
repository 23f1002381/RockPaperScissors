import tkinter as tk
import random

class EnhancedRPSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Enhanced Rock Paper Scissors')

        self.options = ['rock', 'paper', 'scissors']
        self.player_score = 0
        self.computer_score = 0

        # Score Labels
        self.score_frame = tk.Frame(root)
        self.score_frame.pack(pady=10)

        self.player_label = tk.Label(self.score_frame, text='Player: 0', font=('Arial', 12))
        self.player_label.pack(side='left', padx=20)
        self.computer_label = tk.Label(self.score_frame, text='Computer: 0', font=('Arial', 12))
        self.computer_label.pack(side='left', padx=20)

        # Buttons
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

        for choice in self.options:
            btn = tk.Button(self.buttons_frame, text=choice.capitalize(), command=lambda c=choice: self.play(c), width=10)
            btn.pack(side='left', padx=10, pady=10)

        # Result label
        self.result_label = tk.Label(root, text='', font=('Arial', 14))
        self.result_label.pack(pady=10)

        # Reset button
        self.reset_button = tk.Button(root, text='Reset Scores', command=self.reset_scores)
        self.reset_button.pack(pady=10)

    def play(self, user_choice):
        computer_choice = random.choice(self.options)
        result = ''
        if user_choice == computer_choice:
            result = "It's a tie!"
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
             (user_choice == 'paper' and computer_choice == 'rock') or \
             (user_choice == 'scissors' and computer_choice == 'paper'):
            result = "You win!"
            self.player_score += 1
        else:
            result = "Computer wins!"
            self.computer_score += 1

        self.update_scores()
        self.result_label.config(text=f'You chose {user_choice}, computer chose {computer_choice}. {result}')

    def update_scores(self):
        self.player_label.config(text=f'Player: {self.player_score}')
        self.computer_label.config(text=f'Computer: {self.computer_score}')

    def reset_scores(self):
        self.player_score = 0
        self.computer_score = 0
        self.update_scores()
        self.result_label.config(text='Scores reset!')

if __name__ == "__main__":
    root = tk.Tk()
    game = EnhancedRPSGUI(root)
    root.mainloop()
