from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins='*')

task_in_progress = False


def simulate_long_running_task():
    global task_in_progress
    task_in_progress = True
    for i in range(1, 101):
        progress = i
        print("任务进度:", progress)
        socketio.emit('progress', {'progress': progress}, namespace='/')
        if task_in_progress:
            time.sleep(0.1 * i)  # 模拟任务执行时间
        else:
            time.sleep(0.01)
    print("任务完成！")
    task_in_progress = False
    socketio.emit('task_complete', namespace='/')


def gline2para(filepath):
    print(filepath)
    time.sleep(10)
    print("任务完成！")

    global task_in_progress
    task_in_progress = False


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('start_task')
def start_task():
    global task_in_progress
    if not task_in_progress:
        task_thread = threading.Thread(target=simulate_long_running_task)
        task_thread.start()

        task_thread = threading.Thread(target=gline2para("aaa"))
        task_thread.start()
        emit('task_started', {'message': '任务已启动！'}, namespace='/')
    else:
        emit('task_in_progress', {'message': '任务正在进行中！'}, namespace='/')


if __name__ == '__main__':
    socketio.run(app)
