from flask import Flask, jsonify, render_template
import time
import threading

app = Flask(__name__)

task_in_progress = False

def simulate_long_running_task():
    global task_in_progress
    task_in_progress = True
    for i in range(1, 101):
        time.sleep(1)  # 模拟任务执行时间
        progress = i
        print("任务进度:", progress)
    print("任务完成！")
    task_in_progress = False

@app.route('/')
def index():
    return render_template('index_task.html')

@app.route('/start_task', methods=['POST'])
def start_task():
    global task_in_progress
    if not task_in_progress:
        task_thread = threading.Thread(target=simulate_long_running_task)
        task_thread.start()
        return jsonify({'message': '任务已启动！'})
    else:
        return jsonify({'message': '任务正在进行中！'})

@app.route('/task_status', methods=['GET'])
def task_status():
    if task_in_progress:
        return jsonify({'status': 'in_progress'})
    else:
        return jsonify({'status': 'completed'})

if __name__ == '__main__':
    app.run()
