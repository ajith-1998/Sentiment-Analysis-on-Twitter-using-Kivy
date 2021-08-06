from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivymd.icon_definitions import md_icons
from database import DataBase
from sentiment import SentimentAnalysis


class CreateAccountWindow(Screen,MDApp):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen,MDApp):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen,MDApp):

    searchItem = ObjectProperty(None)
    noItems = ObjectProperty(None)

    current = ""


    def savegetdata(self):
        pass


    def on_exit(self, *args):
        pass

    def logout(self):
        sm.current = "login"
        pass

    def gosenti(self):
        self.manager.sw.search_Item.text = self.ids.searchItem.text
        sm.current = "senti"

        pass


class SentiWindow(Screen,MDApp):
    searchI = ObjectProperty(None)
    search_Item = ObjectProperty(MainWindow)
    a = ObjectProperty(SentimentAnalysis)
    b = ObjectProperty(SentimentAnalysis)
    c = ObjectProperty(SentimentAnalysis)
    d = ObjectProperty(SentimentAnalysis)
    e = ObjectProperty(SentimentAnalysis)
    a1 = ObjectProperty(None)
    b1 = ObjectProperty(None)
    c1 = ObjectProperty(None)
    d1 = ObjectProperty(None)
    e1 = ObjectProperty(None)

    current = ""

    def on_enter(self, *args):

        self.searchI.text = "Search Item : " + self.search_Item.text
        self.a, self.b, self.c, self.d = sa.DownloadData(self.search_Item.text)
        self.a1.text = "Overall Sentiment : " + self.a
        self.b1.text = "Percentage of Positive tweets : " + self.b
        self.c1.text = "Percentage of Negative tweets : " + self.c
        self.d1.text = "Percentage of Neutral tweets : " + self.d

    def gomain(self):
        sm.current = "main"
        pass

    def logout(self):
        sm.current = "login"
        pass


class WindowManager(ScreenManager):
    mw = MainWindow()
    sw = SentiWindow()
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")
sa = SentimentAnalysis()
sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main"), SentiWindow(name="senti")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.primary_hue = "500"
        return sm


if __name__ == "__main__":
    MyMainApp().run()