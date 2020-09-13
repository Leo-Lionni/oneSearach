#C:\Users\chy\AppData\Local\conda\conda\envs\py36\Library\plugins 出现错误的时候解决办法
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import *
import qdarkstyle
from SignIn import SignInWidget
from SignUp import SignUpWidget
import sip

from AdminHome import AdminHome
from UserHome import UserHome
from changePasswordDialog import changePasswordDialog



class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.widget = SignInWidget()

        self.resize(900, 600)
        self.setWindowTitle("OneSearch信息管理系统")
        self.setCentralWidget(self.widget)
        bar = self.menuBar()
        self.Menu = bar.addMenu("菜单栏")
        # self.Menu =bar.addMenu("工具栏")
        self.signUpAction = QAction("注册", self)
        self.changePasswordAction =QAction("修改密码",self)
        self.signInAction = QAction("登录", self)
        self.quitSignInAction = QAction("退出登录", self)
        self.quitAction = QAction("退出", self)
        self.Menu.addAction(self.signUpAction)
        self.Menu.addAction(self.changePasswordAction)
        self.Menu.addAction(self.signInAction)
        self.Menu.addAction(self.quitSignInAction)
        self.Menu.addAction(self.quitAction)

        #设置默认状态，也就是主页面的状态，其余须跳转
        self.signUpAction.setEnabled(True)
        self.changePasswordAction.setEnabled(True)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(False) #quit按钮是默认激活的
        # self.quitAction.setEnabled(False) #不用管这个Quit

        #绑定方法，跳跃至其他界面的操作
        self.widget.is_admin_signal.connect(self.adminSignIn) 
        #如果是user，则是connect这个方法
        self.widget.is_user_signal[str].connect(self.userSignIn)
        self.Menu.triggered[QAction].connect(self.menuTriggered)

    #被绑定的方法  管理员
    def adminSignIn(self):
        sip.delete(self.widget)
        self.widget = AdminHome()
        self.setCentralWidget(self.widget)
        self.changePasswordAction.setEnabled(False)
        self.signUpAction.setEnabled(True)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(True)
    #用户登录
    def userSignIn(self, userId):
        sip.delete(self.widget)
        self.widget = UserHome(userId)
        self.setCentralWidget(self.widget)
        self.changePasswordAction.setEnabled(False)
        self.signUpAction.setEnabled(True)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(True)
    #菜单触发行为
    def menuTriggered(self, q):
        if(q.text()=="修改密码"):
            changePsdDialog=changePasswordDialog(self)
            changePsdDialog.show()
            changePsdDialog.exec_()
        if (q.text() == "注册"):
            sip.delete(self.widget)
            print("clicked reg")
            self.widget = SignUpWidget()
            self.setCentralWidget(self.widget)

            self.widget.user_signup_signal[str].connect(self.userSignIn)
            self.signUpAction.setEnabled(False)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(True)
            self.quitSignInAction.setEnabled(False)
            print("_"*50)
        #这里仅仅是退出登录而已，还是需要保留界面，以待其余用户登录使用或注册
        if (q.text() == "退出登录"):
            sip.delete(self.widget)
            #粗暴删除原有界面widget，随后重新实例SignWidgets
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            #捆绑方法
            self.widget.is_admin_signal.connect(self.adminSignIn)
            self.widget.is_user_signal[str].connect(self.userSignIn)
            self.signUpAction.setEnabled(True)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(False)
        if (q.text() == "登录"):
            sip.delete(self.widget)
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.is_admin_signal.connect(self.adminSignIn)
            self.widget.is_user_signal[str].connect(self.userSignIn)
            self.signUpAction.setEnabled(True)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(False)
        if (q.text() == "退出"):
            #产生实例后调用quit方法
            qApp = QApplication.instance()
            qApp.quit()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = Main()
    mainMindow.show()
    sys.exit(app.exec_())
