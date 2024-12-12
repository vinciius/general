import tkinter as tk
from main_jogo import GeneralGame, show_tutorial

# Função para iniciar o jogo
def play_game():
    # Criar uma nova janela para o jogo
    game_window = tk.Toplevel(root)
    game_window.title('General - Jogo em Andamento')
    game = GeneralGame(game_window)
    game.play_game()

# Função para mostrar o tutorial
def show_tutorial_window():
    show_tutorial()

# Função para sair do jogo
def exit_game():
    root.destroy()

# Criar a janela principal
root = tk.Tk()
root.title('Jogo de General')

# Criar um rótulo para o título do jogo
label = tk.Label(root, font=('Helvetica', 24), text="Jogo de General")
label.pack(pady=20)

# Criar um frame para os botões
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# Criar botões
play_button = tk.Button(button_frame, text="Jogar", command=play_game)
play_button.pack(side=tk.LEFT, padx=10)

tutorial_button = tk.Button(button_frame, text="Tutorial de Pontuação", command=show_tutorial_window)
tutorial_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(button_frame, text="Sair", command=exit_game)
exit_button.pack(side=tk.LEFT, padx=10)

# Iniciar o loop da interface gráfica
root.mainloop()
