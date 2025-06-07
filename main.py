import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import pygame

# ---------- Setup Sound System ----------
pygame.mixer.init()
pop_sound = pygame.mixer.Sound("assets/pop.wav")
music_file = "assets/lofi.mp3"

# ---------- Timer Durations ----------
FOCUS_TIME = 25 * 60
BREAK_TIME = 5 * 60

class PomoduckApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomoduck.exe")
        self.root.geometry("500x600")
        self.root.configure(bg="#689fbd")

        self.music_playing = False
        self.time_left = FOCUS_TIME
        self.running = False
        self.on_break = False

        # ---------- Title ----------
        self.title_label = tk.Label(root, text="🪷 p o m o d u c k 🪷", font=("Courier New", 24, "bold"),
                                    bg="#689fbd", fg="#fad877")
        self.title_label.pack(pady=(15, 5))

        # ---------- Timer Display ----------
        self.timer_label = tk.Label(root, text=self.format_time(self.time_left),
                                    font=("Courier New", 64, "bold"), bg="#689fbd", fg="#ffffff")
        self.timer_label.pack(pady=(0, 10))

        # ---------- Button Style ----------
        pill_style = {
            "font": ("Courier New", 12, "bold"),
            "width": 12,
            "height": 2,
            "bg": "#ffd3e0",
            "fg": "#4e342e",
            "activebackground": "#ffc1cc",
            "activeforeground": "#4e342e",
            "bd": 0,
            "highlightthickness": 0,
            "highlightbackground": "#689fbd",
            "relief": "flat",
            "cursor": "hand2"
        }

        # ---------- Timer Buttons ----------
        btn_frame = tk.Frame(root, bg="#689fbd")
        btn_frame.pack(pady=10)

        self.start_button = tk.Button(btn_frame, text="s t a r t", command=self.start_timer, **pill_style)
        self.pause_button = tk.Button(btn_frame, text="p a u s e", command=self.pause_timer, **pill_style)
        self.reset_button = tk.Button(btn_frame, text="r e s e t", command=self.reset_timer, **pill_style)

        self.start_button.grid(row=0, column=0, padx=8, pady=10)
        self.pause_button.grid(row=0, column=1, padx=8, pady=10)
        self.reset_button.grid(row=0, column=2, padx=8, pady=10)

        # ---------- Psyduck GIF ----------
        self.gif_label = tk.Label(root, bg="#689fbd")
        self.gif_label.pack(pady=(30, 10))

        self.gif = Image.open("assets/psyduck.gif")
        self.frames = [ImageTk.PhotoImage(frame.copy().resize((330, 250)))
                       for frame in ImageSequence.Iterator(self.gif)]
        self.frame_index = 0
        self.animate_gif()

        # ---------- Music & To-Do Buttons ----------
        self.sound_button = tk.Button(root, text="🔇 Music Off", command=self.toggle_music, **pill_style)
        self.sound_button.pack(pady=(5, 5))

        self.todo_button = tk.Button(root, text="🧾 t o - d o", command=self.open_todo_window, **pill_style)
        self.todo_button.pack(pady=(0, 10))

    def animate_gif(self):
        frame = self.frames[self.frame_index]
        self.gif_label.config(image=frame)
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.root.after(100, self.animate_gif)

    def format_time(self, seconds):
        minutes = seconds // 60
        sec = seconds % 60
        return f"{minutes:02d}:{sec:02d}"

    def update_timer(self):
        if self.running:
            if self.time_left > 0:
                self.time_left -= 1
                self.timer_label.config(text=self.format_time(self.time_left))
                self.root.after(1000, self.update_timer)
            else:
                self.running = False
                self.on_break = not self.on_break
                self.time_left = BREAK_TIME if self.on_break else FOCUS_TIME
                self.timer_label.config(text=self.format_time(self.time_left))
                messagebox.showinfo("Pomoduck", "Time's up! 🛁")

    def start_timer(self):
        pop_sound.play()
        if not self.running:
            self.running = True
            self.update_timer()

    def pause_timer(self):
        pop_sound.play()
        self.running = False

    def reset_timer(self):
        pop_sound.play()
        self.running = False
        self.time_left = FOCUS_TIME
        self.on_break = False
        self.timer_label.config(text=self.format_time(self.time_left))

    def toggle_music(self):
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False
            self.sound_button.config(text="🔇 Music Off")
        else:
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.play(-1)
                self.music_playing = True
                self.sound_button.config(text="🔊 Music On")
            except Exception as e:
                messagebox.showerror("Error", f"Could not play music:\n{e}")

    def open_todo_window(self):
        if hasattr(self, "todo_window") and self.todo_window.winfo_exists():
            self.todo_window.lift()
            return

        self.todo_window = tk.Toplevel(self.root)
        self.todo_window.title("Pomoduck To-Do")
        self.todo_window.configure(bg="#689fbd")
        self.todo_window.geometry("+50+100")

        # ---------- To-Do Title ----------
        todo_title = tk.Label(self.todo_window, text="📝 t o - d o   l i s t", font=("Courier New", 16, "bold"),
                              bg="#689fbd", fg="#fad877")
        todo_title.pack(pady=8)

        # ---------- Entry Frame (on top now) ----------
        entry_frame = tk.Frame(self.todo_window, bg="#689fbd")
        entry_frame.pack(pady=(0, 10))

        self.task_entry = tk.Entry(entry_frame, font=("Courier New", 12), width=20,
                                   bg="#fff3e6", fg="#4e342e", relief="flat")
        self.task_entry.pack(side="left", padx=(0, 8))

        add_button = tk.Button(entry_frame, text="a d d 🐣", command=self.add_task, **{
            "font": ("Courier New", 12, "bold"),
            "width": 8,
            "height": 1,
            "bg": "#ffd3e0",
            "fg": "#4e342e",
            "activebackground": "#ffc1cc",
            "activeforeground": "#4e342e",
            "bd": 0,
            "highlightthickness": 0,
            "highlightbackground": "#689fbd",
            "relief": "flat",
            "cursor": "hand2"
        })
        add_button.pack(side="left")

        # ---------- Scrollable To-Do Frame ----------
        canvas = tk.Canvas(self.todo_window, bg="#689fbd", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=10)

        scrollbar = tk.Scrollbar(self.todo_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        self.task_list_frame = tk.Frame(canvas, bg="#689fbd")
        canvas.create_window((0, 0), window=self.task_list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.task_list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            var = tk.BooleanVar()

            def on_check():
                pop_sound.play()
                check.destroy()

            check = tk.Checkbutton(self.task_list_frame, text=task_text,
                                   variable=var, command=on_check,
                                   font=("Courier New", 12),
                                   bg="#ffd3e0", fg="#4e342e",
                                   selectcolor="#fff3e6",
                                   activebackground="#ffc1cc",
                                   relief="flat", anchor="w", padx=10)
            check.pack(anchor="w", pady=2, fill="x")
            self.task_entry.delete(0, tk.END)

# ---------- Run App ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = PomoduckApp(root)
    root.mainloop()
