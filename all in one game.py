import tkinter as tk
import random

# ------------------- SPLASH SCREEN -------------------

def show_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg="darkseagreen")
    splash.geometry("1380x700")

    tk.Label(splash, text="----MULTIPGAME----", bg="darkseagreen", fg="ivory",
             font=("Helvetica",50, "bold")).pack(expand=True)

    splash.after(1500, lambda: [splash.destroy(), open_main_menu()])
    splash.mainloop()

# ------------------- MAIN MENU -------------------

def open_main_menu():
    root = tk.Tk()
    root.title("Game Hub")
    root.geometry("1380x700")
    root.configure(bg='rosybrown')
    tk.Label(root, text="-----CHOOSE A GAME-----",bg='rosybrown',fg='white', font=("Helvetica",35)).pack(pady=70)

    tk.Button(root, text="🐍 Snake Game",bg='darkseagreen',fg='ivory',font=('helvetica',20),command=snake_game).pack(pady=10)
    tk.Button(root, text="🧠 Memory Match",bg='darkseagreen',fg='ivory',font=('helvetica',20), command=memory_game).pack(pady=10)
    tk.Button(root, text="✊🖐✌ Stone Paper Scissors",bg='darkseagreen',fg='ivory',font=('helvetica',20), command=sps_game).pack(pady=10)
    tk.Button(root, text="⭕ Tic Tac Toe",bg='darkseagreen',fg='ivory',font=('helvetica',20), command=tictactoe_game).pack(pady=10)
    tk.Button(root, text="🎯 Whack-a-Mole",bg='darkseagreen',fg='ivory',font=('helvetica',20),command=whack_a_mole).pack(pady=10)
    tk.Button(root, text="⏱️ Reaction Time Game",bg='darkseagreen',fg='ivory',font=('helvetica',20), command=reaction_time_game).pack(pady=10)
#-------------------reaction time game---------------------
import time  
def reaction_time_game():
    rt = tk.Toplevel()
    rt.title("Reaction Time Game")
    rt.geometry("400x300")
    rt.configure(bg="red")

    instructions = tk.Label(rt, text="Wait for green...", bg="red", fg="white", font=("Arial", 18))
    instructions.pack(expand=True)

    start_time = [0]
    clicked = [False]

    def turn_green():
        rt.configure(bg="green")
        instructions.config(text="CLICK NOW!", bg="green")
        start_time[0] = time.time()

    def on_click(event):
        if rt["bg"] == "green" and not clicked[0]:
            reaction = int((time.time() - start_time[0]) * 1000)
            instructions.config(text=f"Reaction Time: {reaction} ms", bg="blue")
            clicked[0] = True
        elif rt["bg"] == "red":
            instructions.config(text="Too Early! Wait for green!", bg="red")

    rt.bind("<Button-1>", on_click)
    rt.after(random.randint(2000, 5000), turn_green)

    root.mainloop()

# ------------------- SNAKE GAME -------------------

def snake_game():
    game = tk.Toplevel()
    game.title("Snake Game")
    canvas = tk.Canvas(game, bg="black", width=400, height=300)
    canvas.pack()

    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "Right"
    food = [random.randint(0, 19)*20, random.randint(0, 14)*20]
    running = True

    def move():
        nonlocal direction, running
        if not running:
            canvas.create_text(200, 150, text="Game Over", fill="white", font=("Arial", 20))
            return

        x, y = snake[0]
        if direction == "Up": y -= 20
        elif direction == "Down": y += 20
        elif direction == "Left": x -= 20
        elif direction == "Right": x += 20

        head = (x, y)
        if head in snake or x < 0 or y < 0 or x >= 400 or y >= 300:
            running = False
        else:
            snake.insert(0, head)
            if head == tuple(food):
                food[0], food[1] = random.randint(0, 19)*20, random.randint(0, 14)*20
            else:
                snake.pop()

            canvas.delete("all")
            for seg in snake:
                canvas.create_rectangle(*seg, seg[0]+20, seg[1]+20, fill="lime")
            canvas.create_oval(*food, food[0]+20, food[1]+20, fill="red")
            game.after(100, move)

    def change_dir(event):
        nonlocal direction
        if event.keysym in {"Up", "Down", "Left", "Right"}:
            direction = event.keysym

    game.bind("<KeyPress>", change_dir)
    move()

# ------------------- MEMORY GAME -------------------

def memory_game():
    mem = tk.Toplevel()
    mem.title("Memory Match")
    mem.geometry("1390x700")

    symbols = list("AABBCCDDEEFFGGHH")
    random.shuffle(symbols)

    buttons = []
    revealed = []
    matched = []

    def click(i):
        if i in revealed or i in matched:
            return
        buttons[i].config(text=symbols[i])
        revealed.append(i)
        if len(revealed) == 2:
            mem.after(500, check)

    def check():
        nonlocal revealed
        i1, i2 = revealed
        if symbols[i1] == symbols[i2]:
            matched.extend([i1, i2])
        else:
            buttons[i1].config(text="❓")
            buttons[i2].config(text="❓")
        revealed = []

    for i in range(16):
        b = tk.Button(mem, text="❓", width=20, height=10, command=lambda i=i: click(i))
        b.grid(row=i // 4, column=i % 4)
        buttons.append(b)

# ------------------- STONE PAPER SCISSORS -------------------

def sps_game():
    sps = tk.Toplevel()
    sps.title("Stone Paper Scissors")

    choices = ["Stone", "Paper", "Scissors"]

    result = tk.StringVar()
    result.set("Make your choice!")

    def play(player_choice):
        comp_choice = random.choice(choices)
        if player_choice == comp_choice:
            res = f"Draw! Both chose {player_choice}"
        elif (player_choice == "Stone" and comp_choice == "Scissors") or \
             (player_choice == "Paper" and comp_choice == "Stone") or \
             (player_choice == "Scissors" and comp_choice == "Paper"):
            res = f"You Win! {player_choice} beats {comp_choice}"
        else:
            res = f"You Lose! {comp_choice} beats {player_choice}"
        result.set(res)

    tk.Label(sps, textvariable=result, font=("Arial", 14)).pack(pady=20)

    for choice in choices:
        tk.Button(sps, text=choice, width=15, command=lambda c=choice: play(c)).pack(pady=5)
#---------------------tic tac toe-------------------
def tictactoe_game():
    ttt = tk.Toplevel()
    ttt.title("Tic Tac Toe")

    current = ["X"]
    buttons = []

    def check_winner():
        wins = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for i, j, k in wins:
            if buttons[i]['text'] != "" and \
               buttons[i]['text'] == buttons[j]['text'] == buttons[k]['text']:
                for idx in (i, j, k):
                    buttons[idx].config(bg="lightgreen")
                return True
        return False

    def on_click(i):
        if buttons[i]["text"] == "":
            buttons[i]["text"] = current[0]
            if not check_winner():
                current[0] = "O" if current[0] == "X" else "X"

    for i in range(9):
        b = tk.Button(ttt, text="", width=10, height=4, command=lambda i=i: on_click(i))
        b.grid(row=i // 3, column=i % 3)
        buttons.append(b)
#--------------------whack a mole----------------
def whack_a_mole():
    mole = tk.Toplevel()
    mole.title("Whack-a-Mole")
    mole.geometry("300x300")

    score = [0]
    active_btn = [None]

    score_label = tk.Label(mole, text="Score: 0", font=("Arial", 14))
    score_label.pack()

    frame = tk.Frame(mole)
    frame.pack()

    buttons = []

    def spawn_mole():
        if active_btn[0] is not None:
            buttons[active_btn[0]].config(text="")

        index = random.randint(0, 8)
        buttons[index].config(text="🐹")
        active_btn[0] = index

        mole.after(1000, spawn_mole)

    def hit(index):
        if active_btn[0] == index:
            score[0] += 1
            score_label.config(text=f"Score: {score[0]}")
            buttons[index].config(text="")

    for i in range(9):
        b = tk.Button(frame, text="", width=6, height=3, command=lambda i=i: hit(i))
        b.grid(row=i//3, column=i%3, padx=5, pady=5)
        buttons.append(b)

    spawn_mole()
# ------------------- RUN -------------------

show_splash()
