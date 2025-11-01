import tkinter as tk
import random
import matplotlib.pyplot as plt  # pyright: ignore[reportMissingModuleSource]
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # pyright: ignore[reportMissingModuleSource]


class EnhancedRPSGUIWithGraph:
    def __init__(self, root):
        self.root = root
        self.root.title('Enhanced Rock Paper Scissors with Graph')

        self.options = ['rock', 'paper', 'scissors']
        self.player_score = 0
        self.computer_score = 0
        self.history = []  # Track history of scores

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

        # Matplotlib figure for graph
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.ax.set_title('Score Over Time')
        self.ax.set_xlabel('Rounds')
        self.ax.set_ylabel('Score')

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(pady=10)

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

        self.history.append((self.player_score, self.computer_score))
        self.update_scores()
        self.update_graph()
        self.result_label.config(text=f'You chose {user_choice}, computer chose {computer_choice}. {result}')

    def update_scores(self):
        self.player_label.config(text=f'Player: {self.player_score}')
        self.computer_label.config(text=f'Computer: {self.computer_score}')

    def update_graph(self):
        self.ax.clear()
        self.ax.set_title('Score Over Time')
        self.ax.set_xlabel('Rounds')
        self.ax.set_ylabel('Score')
        rounds = list(range(1, len(self.history) + 1))
        player_scores = [s[0] for s in self.history]
        computer_scores = [s[1] for s in self.history]
        
        self.ax.plot(rounds, player_scores, label='Player', marker='o')
        self.ax.plot(rounds, computer_scores, label='Computer', marker='o')

        # Find first round where player overtakes computer
        overtaken_index = None
        for i, (p_score, c_score) in enumerate(self.history):
            if p_score > c_score:
                overtaken_index = i + 1  # rounds are 1-based
                break

        if overtaken_index is not None:
            # Annotate the overtaking point
            self.ax.annotate(
                f'Player overtook\nPlayer: {player_scores[overtaken_index - 1]}, Computer: {computer_scores[overtaken_index - 1]}',
                xy=(overtaken_index, player_scores[overtaken_index - 1]),
                xytext=(overtaken_index + 1, player_scores[overtaken_index - 1] + 1),
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                fontsize=9,
                bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.5)
            )
            # Mark the overtaking point with a red dot
            self.ax.plot(overtaken_index, player_scores[overtaken_index - 1], 'ro')

        self.ax.legend()
        self.canvas.draw()

    def reset_scores(self):
        self.player_score = 0
        self.computer_score = 0
        self.history.clear()
        self.update_scores()
        self.update_graph()
        self.result_label.config(text='Scores reset!')


if __name__ == "__main__":
    root = tk.Tk()
    game = EnhancedRPSGUIWithGraph(root)
    root.mainloop()
