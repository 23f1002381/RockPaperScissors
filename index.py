import tkinter as tk
import random
import matplotlib.pyplot as plt  # pyright: ignore[reportMissingModuleSource]
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # pyright: ignore[reportMissingModuleSource]


class EnhancedRPSGUIWithGraph:

    MOTIVATION_QUOTES = [
        "Keep pushing, victory is near!",
        "Every loss is a step to success!",
        "Don't give up, legendary players rise again!",
        "Focus and fight back stronger!",
        "Mistakes are proof you're trying!",
        "The comeback is always stronger than the setback!",
    ]

    def __init__(self, root):
        self.root = root
        self.root.title('Enhanced Rock Paper Scissors with Graph and Stats')

        self.options = ['rock', 'paper', 'scissors']
        self.player_score = 0
        self.computer_score = 0
        self.history = []

        self.player_picks = []
        self.computer_picks = []

        self.player_overtake_count = 0
        self.computer_overtake_count = 0
        self.player_win_count = 0

        # Score labels
        self.score_frame = tk.Frame(root)
        self.score_frame.pack(pady=10)

        self.player_label = tk.Label(self.score_frame, text='Player: 0', font=('Arial', 12))
        self.player_label.pack(side='left', padx=20)
        self.computer_label = tk.Label(self.score_frame, text='Computer: 0', font=('Arial', 12))
        self.computer_label.pack(side='left', padx=20)

        # Overtake count labels
        self.overtake_frame = tk.Frame(root)
        self.overtake_frame.pack(pady=5)

        self.player_overtake_label = tk.Label(self.overtake_frame, text='Player overtakes: 0', font=('Arial', 11))
        self.player_overtake_label.pack(side='left', padx=20)
        self.computer_overtake_label = tk.Label(self.overtake_frame, text='Computer overtakes: 0', font=('Arial', 11))
        self.computer_overtake_label.pack(side='left', padx=20)

        # Player win count label
        self.player_win_label = tk.Label(root, text='Player wins: 0', font=('Arial', 12))
        self.player_win_label.pack(pady=5)

        # Motivational quote label
        self.motivation_label = tk.Label(root, text='', font=('Arial', 11), fg='blue')
        self.motivation_label.pack(pady=5)

        # Buttons for options
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

        for choice in self.options:
            btn = tk.Button(self.buttons_frame, text=choice.capitalize(), command=lambda c=choice: self.play(c), width=10)
            btn.pack(side='left', padx=10, pady=10)

        # Result label
        self.result_label = tk.Label(root, text='', font=('Arial', 14))
        self.result_label.pack(pady=10)

        # Last picks display as full text lines
        self.last_picks_frame = tk.Frame(root)
        self.last_picks_frame.pack(pady=5)

        self.player_picks_text = tk.Label(self.last_picks_frame, text='Player last 5 picks: ', font=('Arial', 12))
        self.player_picks_text.pack(anchor='w')

        self.computer_picks_text = tk.Label(self.last_picks_frame, text='Computer last 5 picks: ', font=('Arial', 12))
        self.computer_picks_text.pack(anchor='w')

        # Reset button
        self.reset_button = tk.Button(root, text='Reset Scores', command=self.reset_scores)
        self.reset_button.pack(pady=10)

        # Matplotlib graph
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.ax.set_title('Score Over Time')
        self.ax.set_xlabel('Rounds')
        self.ax.set_ylabel('Score')
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(pady=10)

    def play(self, user_choice):
        computer_choice = random.choice(self.options)
        result = ''
        player_won_this_round = False

        if user_choice == computer_choice:
            result = "It's a tie!"
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
             (user_choice == 'paper' and computer_choice == 'rock') or \
             (user_choice == 'scissors' and computer_choice == 'paper'):
            result = "You win!"
            self.player_score += 1
            player_won_this_round = True
            self.player_win_count += 1
        else:
            result = "Computer wins!"
            self.computer_score += 1

        # Update picks history
        self.player_picks.append(user_choice)
        if len(self.player_picks) > 5:
            self.player_picks.pop(0)
        self.computer_picks.append(computer_choice)
        if len(self.computer_picks) > 5:
            self.computer_picks.pop(0)

        # Update score history and overtakes counts
        self.history.append((self.player_score, self.computer_score))
        self.update_overtake_counts()
        self.update_scores()
        self.update_graph()
        self.update_picks_display()
        self.update_player_win_count()
        self.update_motivation(player_won_this_round)
        self.result_label.config(text=f'You chose {user_choice}, computer chose {computer_choice}. {result}')

    def update_overtake_counts(self):
        leader = None
        self.player_overtake_count = 0
        self.computer_overtake_count = 0
        for p_score, c_score in self.history:
            if p_score > c_score:
                if leader == 'computer':
                    self.player_overtake_count += 1
                leader = 'player'
            elif c_score > p_score:
                if leader == 'player':
                    self.computer_overtake_count += 1
                leader = 'computer'

        self.player_overtake_label.config(text=f'Player overtakes: {self.player_overtake_count}')
        self.computer_overtake_label.config(text=f'Computer overtakes: {self.computer_overtake_count}')

    def update_scores(self):
        self.player_label.config(text=f'Player: {self.player_score}')
        self.computer_label.config(text=f'Computer: {self.computer_score}')

    def update_player_win_count(self):
        self.player_win_label.config(text=f'Player wins: {self.player_win_count}')

    def update_graph(self):
        self.ax.clear()
        self.ax.set_title('Score Over Time')
        self.ax.set_xlabel('Rounds')
        self.ax.set_ylabel('Score')

        rounds = list(range(1, len(self.history) + 1))
        p_scores = [s[0] for s in self.history]
        c_scores = [s[1] for s in self.history]
        self.ax.plot(rounds, p_scores, label='Player', marker='o')
        self.ax.plot(rounds, c_scores, label='Computer', marker='o')

        leader = None
        for i, (p_score, c_score) in enumerate(self.history):
            if p_score > c_score:
                if leader != 'player':
                    self.ax.plot(i + 1, p_score, 'r*')
                    self.ax.annotate('Player overtook', (i + 1, p_score),
                                     xytext=(i + 2, p_score + 1),
                                     arrowprops=dict(facecolor='red', arrowstyle='->'), fontsize=8)
                leader = 'player'
            elif c_score > p_score:
                if leader != 'computer':
                    self.ax.plot(i + 1, c_score, 'b*')
                    self.ax.annotate('Computer overtook', (i + 1, c_score),
                                     xytext=(i + 2, c_score + 1),
                                     arrowprops=dict(facecolor='blue', arrowstyle='->'), fontsize=8)
                leader = 'computer'

        self.ax.legend()
        self.canvas.draw()

    def update_picks_display(self):
        # Show last 5 picks as text after the label
        player_text = ', '.join(p.capitalize() for p in self.player_picks)
        computer_text = ', '.join(p.capitalize() for p in self.computer_picks)

        self.player_picks_text.config(text=f'Player last 5 picks: {player_text}')
        self.computer_picks_text.config(text=f'Computer last 5 picks: {computer_text}')

    def update_motivation(self, player_won_this_round):
        # Show a motivational quote if player is currently losing or tied
        if self.player_score <= self.computer_score:
            quote = random.choice(self.MOTIVATION_QUOTES)
            self.motivation_label.config(text=quote)
        else:
            # Clear motivation if player is winning
            self.motivation_label.config(text='')

    def reset_scores(self):
        self.player_score = 0
        self.computer_score = 0
        self.player_win_count = 0
        self.history.clear()
        self.player_picks.clear()
        self.computer_picks.clear()
        self.update_scores()
        self.update_graph()
        self.update_picks_display()
        self.update_player_win_count()
        self.motivation_label.config(text='')
        self.player_overtake_label.config(text='Player overtakes: 0')
        self.computer_overtake_label.config(text='Computer overtakes: 0')
        self.result_label.config(text='Scores reset!')


if __name__ == "__main__":
    root = tk.Tk()
    game = EnhancedRPSGUIWithGraph(root)
    root.mainloop()
