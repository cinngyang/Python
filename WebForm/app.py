from flask import Flask    # 从flask包中导入Flask类
import routes

app = Flask(__name__)      # 通过Flask类创建一个app实例
app.config['SECRET_KEY'] = 'miaojie is great!'  # 对Flask进行配置



if __name__ == "__main__":
    app.run(debug=True, port=5001)