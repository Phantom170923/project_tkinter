import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.width = 600
        self.height = 400

        self.image = Image.new("RGB", (self.width, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pipette_color)

        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

    # Метод, который отвечает за создание и расположение виджетов управления
    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        update_button = tk.Button(control_frame, text='Изменить размеры холста', command=self.update_canvas)
        update_button.pack(side=tk.LEFT)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        color_label = tk.Button(control_frame, text='Предпросмотр цвета кисти', command=self.draw_label)
        color_label.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        text = tk.Button(control_frame, text='Добавление текста', command=self.add_text)
        text.pack(side=tk.LEFT)

        update_color_canvas = tk.Button(control_frame, text='Изменение цвета фона', command=self.update_canvas_color)
        update_color_canvas.pack(side=tk.LEFT)

        self.brush_size = tk.IntVar()
        self.brush_size.set(1)

        self.brush_button = tk.Button(control_frame, text="Кисть", state=tk.NORMAL)
        self.brush_button.pack(side=tk.LEFT)

        self.eraser = tk.Button(control_frame, text='Ластик', state=tk.NORMAL, command=self.change_state_eraser)
        self.eraser.pack(side=tk.LEFT)

        self.brush_size_button = tk.Label(control_frame, text='Размер кисти:')
        self.brush_size_button.pack(side=tk.LEFT)

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

    # Метод, который позволяет добавить текст на изображение
    def add_text(self):
        text_w = simpledialog.askstring('Добавление текста', prompt='Введите текст')
        text = f'{text_w}'

        if text_w:
            x = simpledialog.askinteger('Координата Х',
                                        prompt='Введите координату Х',
                                        minvalue=0,
                                        maxvalue=self.width)

            y = simpledialog.askinteger('Координата Y',
                                        prompt='Введите координату Y',
                                        minvalue=0,
                                        maxvalue=self.height)

            self.canvas.create_text(x, y, text=text, fill=self.pen_color)

    # Метод, который позволяет сделать предпросмотр цвета кисти
    def draw_label(self):
        text_color = 'black' if self.pen_color == 'white' else 'white'
        self.lbl = tk.Label(master=self.root, text='Цвет кисти', bg=self.pen_color, fg=text_color)
        self.lbl.pack()

    # Метод, который обновляет размеры кисти из списка значений.
    def update_size_brush(self, value):
        self.brush_size.set(value)

    def change_state_eraser(self) -> None:
        if self.brush_button['state'] == tk.NORMAL:
            self.brush_button['state'] = tk.DISABLED
        else:
            self.brush_button['state'] = tk.NORMAL

    # Функция рисует линии на холсте Tkinter и параллельно на объекте Image из Pillow
    def paint(self, event):
        if self.brush_button['state'] == tk.NORMAL:
            if self.last_x and self.last_y:
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        width=self.brush_size_scale.get(), fill=self.pen_color,
                                        capstyle=tk.ROUND, smooth=tk.TRUE)
                self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                               width=self.brush_size_scale.get())

            self.last_x = event.x
            self.last_y = event.y
        else:
            if self.last_x and self.last_y:
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        width=self.brush_size_scale.get(), fill='white',
                                        capstyle=tk.ROUND, smooth=tk.TRUE)
                self.draw.line([self.last_x, self.last_y, event.x, event.y], fill='white',
                               width=20)

            self.last_x = event.x
            self.last_y = event.y

    # Метод сбрасывает последние координаты кисти
    def reset(self, event):
        self.last_x, self.last_y = None, None

    # Метод очищает холст, удаляя все нарисованное, и пересоздает объекты Image и ImageDraw для нового изображения.
    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.width, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)

    # Метод открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий для кисти
    def choose_color(self, event=None):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    # Метод позволяет пользователю сохранить изображение
    def save_image(self, event):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def change_size(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

    # Метод, который получает цвет на холсте и устанавливает его в pen_color
    def pipette_color(self, event):
        pipette = self.image.getpixel((event.x, event.y))
        pipette = '#{:02x}{:02x}{:02x}'.format(pipette[0], pipette[1], pipette[2])
        self.pen_color = pipette

    # Метод, который позволяет изменить размеры холста
    def update_canvas(self, event: tk.Event = None):

        agree = simpledialog.askstring('Согласие на изменение',
                                       prompt='Вы уверены? Текущий рисунок пропадет',
                                       initialvalue='Да')

        if agree == 'Да':

            width = simpledialog.askinteger(f'Текущий размер холста: {self.width}X{self.height}',
                                            prompt='Введите ширину',
                                            minvalue=50,
                                            maxvalue=1200,
                                            initialvalue=self.width)

            if width:
                self.width = width
                self.canvas.config(width=self.width, height=self.height)

            height = simpledialog.askinteger(f'Текущий размер холста: {self.width}X{self.height}',
                                             prompt='Введите высоту',
                                             minvalue=50,
                                             maxvalue=700,
                                             initialvalue=self.height)

            if height:
                self.height = height
            self.canvas.config(width=self.width, height=self.height)

            self.clear_canvas()

    def update_canvas_color(self, event: tk.Event = None):
        agree = simpledialog.askstring('Согласие на изменение',
                                       prompt='Вы уверены? Текущий рисунок пропадет',
                                       initialvalue='Да')

        if agree == 'Да':
            self.color_canvas = colorchooser.askcolor(color=self.pen_color)[1]

            self.canvas.config(background=self.color_canvas)

            self.clear_canvas()


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

