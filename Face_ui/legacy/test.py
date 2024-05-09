import tkinter as tk
from tkinter import Canvas

class EyeController:
    def __init__(self, canvas, eye_size=100):
        self.canvas = canvas
        self.eye_size = eye_size
        self.create_eyes()

    def create_eyes(self):
        self.left_eye = self.canvas.create_oval(50, 50, 50 + self.eye_size, 50 + self.eye_size, fill='black')
        self.right_eye = self.canvas.create_oval(200, 50, 200 + self.eye_size, 50 + self.eye_size, fill='black')

    def express(self, expression):
        if expression == 'happy':
            self.canvas.itemconfig(self.left_eye, fill='green')
            self.canvas.itemconfig(self.right_eye, fill='green')
        elif expression == 'sad':
            self.canvas.itemconfig(self.left_eye, fill='blue')
            self.canvas.itemconfig(self.right_eye, fill='blue')
        elif expression == 'angry':
            self.canvas.itemconfig(self.left_eye, fill='red')
            self.canvas.itemconfig(self.right_eye, fill='red')
        elif expression == 'focused':
            self.canvas.itemconfig(self.left_eye, fill='yellow')
            self.canvas.itemconfig(self.right_eye, fill='yellow')
        elif expression == 'confused':
            self.canvas.itemconfig(self.left_eye, fill='purple')
            self.canvas.itemconfig(self.right_eye, fill='purple')
        else:
            self.canvas.itemconfig(self.left_eye, fill='black')
            self.canvas.itemconfig(self.right_eye, fill='black')

def create_buttons(root, eye_controller):
    expressions = ['happy', 'sad', 'angry', 'focused', 'confused']
    for idx, expr in enumerate(expressions):
        btn = tk.Button(root, text=expr.capitalize(), command=lambda e=expr: eye_controller.express(e))
        btn.pack(side=tk.LEFT, padx=10, pady=10)

def main():
    root = tk.Tk()
    root.title("Expressive Robot Face for Tablet")

    canvas = Canvas(root, width=400, height=200)
    canvas.pack()

    eye_controller = EyeController(canvas)

    create_buttons(root, eye_controller)

    root.mainloop()

if __name__ == "__main__":
    main()
