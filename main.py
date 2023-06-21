import tkinter as tk
from tkinter import filedialog

from PyQt5 import QtWidgets

from circle_editor import ImageEditorWindow


def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[('JPEG', '*.jpg'), ('JPEG', '*.jpeg'), ('PNG', '*.png')])
    return file_path


def load_image():
    file_path = open_file_dialog()
    if file_path:
        target_path = 'input.jpg'

        with open(file_path, 'rb') as file:
            image_data = file.read()
            with open(target_path, 'wb') as output_file:
                output_file.write(image_data)

        print("Выбранное изображение: ", file_path)
        print("Путь для сохранения: ", target_path)
    else:
        print("Файл не выбран.")


if __name__ == "__main__":
    import sys
    load_image()
    app = QtWidgets.QApplication(sys.argv)
    image_path = "input.jpg"
    editor = ImageEditorWindow(image_path)
    editor.show_window()
    sys.exit(app.exec_())




