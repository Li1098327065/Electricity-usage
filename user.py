from flask import Flask, request, jsonify, render_template
import datetime

app = Flask(__name__)

# 模拟电表数据存储（字典形式）
electricity_data = {
    "meter_001": [
        {"timestamp": datetime.datetime.utcnow() - datetime.timedelta(minutes=15), "reading": 2.5},
        {"timestamp": datetime.datetime.utcnow() - datetime.timedelta(hours=1), "reading": 10.0},
        {"timestamp": datetime.datetime.utcnow() - datetime.timedelta(days=1), "reading": 50.0},
        {"timestamp": datetime.datetime.utcnow() - datetime.timedelta(weeks=1), "reading": 300.0},
        {"timestamp": datetime.datetime.utcnow() - datetime.timedelta(days=30), "reading": 1200.0},
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/usage', methods=['GET'])
def get_usage():
    try:
        meter_id = request.args.get('meter_id')
        period = request.args.get('period', '30m')
        
        if meter_id not in electricity_data:
            return jsonify({'status': 'error', 'message': 'Invalid meter ID'})
        
        now = datetime.datetime.utcnow()
        if period == '30m':
            start_time = now - datetime.timedelta(minutes=30)
        elif period == '1d':
            start_time = now - datetime.timedelta(days=1)
        elif period == '1w':
            start_time = now - datetime.timedelta(weeks=1)
        elif period == '1m':
            start_time = now - datetime.timedelta(days=30)
        else:
            return jsonify({'status': 'error', 'message': 'Invalid period'})
        
        usage = [entry for entry in electricity_data[meter_id] if entry['timestamp'] >= start_time]
        return render_template('usage.html', meter_id=meter_id, usage=usage)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
