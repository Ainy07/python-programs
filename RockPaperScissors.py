import tkinter as tk
from tkinter import messagebox
import random
import json
import os

USER_FILE = "users.json"

if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

choices = {
    "Rock": "🪨",
    "Paper": "📄",
    "Scissors": "✂️"
}

current_user = None
user_score = 0
computer_score = 0

# ------------------ GAME FUNCTIONS ------------------ #
def play(user_choice):
    global user_score, computer_score
    comp_choice = random.choice(list(choices.keys()))
    
    user_emoji = choices[user_choice]
    comp_emoji = choices[comp_choice]

    if user_choice == comp_choice:
        result_text = "🤝 It's a Tie!"
        color = "#FFA500"  
    elif (
        (user_choice == "Rock" and comp_choice == "Scissors") or
        (user_choice == "Paper" and comp_choice == "Rock") or
        (user_choice == "Scissors" and comp_choice == "Paper")
    ):
        result_text = "🎉 You Win!"
        user_score += 1
        color = "#28a745"  
    else:
        result_text = "💀 Computer Wins!"
        computer_score += 1
        color = "#FF4500"  

    animate_result(f"{current_user} : {user_choice} {user_emoji}  |  Computer: {comp_choice} {comp_emoji}\n{result_text}", color)
    score_label.config(text=f"Score -> {current_user}: {user_score} | Computer: {computer_score}")
    save_user_data()
    update_leaderboard()

def animate_result(text, color):
    flashes = [color, "#000000"]
    for i in range(3):
        result_label.config(text=text, fg=flashes[i%2])
        result_label.update()
        result_label.after(150)
    result_label.config(text=text, fg=color)

def reset_game():
    global user_score, computer_score
    user_score = 0
    computer_score = 0
    score_label.config(text=f"Score -> {current_user}: 0 | Computer: 0")
    result_label.config(text="Make your move!", fg="#007FFF")
    save_user_data()
    update_leaderboard()

def save_user_data():
    users[current_user]["score"] = user_score
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ------------------ LOGIN & REGISTER ------------------ #
def register_user():
    username = reg_username_entry.get().strip()
    password = reg_password_entry.get().strip()
    email = reg_email_entry.get().strip()

    if username == "" or password == "" or email == "":
        messagebox.showwarning("Warning", "All fields are required!")
        return
    if username in users:
        messagebox.showerror("Error", "Username already exists!")
        return

    users[username] = {"password": password, "email": email, "score": 0}
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)
    messagebox.showinfo("Success", f"User '{username}' registered!")
    reg_username_entry.delete(0, tk.END)
    reg_password_entry.delete(0, tk.END)
    reg_email_entry.delete(0, tk.END)
    show_login_frame()

def login_user():
    global current_user, user_score, computer_score
    username = login_username_entry.get().strip()
    password = login_password_entry.get().strip()
    if username in users and users[username]["password"] == password:
        current_user = username
        user_score = users[username]["score"]
        computer_score = 0
        login_frame.pack_forget()
        game_frame.pack(fill="both", expand=True)
        user_label.config(text=f"Player: {current_user}")
        score_label.config(text=f"Score -> {current_user}: {user_score} | Computer: {computer_score}")
        update_leaderboard()
    else:
        messagebox.showerror("Error", "Incorrect username or password!")

def logout_user():
    global current_user, user_score, computer_score
    current_user = None
    user_score = 0
    computer_score = 0
    game_frame.pack_forget()
    show_login_frame()

# ------------------ FRAME SWITCH ------------------ #
def show_register_frame():
    login_frame.pack_forget()
    register_frame.pack(fill="both", expand=True)

def show_login_frame():
    register_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

# ------------------ BUTTON PULSE ------------------ #
def pulse_button(button, colors, step=0):
    button.config(fg=colors[step % len(colors)])
    button.after(100, pulse_button, button, colors, step+1)

# ------------------ LEADERBOARD ------------------ #
def update_leaderboard():
    leaderboard_text = "Leaderboard:\n"
    sorted_users = sorted(users.items(), key=lambda x: x[1]["score"], reverse=True)
    for u, data in sorted_users:
        leaderboard_text += f"{u}: {data['score']}\n"
    leaderboard_label.config(text=leaderboard_text)

# ------------------ MAIN WINDOW ------------------ #
root = tk.Tk()
root.title("🎮 Arcade Rock Paper Scissors with Login/Register")
root.geometry("600x650")
root.resizable(False, False)
root.configure(bg="#f0f8ff") 

# ------------------ REGISTER FRAME ------------------ #
register_frame = tk.Frame(root, bg="#f0f8ff")
tk.Label(register_frame, text="🎮 Register", font=("Comic Sans MS", 24, "bold"), bg="#f0f8ff", fg="#007FFF").pack(pady=20)
tk.Label(register_frame, text="Username:", font=("Arial", 14), bg="#f0f8ff", fg="#007FFF").pack(pady=5)
reg_username_entry = tk.Entry(register_frame, font=("Arial", 14), width=25)
reg_username_entry.pack(pady=5)
tk.Label(register_frame, text="Password:", font=("Arial", 14), bg="#f0f8ff", fg="#007FFF").pack(pady=5)
reg_password_entry = tk.Entry(register_frame, font=("Arial", 14), width=25, show="*")
reg_password_entry.pack(pady=5)
tk.Label(register_frame, text="Email:", font=("Arial", 14), bg="#f0f8ff", fg="#007FFF").pack(pady=5)
reg_email_entry = tk.Entry(register_frame, font=("Arial", 14), width=25)
reg_email_entry.pack(pady=5)
reg_btn = tk.Button(register_frame, text="Register", font=("Arial", 14, "bold"), bg="#28a745", fg="#ffffff", width=15, command=register_user)
reg_btn.pack(pady=20)
pulse_button(reg_btn, ["#28a745","#32CD32","#7CFC00","#ADFF2F"])
tk.Button(register_frame, text="Already have account? Login", font=("Arial", 12), bg="#f0f8ff", fg="#007FFF", bd=0, command=show_login_frame).pack(pady=10)

# ------------------ LOGIN FRAME ------------------ #
login_frame = tk.Frame(root, bg="#f0f8ff")
tk.Label(login_frame, text="🎮 Login", font=("Comic Sans MS", 24, "bold"), bg="#f0f8ff", fg="#007FFF").pack(pady=20)
tk.Label(login_frame, text="Username:", font=("Arial", 14), bg="#f0f8ff", fg="#007FFF").pack(pady=5)
login_username_entry = tk.Entry(login_frame, font=("Arial", 14), width=25)
login_username_entry.pack(pady=5)
tk.Label(login_frame, text="Password:", font=("Arial", 14), bg="#f0f8ff", fg="#007FFF").pack(pady=5)
login_password_entry = tk.Entry(login_frame, font=("Arial", 14), width=25, show="*")
login_password_entry.pack(pady=5)
login_btn = tk.Button(login_frame, text="Login", font=("Arial", 14, "bold"), bg="#007FFF", fg="#ffffff", width=15, command=login_user)
login_btn.pack(pady=20)
pulse_button(login_btn, ["#007FFF","#339FFF","#66B2FF","#99CCFF"])
tk.Button(login_frame, text="Don't have account? Register", font=("Arial", 12), bg="#f0f8ff", fg="#007FFF", bd=0, command=show_register_frame).pack(pady=10)

# ------------------ GAME FRAME ------------------ #
game_frame = tk.Frame(root, bg="#f0f8ff")
user_label = tk.Label(game_frame, text="", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="#007FFF")
user_label.pack(pady=5)
score_label = tk.Label(game_frame, text="", font=("Arial", 14, "bold"), bg="#f0f8ff", fg="#007FFF")
score_label.pack(pady=5)
result_label = tk.Label(game_frame, text="Make your move!", font=("Arial", 14, "bold"), width=45, height=5, bg="#e0ffff", fg="#007FFF", bd=4, relief="ridge")
result_label.pack(pady=20)

button_frame = tk.Frame(game_frame, bg="#f0f8ff")
button_frame.pack(pady=10)
button_colors = {"Rock": ["#FF007F","#FF3399","#FF66AA","#FF99BB"],
                 "Paper": ["#00FFFF","#33FFFF","#66FFFF","#99FFFF"],
                 "Scissors": ["#FFD700","#FFEB3B","#FFF176","#FFEE58"]}
buttons = {}
for choice in choices.keys():
    btn = tk.Button(button_frame, text=f"{choices[choice]} {choice}", font=("Arial", 14, "bold"),
                    width=12, height=2, bg="#f0f8ff", fg=button_colors[choice][0],
                    bd=4, relief="raised", command=lambda c=choice: play(c))
    btn.pack(side="left", padx=15)
    pulse_button(btn, button_colors[choice])
    buttons[choice] = btn

reset_btn = tk.Button(game_frame, text="🔄 Reset Game", font=("Arial", 14, "bold"), width=18, height=2, bg="#007FFF", fg="#ffffff", bd=4, relief="raised", command=reset_game)
reset_btn.pack(pady=15)
pulse_button(reset_btn, ["#007FFF","#339FFF","#66B2FF","#99CCFF"])

logout_btn = tk.Button(game_frame, text="🚪 Logout", font=("Arial", 14, "bold"), width=18, height=2, bg="#FF4500", fg="#ffffff", bd=4, relief="raised", command=logout_user)
logout_btn.pack(pady=10)
pulse_button(logout_btn, ["#FF4500","#FF6347","#FF7F50","#FF8C69"])

# Leaderboard
leaderboard_label = tk.Label(game_frame, text="Leaderboard:", font=("Arial", 12, "bold"), bg="#f0f8ff", fg="#007FFF", justify="left")
leaderboard_label.pack(pady=10)

# Show login frame initially
login_frame.pack(fill="both", expand=True)

root.mainloop()