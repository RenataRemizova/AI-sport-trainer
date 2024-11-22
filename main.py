# импорты
import customtkinter as ctk
import numpy as np
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import PoseModule as pm

# тема - белая
ctk.set_appearance_mode("light")

# модуль позы
detector = pm.poseDetector()


# приложение
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("AI trainer")
        self.geometry("1000x600")

        # создание холста
        self.canvas = tk.Canvas(self, width=1000, height=600)

        # необходимые далее переменные
        self.button_is_pressed = False
        self.count = 0

        self.home()

    # главное окно
    def home(self):
        # элементы дизайна
        rect_bg = self.canvas.create_rectangle(0, 50, 1000, 300, fill="#08152F", width=0)
        line = self.canvas.create_line(100, 350, 100, 400, fill="#08152F", width=5)
        circle1 = self.canvas.create_oval(-100, 500, 100, 700, fill="#6BC0C4", width=0)
        circle2 = self.canvas.create_oval(850, 450, 1150, 750, fill="#6BC0C4", width=0)

        # цитата
        label = ctk.CTkLabel(self, text="“Единственная плохая тренировка - та, которой не было.”", text_color="#08152F",
                             font=("Arial", 28), bg_color="#F0F0F0")
        label.place(x=150, y=350)

        # кнопка старта
        button = ctk.CTkButton(self, text="Начать заниматься сегодня", width=600, height=60, fg_color="#D02527",
                               text_color="#ffffff", font=("Arial", 25), corner_radius=20, hover_color="#08152F",
                               command=self.train)
        button.place(x=200, y=450)

        # иконка главной страницы
        home = Image.open("icons8-home-64.png")
        home = home.resize((45, 45), Image.Resampling.LANCZOS)
        home_2 = ImageTk.PhotoImage(home)
        label_home = tk.Label(image=home_2)
        label_home.image = home_2
        label_home.place(x=10, y=0)

        # изображения для примера
        ex_img1 = Image.open("woman.png")
        ex_img1 = ex_img1.resize((350, 200), Image.Resampling.LANCZOS)
        ex_img_2 = ImageTk.PhotoImage(ex_img1)
        label_ex_img = tk.Label(image=ex_img_2)
        label_ex_img.image = ex_img_2
        label_ex_img.place(x=100, y=75)

        ex_img2 = Image.open("man.jpg")
        ex_img2 = ex_img2.resize((350, 200), Image.Resampling.LANCZOS)
        ex_img2_2 = ImageTk.PhotoImage(ex_img2)
        label_ex_img2 = tk.Label(image=ex_img2_2)
        label_ex_img2.image = ex_img2_2
        label_ex_img2.place(x=550, y=75)

        self.canvas.pack()
        self.lst_widgets = [label, button, label_home, label_ex_img, label_ex_img2]

    # очистка окна
    def clear(self):
        self.canvas.delete("all")
        for widget in self.lst_widgets:
            widget.destroy()

    # считывание видео с веб камеры
    def train(self):
        self.clear()

        # декоративные элементы
        rect = self.canvas.create_rectangle(345, 150, 1000, 600, fill="#08152F", width=0)
        line = self.canvas.create_line(340, 0, 340, 600, fill="#D02527", width=10)

        # кнопка досрочного завершения
        button = ctk.CTkButton(self, text="Досрочное завершение", width=150, height=60, fg_color="#F0F0F0",
                               border_width=5, border_color="#6BC0C4",
                               text_color="#08152F", font=("Arial", 20), corner_radius=20, hover_color="#6BC0C4",
                               command=self.result)
        button.place(x=40, y=520)

        # элементы дизайна
        line = self.canvas.create_line(53, 50, 53, 170, width=5, fill="#08152F")
        mini_circle_1 = self.canvas.create_oval(43, 43, 63, 63, fill="#F0F0F0", outline="#6BC0C4", width=3)
        mini_circle_2 = self.canvas.create_oval(43, 153, 63, 173, fill="#F0F0F0", outline="#6BC0C4", width=3)

        # надписи упражнений
        ex_1_label = ctk.CTkLabel(self, text="Подъем на правый бицепс \n 10 раз", text_color="#08152F",
                                  font=("Arial", 20),
                                  bg_color="#f0f0f0")
        ex_1_label.place(x=80, y=50)
        ex_2_label = ctk.CTkLabel(self, text="Подъем на левый бицепс \n 10 раз", text_color="#08152F",
                                  font=("Arial", 20),
                                  bg_color="#f0f0f0")
        ex_2_label.place(x=80, y=150)

        # подписи показателей
        label_accuracy = ctk.CTkLabel(self, text="Процент", text_color="#ffffff",
                                      font=("Arial", 22), bg_color="#08152F")
        label_count = ctk.CTkLabel(self, text="Количество", text_color="#ffffff",
                                   font=("Arial", 22), bg_color="#08152F")

        label_accuracy.place(x=500, y=470)
        label_count.place(x=750, y=470)

        # переменные с показателями
        accuracy = 0
        count_right_1 = 0
        count_left_1 = 0

        # вывод показателей
        n_accuracy = ctk.CTkLabel(self, text=str(accuracy) + "%", text_color="#ffffff",
                                  font=("Arial", 22), bg_color="#08152F")
        n_count = ctk.CTkLabel(self, text=str(self.count) + " раз", text_color="#ffffff",
                               font=("Arial", 22), bg_color="#08152F")
        n_accuracy.place(x=500, y=520)
        n_count.place(x=750, y=520)

        webcam = cv2.VideoCapture(0)

        # необходимые далее переменные
        dir_right = 0
        dir_left = 0
        ex_1 = True
        ex_2 = False

        # метка для видео
        label = tk.Label(self.canvas)
        label.place(x=345, y=0)

        self.lst_widgets = [button, label_count, label_accuracy, n_accuracy, n_count, ex_1_label,
                            ex_2_label]

        while True:
            # считывание фрейма
            successful_frame_read, frame = webcam.read()
            frame = cv2.resize(frame, (650, 450))

            # перевод в rgb
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # находим позу
            frame = detector.findPose(frame)
            lmList = detector.findPosition(frame, False)

            # если человек в кадре
            if len(lmList) != 0:

                # находим углы
                angle_right_hand = detector.findAngle(frame, 12, 14, 16)
                angle_left_hand = detector.findAngle(frame, 11, 13, 15)

                # находим процент
                per_right = np.interp(angle_right_hand, (210, 310), (0, 100))
                per_right = int(per_right)
                per_left = np.interp(angle_left_hand, (30, 150), (0, 100))
                per_left = int(per_left)

                # упражнение 1 (правая рука)
                if ex_1:
                    n_accuracy.configure(text=str(per_right) + "%")

                    # счетчик количества
                    if per_right == 100:
                        if dir_right == 0:
                            count_right_1 += 0.5
                            dir_right = 1
                            n_count.configure(text=str(int(count_right_1)) + " раз")

                    if per_right == 0:
                        if dir_right == 1:
                            count_right_1 += 0.5
                            dir_right = 0
                            n_count.configure(text=str(int(count_right_1)) + " раз")

                    # если сделано необходимое количество
                    if count_right_1 >= 10:
                        ex_1 = False
                        ex_2 = True
                        # выводим показатель счетчика
                        n_count.configure(text=str(int(count_left_1)) + " раз")
                        # закрашиваем метку
                        mini_circle_1 = self.canvas.create_oval(43, 43, 63, 63, fill="#6BC0C4", outline="#6BC0C4",
                                                                width=3)
                        # добавляем к общему количеству
                        self.count += count_right_1

                # упражнение 2 (левая рука)
                if ex_2:
                    n_accuracy.configure(text=str(per_left) + "%")

                    # счетчик количества
                    if per_left == 100:
                        if dir_left == 0:
                            count_left_1 += 0.5
                            dir_left = 1
                            n_count.configure(text=str(int(count_left_1)) + " раз")

                    if per_left == 0:
                        if dir_left == 1:
                            count_left_1 += 0.5
                            dir_left = 0
                            n_count.configure(text=str(int(count_left_1)) + " раз")

                    # если сделано необходимое количество
                    if count_left_1 >= 10:
                        ex_2 = False
                        # закрашиваем метку
                        mini_circle_2 = self.canvas.create_oval(43, 153, 63, 173, fill="#6BC0C4", outline="#6BC0C4",
                                                                width=3)

                        # меняем вид кнопки
                        button.configure(text="Завершение", fg_color="#D02527",
                                         text_color="#ffffff", hover_color="#08152F", border_width=0)

                        # добавляем к общему количеству
                        self.count += count_left_1

            # вывод видео
            captured_image = Image.fromarray(frame)
            photo_image = ImageTk.PhotoImage(image=captured_image)
            label.photo_image = photo_image
            label.configure(image=photo_image)
            label.after(10, label.update())

            # если кнопка нажата, видео останавливается
            if self.button_is_pressed:
                label.photo_image = None
                label.configure(image='')
                label.destroy()
                break

    # окно результатов
    def result(self):

        # очистка окна
        self.clear()
        self.button_is_pressed = True

        # элементы дизайна
        rect = self.canvas.create_rectangle(0, 0, 1000, 250, fill="#08152F", width=0)
        circle1 = self.canvas.create_oval(-100, 300, 100, 600, fill="#D02527", width=0)
        circle2 = self.canvas.create_oval(-150, 400, 250, 800, fill="#6BC0C4", width=0)

        # надписи
        label_end = ctk.CTkLabel(self, text="Тренировка завершена!", text_color="#ffffff",
                                 font=("Arial", 32), bg_color="#08152F")
        label_end.place(x=400, y=100)
        label_end2 = ctk.CTkLabel(self, text="Вы отлично постарались!", text_color="#ffffff",
                                  font=("Arial", 22), bg_color="#08152F")
        label_end2.place(x=450, y=155)

        label_results = ctk.CTkLabel(self, text="Общие результаты:", text_color="#08152F",
                                     font=("Arial", 26), bg_color="#f0f0f0")
        label_results.place(x=450, y=280)

        label_count = ctk.CTkLabel(self, text="Количество", text_color="#08152F",
                                   font=("Arial", 22), bg_color="#f0f0f0")

        label_count.place(x=500, y=330)

        n_count = ctk.CTkLabel(self, text=str(int(self.count)) + " раз", text_color="#08152F",
                               font=("Arial", 22), bg_color="#f0f0f0")
        n_count.place(x=500, y=380)

        # кнопка возвращения на главную
        button = ctk.CTkButton(self, text="Вернуться на главную", width=600, height=60, fg_color="#D02527",
                               text_color="#ffffff", font=("Arial", 25), corner_radius=20, hover_color="#08152F",
                               command=self.home_return)
        button.place(x=350, y=500)
        self.lst_widgets = [label_end, label_end2, label_results, label_count, button, n_count]

    # возврат к главной странице
    def home_return(self):
        self.clear()
        self.home()


# запуск
if __name__ == '__main__':
    app = App()
    app.mainloop()