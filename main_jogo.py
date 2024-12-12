import random
import tkinter as tk
from tkinter import messagebox

def show_tutorial():
    tutorial = """
┌────────────── TUTORIAL DO GENERAL ──────────────┐
│                                                 │
│  Como pontuar:                                  │
│                                                 │
│  ▶ Trinca: 3+ dados iguais                     │
│    Pontuação = soma de todos os dados           │
│                                                 │
│  ▶ Quadra: 4+ dados iguais                     │
│    Pontuação = soma de todos os dados           │
│                                                 │
│  ▶ Full House: Um par + uma trinca             │
│    Pontuação fixa = 25 pontos                   │
│                                                 │
│  ▶ Sequência Baixa: 4 números consecutivos     │
│    Pontuação fixa = 30 pontos                   │
│                                                 │
│  ▶ Sequência Alta: 5 números consecutivos      │
│    Pontuação fixa = 40 pontos                   │
│                                                 │
│  ▶ General: Todos os 5 dados iguais            │
│    Pontuação fixa = 50 pontos                   │
│                                                 │
│  ▶ Chance: Soma de todos os dados              │
│    Sem restrições                               │
│                                                 │
│             Boa sorte! 🎲                      │
└─────────────────────────────────────────────────┘
"""
    messagebox.showinfo("Tutorial", tutorial)

class GeneralGame:
    def __init__(self, root):
        self.root = root
        self.scores = {}
        self.categories = [
            "Trinca", "Quadra", "Full House", "Sequência Baixa", 
            "Sequência Alta", "General", "Chance"
        ]
        self.reset_scores()
        self.current_dice = []
        self.selected_dice = []
        self.dice_buttons = []
        self.category_buttons = {}  # Novo dicionário para armazenar os botões das categorias
        self.current_round = 0
        self.setup_ui()

    def setup_ui(self):
        # Configurar a interface do usuário
        self.display_scores_label = tk.Label(self.root, text="", font=('Courier', 10), justify=tk.CENTER)
        self.display_scores_label.pack(pady=10)
        
        # Frame para os dados
        self.dice_frame = tk.Frame(self.root)
        self.dice_frame.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(self.root, text="", font=('Arial', 10))
        self.status_label.pack(pady=5)

        # Frame para os botões de controle
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)
        
        self.roll_button = tk.Button(button_frame, text="Lançar Dados", width=15, command=self.roll_dice_action)
        self.roll_button.pack(side=tk.LEFT, padx=5)

        # Frame para as categorias de pontuação
        score_frame = tk.Frame(self.root)
        score_frame.pack(pady=10)
        
        # Criar botões para cada categoria
        for category in self.categories:
            btn = tk.Button(score_frame, text=category, width=15,
                          command=lambda cat=category: self.score_category(cat))
            btn.pack(pady=2)
            self.category_buttons[category] = btn  # Armazenar referência ao botão
        
        self.tutorial_button = tk.Button(self.root, text="Tutorial", width=15, command=show_tutorial)
        self.tutorial_button.pack(pady=5)

    def reset_scores(self):
        self.scores = {category: None for category in self.categories}

    def roll_dice(self, keep=[]):
        dice = [random.randint(1, 6) for _ in range(5 - len(keep))]
        return keep + dice

    def display_scores(self):
        score_display = "\n┌─────────── PLACAR ───────────┐\n"
        for category, score in self.scores.items():
            status = str(score) if score is not None else "□"
            score_display += f"│ {category:<15} │ {status:>5} │\n"
        score_display += "└───────────────────────────────┘"
        self.display_scores_label['text'] = score_display

    def create_dice_buttons(self):
        # Limpar dados anteriores
        for button in self.dice_buttons:
            button.destroy()
        self.dice_buttons = []
        
        # Criar novos botões para cada dado
        for i, value in enumerate(self.current_dice):
            btn = tk.Button(self.dice_frame, text=str(value), width=3, height=1,
                          command=lambda x=i: self.toggle_dice(x))
            btn.pack(side=tk.LEFT, padx=5)
            # Se o dado já estava selecionado, manter a cor
            if i < len(self.selected_dice) and self.selected_dice[i]:
                btn.configure(bg='lightblue')
            self.dice_buttons.append(btn)

    def toggle_dice(self, index):
        # Alternar a seleção do dado
        if index >= len(self.selected_dice):
            self.selected_dice.extend([False] * (index - len(self.selected_dice) + 1))
        
        self.selected_dice[index] = not self.selected_dice[index]
        
        # Atualizar a cor do botão
        if self.selected_dice[index]:
            self.dice_buttons[index].configure(bg='lightblue')
        else:
            self.dice_buttons[index].configure(bg='SystemButtonFace')

    def roll_dice_action(self):
        if self.current_round < 3:
            # Manter apenas os dados selecionados
            keep = [d for i, d in enumerate(self.current_dice) if i < len(self.selected_dice) and self.selected_dice[i]]
            self.current_dice = self.roll_dice(keep)
            self.selected_dice = [False] * len(self.current_dice)
            self.create_dice_buttons()
            
            self.current_round += 1
            remaining = 3 - self.current_round
            
            if remaining > 0:
                self.status_label['text'] = f"Rodada {self.current_round}/3 - Você tem mais {remaining} {'jogada' if remaining == 1 else 'jogadas'}"
            else:
                self.status_label['text'] = "Última rodada! Escolha uma categoria para pontuar"
                self.roll_button.configure(state='disabled')

    def score_category(self, category):
        if self.current_dice and self.scores[category] is None:
            score = self.calculate_score(self.current_dice, category)
            self.scores[category] = score
            messagebox.showinfo("Pontuação", f"Você marcou {score} pontos em {category}!")
            self.display_scores()
            
            # Desabilitar o botão da categoria pontuada
            self.category_buttons[category].configure(state='disabled')
            
            self.reset_round()
            
            # Verificar se todas as categorias foram preenchidas
            if all(score is not None for score in self.scores.values()):
                total = sum(score for score in self.scores.values())
                messagebox.showinfo("Fim do Jogo", f"Jogo terminado! Pontuação total: {total}")
                self.root.destroy()

    def reset_round(self):
        self.current_round = 0
        self.current_dice = []
        self.selected_dice = []
        for button in self.dice_buttons:
            button.destroy()
        self.dice_buttons = []
        self.roll_button.configure(state='normal')
        self.status_label['text'] = "Clique em 'Lançar Dados' para começar nova rodada"

    def calculate_score(self, dice, category):
        if category == "Trinca":
            for i in range(1, 7):
                if dice.count(i) >= 3:
                    return sum(dice)
            return 0
        elif category == "Quadra":
            for i in range(1, 7):
                if dice.count(i) >= 4:
                    return sum(dice)
            return 0
        elif category == "Full House":
            counts = [dice.count(i) for i in range(1, 7)]
            if 2 in counts and 3 in counts:
                return 25
            return 0
        elif category == "Sequência Baixa":
            sorted_dice = sorted(list(set(dice)))
            sequences = [{1,2,3,4}, {2,3,4,5}, {3,4,5,6}]
            if any(set(sorted_dice).issuperset(seq) for seq in sequences):
                return 30
            return 0
        elif category == "Sequência Alta":
            sorted_dice = sorted(list(set(dice)))
            if sorted_dice in [[1,2,3,4,5], [2,3,4,5,6]]:
                return 40
            return 0
        elif category == "General":
            if len(set(dice)) == 1:
                return 50
            return 0
        elif category == "Chance":
            return sum(dice)
        return 0

    def play_game(self):
        self.display_scores_label['text'] = "\n" + "═" * 40 + "\n      BEM-VINDO AO GENERAL!" + "\n" + "═" * 40
        self.display_scores()
        self.status_label['text'] = "Clique em 'Lançar Dados' para começar!"

root = tk.Tk()
game = GeneralGame(root)
game.play_game()
root.mainloop()
