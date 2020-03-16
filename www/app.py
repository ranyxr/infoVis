from flask import Flask, render_template, request
from Processor.DataProcessor import DataProcessor as Dp
app = Flask(__name__)

dp = Dp()
stack_x_axis_data = dp.get_x_axis()
stack_item_data = dp.get_stack_data()
word_cloud_chart_data = dp.get_word_cloud_data()


@app.route('/')
def index():
    return render_template(
        'index.html',
        stack_x_axis_data=stack_x_axis_data,
        stack_item_data=stack_item_data,
        word_cloud_chart_data=word_cloud_chart_data
    )


@app.route('/api/x_axis')
def get_x_axis():
    return 'Hello World!'


@app.route('/api/stack_data')
def get_stack_data():
    return 'Hello World!'


@app.route('/api/filter', methods=['POST'])
def data_filter():
    rd = request.get_json()
    print(rd)
    sy = rd["start_year"]
    ey = rd["end_year"]
    return dp.data_filter(sy, ey)


if __name__ == '__main__':
    app.run()
