from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QPen, QColor, QPainter, QFont


class ImageEditorWindow(QtWidgets.QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Image Editor")
        self.image_path = image_path
        self.image = QtGui.QImage(image_path)
        self.scaled_image = self.scale_image()
        self.circles = []
        self.circle_x0 = 0
        self.circle_y0 = 0
        self.circle_width = 0
        self.circle_height = 0
        self.is_mouse_pressed = False
        self.is_mouse_wheel_pressed = False
        self.curr_circle = None
        self.roll_x = 0
        self.roll_y = 0
        self.offset_x = 0
        self.offset_y = 0
        self.y_on_start = 0
        self.setMouseTracking(True)

        self.res = 0

    def scale_image(self):
        screen_size = QtWidgets.QDesktopWidget().screenGeometry()
        scaled_image = self.image.scaled(screen_size.width(), screen_size.height(),
                                         QtCore.Qt.KeepAspectRatio)
        return scaled_image

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 0, 0), 2))
        painter.setRenderHint(QPainter.Antialiasing)

        painter.drawImage(self.rect(), self.scaled_image)

        for circle in self.circles:
            x, y, diameter = circle
            painter.drawEllipse(x, y, diameter, diameter)

        if self.is_mouse_pressed:
            painter.drawEllipse(self.circle_x0, self.circle_y0, min(self.circle_width, self.circle_height), min(self.circle_width, self.circle_height))

        if len(self.circles) == 2:
            font = QFont("Arial", 20)
            color = QColor(255, 0, 0)
            painter.setFont(font)
            painter.setPen(color)
            self.res = min(self.circles[0][2], self.circles[1][2]) / max(self.circles[0][2], self.circles[1][2])
            painter.drawText(100, 100, f'{self.res}')

    def mouseMoveEvent(self, event):
        if self.is_mouse_pressed:
            x = event.pos().x()
            y = self.y_on_start
            width = abs(x - self.circle_x0)
            height = width
            self.circle_y0 = y - width / 2

            self.circle_width, self.circle_height = width, height
            self.update()
        elif self.is_mouse_wheel_pressed and self.curr_circle is not None:
            x, y = event.pos().x(), event.pos().y()
            self.curr_circle[0] += x - self.roll_x
            self.curr_circle[1] += y - self.roll_y
            self.roll_x, self.roll_y = x, y
            self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.is_mouse_pressed = True
            self.circle_x0, self.circle_y0 = event.pos().x(), event.pos().y()
            self.y_on_start = self.circle_y0
        elif event.button() == QtCore.Qt.RightButton:
            x, y = event.pos().x(), event.pos().y()
            circle_to_remove = None
            for circle in self.circles:
                if x >= circle[0] and x <= circle[0] + circle[2] and y >= circle[1] and y <= circle[1] + circle[2]:
                    circle_to_remove = circle
            if circle_to_remove:
                self.circles.remove(circle_to_remove)
                self.update()
        elif event.button() == QtCore.Qt.MiddleButton:
            self.is_mouse_wheel_pressed = True
            x, y = event.pos().x(), event.pos().y()
            for circle in self.circles:
                if x >= circle[0] and x <= circle[0] + circle[2] and y >= circle[1] and y <= circle[1] + circle[2]:
                    self.curr_circle = circle
                    self.offset_x, self.offset_y = x - circle[0], y - circle[1]
            self.roll_x, self.roll_y = x, y

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.is_mouse_pressed = False
            x = event.pos().x()
            y = self.y_on_start
            width = abs(x - self.circle_x0)
            height = width
            self.circle_y0 = y - width / 2

            self.circles.append([self.circle_x0, self.circle_y0, min(self.circle_width, self.circle_height)])
            self.update()
        elif event.button() == QtCore.Qt.MiddleButton:
            self.is_mouse_wheel_pressed = False
            x, y = event.pos().x(), event.pos().y()

            if self.curr_circle is not None:
                diameter = self.curr_circle[2]
                self.curr_circle[0] = x - self.offset_x
                self.curr_circle[1] = y - self.offset_y
                self.curr_circle = None
            self.update()

    def closeEvent(self, event):
        self.save_output()
        self.close()

    def save_output(self):
        if len(self.circles) == 2:
            with open("result_diameter.txt", "w") as file:
                self.res = min(self.circles[0][2], self.circles[1][2]) / max(self.circles[0][2], self.circles[1][2])
                file.write(f"{self.circles[0][2], self.circles[1][2], self.res}")
        else:
            return

    def show_window(self):
        self.setGeometry(100, 100, self.scaled_image.width(), self.scaled_image.height())
        self.show()
