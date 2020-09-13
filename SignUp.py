import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib

#注册窗口部件
class SignUpWidget(QWidget):
    #用户注册信号
    user_signup_signal = pyqtSignal(str)
    #初始化ui
    def __init__(self):
        super().__init__()
        self.setUpUI()
    #调用setUpUI()方法
    def setUpUI(self):
        self.resize(900, 600)
        self.setWindowTitle("OneSearch信息管理系统")
        
        self.signUpLabel = QLabel("注   册")
        self.signUpLabel.setAlignment(Qt.AlignCenter)  #Qt.AlignCenter 上下左右居中 
        # self.signUpLabel.setFixedWidth(300)
        #最佳匹配高度 宽度
        self.signUpLabel.setFixedHeight(300)
        

        #普适
        font = QFont()
        font.setPixelSize(36)
        #文字行控件文字对象
        lineEditFont = QFont()
        lineEditFont.setPixelSize(18)
        self.signUpLabel.setFont(font)



        #最外围使用竖直布局，加入部件
        self.layout = QVBoxLayout()
        #当前布局加入 label 并且设置位置
        self.layout.addWidget(self.signUpLabel, Qt.AlignHCenter)
        #将当前部件设置为竖直布局
        self.setLayout(self.layout)


        # 定义表单布局，包括学号，姓名，密码，确认密码
        self.formlayout = QFormLayout()
        #表单字体
        font.setPixelSize(18)
        # Row1 label左
        self.userIdLabel = QLabel("帐    号: ")
        self.userIdLabel.setFont(font)
        #文字控件右
        self.userIdLineEdit = QLineEdit()
        self.userIdLineEdit.setFixedWidth(180)
        self.userIdLineEdit.setFixedHeight(32)
        self.userIdLineEdit.setFont(lineEditFont)
        self.userIdLineEdit.setMaxLength(20)
        self.formlayout.addRow(self.userIdLabel, self.userIdLineEdit)

        # Row2
        self.userNameLabel = QLabel("姓    名: ")
        self.userNameLabel.setFont(font)
        self.userNameLineEdit = QLineEdit()
        self.userNameLineEdit.setFixedHeight(32)
        self.userNameLineEdit.setFixedWidth(180)
        self.userNameLineEdit.setFont(lineEditFont)
        self.userNameLineEdit.setMaxLength(20)
        self.formlayout.addRow(self.userNameLabel, self.userNameLineEdit)

        lineEditFont.setPixelSize(10)

        # Row3
        self.passwordLabel = QLabel("密    码: ")
        self.passwordLabel.setFont(font)
        # self.passwordLabel.setStyleSheet("QLabel{color:rgb(225,22,173,255);font-size:50px;font-weight:normal;font-family:Arial;}")
        # self.passwordLabel.setStyleSheet("font:18pt '楷体';border-width: 1px;border-style: solid;border-color: rgb(255, 0, 0);")
        self.passwordLineEdit = QLineEdit()

        self.passwordLineEdit.setFixedWidth(180)
        self.passwordLineEdit.setFixedHeight(32)
        self.passwordLineEdit.setFont(lineEditFont)
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLineEdit.setMaxLength(16)
        self.formlayout.addRow(self.passwordLabel, self.passwordLineEdit)

        # Row4
        self.passwordConfirmLabel = QLabel("确认密码: ")
        #QFont("Roman times",15)
        self.passwordConfirmLabel.setFont(font)
        self.passwordConfirmLineEdit = QLineEdit()
        self.passwordConfirmLineEdit.setFixedWidth(180)
        self.passwordConfirmLineEdit.setFixedHeight(32)
        self.passwordConfirmLineEdit.setFont(lineEditFont)
        self.passwordConfirmLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordConfirmLineEdit.setMaxLength(16)
        self.formlayout.addRow(self.passwordConfirmLabel, self.passwordConfirmLineEdit)

        # Row5
        self.signUpbutton = QPushButton("注 册")
        self.signUpbutton.setFixedWidth(120)
        self.signUpbutton.setFixedHeight(30)
        self.signUpbutton.setFont(font)
        self.formlayout.addRow("", self.signUpbutton)

        #新建一个部件，加入上面的formlayout布局
        widget = QWidget()
        widget.setLayout(self.formlayout)
        widget.setFixedHeight(250)
        widget.setFixedWidth(300)
        self.Hlayout = QHBoxLayout()
        self.Hlayout.addWidget(widget, Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(self.Hlayout)
        self.layout.addWidget(widget, Qt.AlignHCenter)
        
        # 设置验证
        #正则规则
        reg = QRegExp("PB[0~9]{8}")
        #验证器
        pValidator = QRegExpValidator(self)
        #设置验证
        pValidator.setRegExp(reg)
        
        #对userId进行Validator
        self.userIdLineEdit.setValidator(pValidator)
        #密码验证
        reg = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg)
        self.passwordLineEdit.setValidator(pValidator)
        self.passwordConfirmLineEdit.setValidator(pValidator)

        #按钮绑定，在任意一个输入框按enter后，则可以进行signup方法
        self.signUpbutton.clicked.connect(self.SignUp)
        self.userIdLineEdit.returnPressed.connect(self.SignUp)
        self.userIdLineEdit.returnPressed.connect(self.SignUp)
        self.passwordLineEdit.returnPressed.connect(self.SignUp)
        self.passwordConfirmLineEdit.returnPressed.connect(self.SignUp)

    def SignUp(self):
        #拿到userId的文本
        userId = self.userIdLineEdit.text()
        userName = self.userNameLineEdit.text()
        password = self.passwordLineEdit.text()
        confirmPassword = self.passwordConfirmLineEdit.text()
        #除掉 空的情况，否则就打开db再进行判断
        if (userId == "" or userName == "" or password == "" or confirmPassword == ""):
            print(QMessageBox.warning(self, "警告", "账户或密码不可为空，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:  # 需要处理逻辑，1.账号已存在;2.密码不匹配;3.插入user表
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('C:\\Users\\chy\\LibraryManageDesktopApp\\oneSearch\\db\\sciinfo.db')
            #打开db数据库
            db.open()
            #实例化查询对象
            query = QSqlQuery()
            print("打开了查询对象")
            if (confirmPassword != password):
                print(QMessageBox.warning(self, "警告", "两次输入密码不一致，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
                return
            elif (confirmPassword == password):
                # md5编码
                hl = hashlib.md5()
                hl.update(password.encode(encoding='utf-8'))
                md5password = hl.hexdigest()
                #userId在库中作为id
                sql = "SELECT * FROM User WHERE userId='%s'" % (userId)
                query.exec_(sql)
            
                if (query.next()):
                    print(QMessageBox.warning(self, "警告", "该账号已存在,请重新输入", QMessageBox.Yes, QMessageBox.Yes))
                    return
                else:
                    sql = "INSERT INTO User VALUES ('%s','%s','%s',0,0,0)" % (
                        userId, userName, md5password)
                    db.exec_(sql)
                    db.commit()
                    print("执行提交语句")
                    print(QMessageBox.information(self, "提醒", "您已成功注册账号!", QMessageBox.Yes, QMessageBox.Yes))
                    #将注册好的信息用来登录
                    self.user_signup_signal.emit(userId)
                db.close()
                return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    # 
    # 
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = SignUpWidget()
    # mainMindow.passwordLabel.setStyleSheet("font:18pt '楷体';border-width: 1px;border-style: solid;border-color: rgb(255, 0, 0);")
    mainMindow.show()
    sys.exit(app.exec_())
