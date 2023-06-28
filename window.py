import sys, random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главное окно")
        self.setGeometry(100, 100, 400, 300)

        self.logo_label = QLabel("Логотип")
        self.titleLabel = QLabel("Название мероприятия")
        self.directionLabel = QLabel("Направление мероприятия")
        self.dateLabel = QLabel("Дата")
        self.direction_filter_edit = QLineEdit()
        self.date_filter_edit = QLineEdit()
        self.filter_button = QPushButton("Фильтровать")
        self.login_button = QPushButton("Авторизация")

        layout = QVBoxLayout()
        layout.addWidget(self.logo_label)
        layout.addWidget(self.titleLabel)
        layout.addWidget(self.directionLabel)
        layout.addWidget(self.dateLabel)
        layout.addWidget(QLabel("Фильтр по направлению:"))
        layout.addWidget(self.direction_filter_edit)
        layout.addWidget(QLabel("Фильтр по дате:"))
        layout.addWidget(self.date_filter_edit)
        layout.addWidget(self.filter_button)
        layout.addWidget(self.login_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        TwoWindow = LoginWindow()
        self.login_button.clicked.connect(self.TwoWindow)

    def TwoWindow(self):
        self.TwoWindows = LoginWindow()
        self.TwoWindows.show()



class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация')
        self.setGeometry(300, 300, 300, 150)

        self.username_label = QLabel('Логин:')
        self.password_label = QLabel('Пароль:')
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Войти')

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.captcha_dialog = CaptchaDialog(parent=self)
        self.captcha_dialog.setModal(True)
        self.login_attempts = 0

        self.login_button.clicked.connect(self.login)

    def login(self):
        login = self.username_input.text()
        password = self.password_input.text()

        if login and password:
            role = self.get_user_role(login, password)
            if role == "Организатор":
                self.open_organizer_window()
            elif role == "Участник":
                self.open_participant_window()
            elif role == "Модератор":
                self.open_moderator_window()
            elif role == "Жюри":
                self.open_jury_window()
            else:
                QMessageBox.critical(self, "Ошибка", "Неверные логин или пароль")
        else:
            self.captcha_dialog.start_timer()
                            
            if self.captcha_dialog.exec() == QDialog.DialogCode.Accepted:
                QMessageBox.information(self, "Успех", "Вход выполнен после капчи")
                self.organizedWin = OrganizerWindow()
                self.organizedWin.show()
                            
            else:
                QMessageBox.warning(self, "Ошибка", "Неверные данные и капча")
                self.login_attempts = 0
                self.generate_captcha()
            

    def get_user_role(self, login, password):
        if login == "admin" and password == "admin":
            return "Организатор"
        elif login == "participant" and password == "participant":
            return "Участник"
        elif login == "moderator" and password == "moderator":
            return "Модератор"
        elif login == "jury" and password == "jury":
            return "Жюри"
        else:
            return None

    def open_organizer_window(self):
        self.hide()
        self.organizer_window = OrganizerWindow()
        self.organizer_window.show()

    def open_participant_window(self):
        self.hide()
        self.participant_window = ParticipantWindow()
        self.participant_window.show()

    def open_moderator_window(self):
        self.hide()
        self.moderator_window = ModeratorWindow()
        self.moderator_window.show()

    def open_jury_window(self):
        self.hide()
        self.jury_window = JuryWindow()
        self.jury_window.show()



class CaptchaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Капча")
        self.label = QLabel("Введите капчу:")
        self.textbox = QLineEdit()
        self.button = QPushButton("Проверить")
        self.button.clicked.connect(self.verify_captcha)
        self.generate_captcha()

        
        self.timer_label = QLabel("Таймер: 10")
        self.timer_counter = 10
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def verify_captcha(self):
        captcha = self.textbox.text()
        print("Проверка капчи:", captcha)


        if captcha.lower() == self.label.text(): 
            self.accept()
        else:
            self.textbox.setDisabled(True)  
            self.timer_counter = 11
            self.generate_captcha()
            self.timer.start()
            QMessageBox.critical(self, "Ошибка", "Неправильная капча")

    def start_timer(self):
        
        self.timer_counter = 10
        self.timer.start()
        

    def update_timer(self):
        self.timer_counter -= 1
        self.timer_label.setText(f"Таймер: {self.timer_counter}")

        if self.timer_counter == 0:
            self.timer.stop()
            self.textbox.setDisabled(False)
            
        self.captcha_label = QLabel(self)
        self.captcha_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

    def generate_captcha(self):
        captcha1 = str(random.randint(1000, 9999))
        self.label.setText(captcha1)
    
class OrganizerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Организатор мероприятий")
        self.setGeometry(100, 100, 400, 300)

        current_time = QTime.currentTime()

        if QTime(9, 0) <= current_time <= QTime(11, 0):
            period = "Утро"
        elif QTime(11, 1) <= current_time <= QTime(18, 0):
            period = "День"
        elif QTime(18, 1) <= current_time <= QTime(23, 59):
            period = "Вечер"
        else:
            period = "Ночь"

        self.greeting_label = QLabel(f"Доброе {period}!")
        self.greeting_label.setAlignment(Qt.AlignCenter)

        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignCenter)

        self.avatar_label.setPixmap(QPixmap("avatar.jpg"))

        self.logout_button = QPushButton("Выход")
        self.logout_button.clicked.connect(self.logout)

        layout = QVBoxLayout()
        layout.addWidget(self.greeting_label)
        layout.addWidget(self.avatar_label)
        layout.addWidget(self.logout_button)
        layout.setAlignment(Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.greeting_label.setText(f"Доброе {self.get_period()}, Артём Викторович! Текущее время: {current_time}")

    def get_period(self):
        current_time = QTime.currentTime()
        if QTime(9, 0) <= current_time <= QTime(11, 0):
            period = "Утро"
        elif QTime(11, 1) <= current_time <= QTime(18, 0):
            period = "День"
        elif QTime(18, 1) <= current_time <= QTime(23, 59):
            period = "Вечер"
        else:
            period = "Ночь"
        return period

    def logout(self):
        self.close()



class ParticipantWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно участника")
        self.setGeometry(100, 100, 400, 300)
        


class ModeratorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно модератора")
        self.setGeometry(100, 100, 400, 300)


class JuryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Окно жюри")
        self.setGeometry(100, 100, 400, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = MainWindow()
    login_window.show()
    sys.exit(app.exec_())
