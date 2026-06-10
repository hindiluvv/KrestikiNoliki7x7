import tkinter as tk
from enum import Enum
import random

class Player(Enum):
    X = 1
    O = 2

class TicTacToe7x7:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Крестики-нолики 7x7")
        self.root.geometry("1000x700")
        self.root.configure(bg="#fafafa")
        
        self.board = [[None]*7 for _ in range(7)]
        self.current = Player.X
        self.x_score = self.o_score = 0
        self.winner = None
        self.win_line = []
        self.highlight = "#1a5490"
        self.buttons = []
        
        self.main_menu()
    
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()
    
    def main_menu(self):
        self.clear()
        self.root.configure(bg="#fafafa")
        card = tk.Frame(self.root, bg="#ffffff", relief="flat")
        card.place(relx=0.5, rely=0.45, anchor="center", width=500, height=300)
        
        tk.Label(card, text="Крестики-нолики 7×7", bg="#ffffff", fg="#1a2a3a", font=("Helvetica", 28, "normal")).pack(pady=(50, 40))
        tk.Button(card, text="Новая игра", bg="#1a2a3a", fg="white", font=("Helvetica", 14), relief="flat", width=20, height=2, cursor="hand2", command=self.setup).pack(pady=5)
        tk.Button(card, text="Настройки", bg="#ffffff", fg="#1a2a3a", font=("Helvetica", 14), relief="solid", bd=1, width=20, height=2, cursor="hand2", command=self.settings).pack(pady=5)
    
    def settings(self):
        self.clear()
        self.root.configure(bg="#fafafa")
        colors = ["#1a5490", "#2ecc71", "#3498db", "#f1c40f", "#9b59b6", "#ff7f50"]
        card = tk.Frame(self.root, bg="#ffffff", relief="flat")
        card.place(relx=0.5, rely=0.45, anchor="center", width=450, height=280)
        
        tk.Label(card, text="Настройки", bg="#ffffff", fg="#1a2a3a", font=("Helvetica", 24, "normal")).pack(pady=25)
        row = tk.Frame(card, bg="#f5f5f5", bd=1, relief="solid")
        row.pack(padx=40, fill="x")
        
        tk.Button(row, text="Изменить цвет подсветки", border=0, bg="#f5f5f5", fg="#1a2a3a", font=("Helvetica", 12), cursor="hand2", command=lambda: self.change_color(colors)).pack(side="left", padx=20, pady=15)
        self.preview = tk.Canvas(row, width=25, height=25, bg="#f5f5f5", highlightthickness=0)
        self.preview.pack(side="right", padx=20)
        self.preview.create_oval(2, 2, 23, 23, fill=self.highlight, outline=self.highlight)
        tk.Button(card, text="Главное меню", bg="#1a2a3a", fg="white", relief="flat", font=("Helvetica", 14), width=25, height=2, cursor="hand2", command=self.main_menu).pack(pady=20)
    
    def set_color(self, color):
        self.highlight = color
        self.settings()
    
    def change_color(self, colors):
        self.highlight = colors[(colors.index(self.highlight) + 1) % len(colors)] if self.highlight in colors else colors[0]
        self.preview.delete("all")
        self.preview.create_oval(2, 2, 23, 23, fill=self.highlight, outline=self.highlight)

    def setup(self):
        self.clear()
        self.root.configure(bg="#fafafa")
        bg_frame = tk.Frame(self.root, bg='#1a2a3a')
        bg_frame.pack(fill="both", expand=True)
        
        tk.Label(bg_frame, text="ВЫБОР ПРОТИВНИКА", font=("Helvetica", 18, "bold"), bg='#1a2a3a', fg='white').pack(pady=40)
        self.opponent_var = tk.StringVar(value='human')
        self.first_var = tk.StringVar(value='X')
        
        for text, val in [("👤 Против человека", 'human'), ("🤖 Против компьютера", 'computer')]:
            tk.Radiobutton(bg_frame, text=text, value=val, variable=self.opponent_var, bg='#1a2a3a', fg='white', selectcolor='#1a2a3a', activebackground='#1a2a3a', activeforeground='white', font=("Helvetica", 13), cursor="hand2").pack(pady=8)
        
        tk.Label(bg_frame, text="ПЕРВЫЙ ХОД", font=("Helvetica", 16, "bold"), bg='#1a2a3a', fg='white').pack(pady=20)
        for text, val in [("❌ Крестики (X)", 'X'), ("⭕ Нолики (O)", 'O')]:
            tk.Radiobutton(bg_frame, text=text, value=val, variable=self.first_var, bg='#1a2a3a', fg='white', selectcolor='#1a2a3a', activebackground='#1a2a3a', activeforeground='white', font=("Helvetica", 12), cursor="hand2").pack(pady=5)
        
        tk.Button(bg_frame, text="▶ СТАРТ", command=self.start_game, font=("Helvetica", 14, "bold"), bg="#1a5490", fg='white', relief='flat', cursor='hand2', width=15, height=1).pack(pady=30)
        
    def start_game(self):
        self.clear()
        self.root.configure(bg="#fafafa")
        self.board = [[None]*7 for _ in range(7)]
        self.buttons = []
        self.winner = None
        self.win_line = []
        self.opponent = self.opponent_var.get()
        self.current = Player.X if self.first_var.get() == 'X' else Player.O
        
        top_frame = tk.Frame(self.root, bg='#ffffff')
        top_frame.pack(fill="x", padx=20, pady=(20, 10))
        frame = tk.Frame(self.root, bg='#1a2a3a')
        frame.pack(pady=20)
        
        for i in range(7):
            row = []
            for j in range(7):
                btn = tk.Button(frame, text="", font=("Helvetica", 18, "bold"), width=3, height=1, bg='#ffffff', relief="flat", cursor="hand2", command=lambda r=i, c=j: self.move(r,c))
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
        
        self.score_label = tk.Label(top_frame, text=f"Счет: X {self.x_score} - {self.o_score} O", font=("Helvetica", 16, "bold"), bg='#ffffff', fg='#1a2a3a')
        self.score_label.pack(pady=10)
        self.turn_label = tk.Label(top_frame, text="", font=("Helvetica", 13), bg='#ffffff', fg='#1a5490')
        self.turn_label.pack()
        self.update_turn()
        
        if self.opponent == 'computer' and self.current == Player.O:
            self.root.after(300, self.computer_move)
    
    def update_turn(self):
        self.turn_label.config(text=f"Ход: {'❌ X' if self.current == Player.X else '⭕ O'}", fg='#1a5490' if self.current == Player.X else '#2ecc71')
    
    def move(self, row, col):
        if self.winner or self.board[row][col]:
            return
        
        self.board[row][col] = self.current
        symbol = 'X' if self.current == Player.X else 'O'
        color = '#1a5490' if self.current == Player.X else '#2ecc71'
        self.buttons[row][col].config(text=symbol, fg=color, font=("Helvetica", 18, "bold"))
        
        if self.check_win():
            self.winner = self.current
            if self.winner == Player.X:
                self.x_score += 1
            else:
                self.o_score += 1
            self.highlight_win()
            self.ends()
            return
        
        if all(self.board[i][j] for i in range(7) for j in range(7)):
            self.ends()
            return
        
        self.current = Player.O if self.current == Player.X else Player.X
        self.update_turn()
        
        if self.opponent == 'computer' and self.current == Player.O and not self.winner:
            self.root.after(300, self.computer_move)
    
    def computer_move(self):
        if self.winner:
            return
        
        move = self.get_best_move()
        if move:
            row, col = move
            self.board[row][col] = Player.O
            self.buttons[row][col].config(text='O', fg='#2ecc71', font=("Helvetica", 18, "bold"))
            
            if self.check_win():
                self.winner = Player.O
                self.o_score += 1
                self.highlight_win()
                self.ends()
                return
            
            if all(self.board[i][j] for i in range(7) for j in range(7)):
                self.ends()
                return
            
            self.current = Player.X
            self.update_turn()
    
    def get_best_move(self):
        empty_cells = [(i, j) for i in range(7) for j in range(7) if not self.board[i][j]]
        if not empty_cells:
            return None
        
        for i, j in empty_cells:
            self.board[i][j] = Player.O
            if self.check_win():
                self.board[i][j] = None
                return (i, j)
            self.board[i][j] = None
        
        for i, j in empty_cells:
            self.board[i][j] = Player.X
            if self.check_win():
                self.board[i][j] = None
                return (i, j)
            self.board[i][j] = None
        
        scored_moves = []
        for i, j in empty_cells:
            score = self.evaluate_position_for_move(i, j)
            scored_moves.append((score, i, j))
        
        scored_moves.sort(reverse=True)
        best_moves = scored_moves[:8]
        
        best_score, best_move = -float('inf'), None
        for _, i, j in best_moves:
            self.board[i][j] = Player.O
            score = self.minimax(self.board, 0, False, -float('inf'), float('inf'), 3)
            self.board[i][j] = None
            if score > best_score:
                best_score, best_move = score, (i, j)
                if best_score >= 50:
                    break
        
        return best_move if best_move else best_moves[0][1:]
    
    def evaluate_position_for_move(self, row, col):
        score = 0
        center = 3
        distance = abs(row - center) + abs(col - center)
        score += (6 - distance) * 4
        
        if (row in [0,6] and col in [0,6]):
            score += 8
        elif row in [0,6] or col in [0,6]:
            score += 3
        
        for dr, dc in [(0,1), (1,0), (1,1), (1,-1)]:
            count = 1
            for k in range(1, 4):
                r, c = row + dr*k, col + dc*k
                if 0 <= r < 7 and 0 <= c < 7 and self.board[r][c] == Player.O:
                    count += 1
                else:
                    break
            for k in range(1, 4):
                r, c = row - dr*k, col - dc*k
                if 0 <= r < 7 and 0 <= c < 7 and self.board[r][c] == Player.O:
                    count += 1
                else:
                    break
            if count >= 3:
                score += count * 15
        
        return score
    
    def minimax(self, board, depth, is_max, alpha, beta, max_depth=3):
        winner = self.strokeprocessing(board)
        if winner == Player.O:
            return 100 - depth
        if winner == Player.X:
            return -100 + depth
        
        if depth >= max_depth:
            return self.evaluate_board(board)
        
        empty = [(i, j) for i in range(7) for j in range(7) if not board[i][j]]
        if not empty:
            return 0
        
        if is_max:
            best = -float('inf')
            for i, j in empty[:12]:
                board[i][j] = Player.O
                best = max(best, self.minimax(board, depth+1, False, alpha, beta, max_depth))
                board[i][j] = None
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = float('inf')
            for i, j in empty[:12]:
                board[i][j] = Player.X
                best = min(best, self.minimax(board, depth+1, True, alpha, beta, max_depth))
                board[i][j] = None
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best
    
    def evaluate_board(self, board):
        score = 0
        
        for i in range(7):
            for j in range(4):
                o_count = sum(1 for k in range(4) if board[i][j+k] == Player.O)
                x_count = sum(1 for k in range(4) if board[i][j+k] == Player.X)
                if o_count == 4:
                    score += 100
                elif x_count == 4:
                    score -= 100
                elif o_count == 3 and x_count == 0:
                    score += 15
                elif x_count == 3 and o_count == 0:
                    score -= 15
                elif o_count == 2 and x_count == 0:
                    score += 3
                elif x_count == 2 and o_count == 0:
                    score -= 3
        
        for j in range(7):
            for i in range(4):
                o_count = sum(1 for k in range(4) if board[i+k][j] == Player.O)
                x_count = sum(1 for k in range(4) if board[i+k][j] == Player.X)
                if o_count == 4:
                    score += 100
                elif x_count == 4:
                    score -= 100
                elif o_count == 3 and x_count == 0:
                    score += 15
                elif x_count == 3 and o_count == 0:
                    score -= 15
                elif o_count == 2 and x_count == 0:
                    score += 3
                elif x_count == 2 and o_count == 0:
                    score -= 3
        
        for i in range(4):
            for j in range(4):
                o_count = sum(1 for k in range(4) if board[i+k][j+k] == Player.O)
                x_count = sum(1 for k in range(4) if board[i+k][j+k] == Player.X)
                if o_count == 4:
                    score += 100
                elif x_count == 4:
                    score -= 100
                elif o_count == 3 and x_count == 0:
                    score += 15
                elif x_count == 3 and o_count == 0:
                    score -= 15
                elif o_count == 2 and x_count == 0:
                    score += 3
                elif x_count == 2 and o_count == 0:
                    score -= 3
        
        for i in range(4):
            for j in range(3, 7):
                o_count = sum(1 for k in range(4) if board[i+k][j-k] == Player.O)
                x_count = sum(1 for k in range(4) if board[i+k][j-k] == Player.X)
                if o_count == 4:
                    score += 100
                elif x_count == 4:
                    score -= 100
                elif o_count == 3 and x_count == 0:
                    score += 15
                elif x_count == 3 and o_count == 0:
                    score -= 15
                elif o_count == 2 and x_count == 0:
                    score += 3
                elif x_count == 2 and o_count == 0:
                    score -= 3
        
        center = 3
        if board[center][center] == Player.O:
            score += 5
        elif board[center][center] == Player.X:
            score -= 5
        
        return score
    
    def check_win(self):
        return self.strokeprocessing(self.board)
    
    def strokeprocessing(self, board):
        for i in range(7):
            for j in range(4):
                if board[i][j] and all(board[i][j+k] == board[i][j] for k in range(4)):
                    self.win_line = [(i, j+k) for k in range(4)]
                    return board[i][j]
        for j in range(7):
            for i in range(4):
                if board[i][j] and all(board[i+k][j] == board[i][j] for k in range(4)):
                    self.win_line = [(i+k, j) for k in range(4)]
                    return board[i][j]
        for i in range(4):
            for j in range(4):
                if board[i][j] and all(board[i+k][j+k] == board[i][j] for k in range(4)):
                    self.win_line = [(i+k, j+k) for k in range(4)]
                    return board[i][j]
        for i in range(4):
            for j in range(3, 7):
                if board[i][j] and all(board[i+k][j-k] == board[i][j] for k in range(4)):
                    self.win_line = [(i+k, j-k) for k in range(4)]
                    return board[i][j]
        return None
    
    def highlight_win(self):
        for r, c in self.win_line:
            self.buttons[r][c].config(bg=self.highlight)
    
    def ends(self):
        msg = f"Победили {'❌ X' if self.winner == Player.X else '⭕ O'}!" if self.winner else "Ничья!"
        self.score_label.config(text=f"Счет: X {self.x_score} - {self.o_score} O")
        
        win = tk.Toplevel(self.root)
        win.geometry("500x300")
        win.configure(bg="#fafafa")
        win.resizable(False, False)
        card = tk.Frame(win, bg="#ffffff")
        card.place(relx=0.5, rely=0.5, anchor="center", width=470, height=260)
        
        tk.Label(card, text=msg, bg="#ffffff", fg="#1a2a3a", font=("Helvetica", 24, "bold")).pack(pady=40)
        tk.Button(card, text="Играть заново", bg="#1a2a3a", fg="white", relief="flat", font=("Helvetica", 14), width=22, height=2, cursor="hand2", command=lambda:[win.destroy(), self.start_game()]).pack(pady=5)
        tk.Button(card, text="Главное меню", bg="#ffffff", fg="#1a2a3a", relief="solid", bd=1, font=("Helvetica", 14), width=22, height=2, cursor="hand2", command=lambda:[win.destroy(), self.main_menu()]).pack(pady=5)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToe7x7()
    game.run()