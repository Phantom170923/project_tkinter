import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)



    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.brush_size = tk.IntVar()
        self.brush_size.set(1)

        brush_size_label = tk.Label(control_frame, text="Размер кисти:")
        brush_size_label.pack(side=tk.LEFT, padx=(5, 2))

        sizes = [1, 3, 5, 10]

        size_menu = tk.OptionMenu(control_frame,
                                  self.brush_size,
                                  *sizes,
                                  command=self.update_size_brush)
        size_menu.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame,
                                         from_=1, to=10,
                                         orient=tk.HORIZONTAL,
                                         variable=self.brush_size,
                                         length=100,
                                         command=self.update_size_brush)
        self.brush_size_scale.pack(side=tk.LEFT)

    def update_size_brush(self, value):
        self.brush_size.set(value)

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size_scale.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size_scale.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def change_size(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()