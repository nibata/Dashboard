from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
import json
import uuid
import os

app = Flask(__name__)

# Path to the configuration file
CONFIG_PATH = 'config.json'


# Load existing configuration
def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    else:
        return {'graphs': []}


# Save configuration
def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)


@app.route('/')
def index():
    config = load_config()
    return render_template('index.html', graphs=config['graphs'])


@app.route('/add_graph', methods=['POST'])
def add_graph():
    data = request.get_json()
    graph_type = data['graphType']
    graph_title = data['graphTitle']

    div_id = str(uuid.uuid4())

    # Generate plot data based on graph type
    x_data = [1, 2, 3, 4, 5]
    y_data = [10, 14, 19, 23, 28]

    if graph_type == 'scatter':
        trace = go.Scatter(x=x_data, y=y_data, mode='markers', name=graph_title)
    elif graph_type == 'bar':
        trace = go.Bar(x=x_data, y=y_data, name=graph_title)
    elif graph_type == 'line':
        trace = go.Scatter(x=x_data, y=y_data, mode='lines', name=graph_title)
    else:
        return jsonify({'error': 'Invalid graph type'}), 400

    fig = go.Figure(data=[trace])
    fig.update_layout(title=graph_title, xaxis_title='X Axis', yaxis_title='Y Axis')
    plot_data = fig.to_json()

    # Load the existing configuration
    config = load_config()
    config['graphs'].append({
        'graphType': graph_type,
        'graphTitle': graph_title,
        'div_id': div_id,
        'plot_data': plot_data
    })
    save_config(config)

    return jsonify({'plot_data': json.loads(plot_data), 'div_id': div_id})


if __name__ == '__main__':
    app.run(debug=True)
