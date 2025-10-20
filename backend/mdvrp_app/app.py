from flask import Flask, request, jsonify
from flask_cors import CORS
from mdvrp_solver import solve_mdvrp_enhanced
import json

app = Flask(__name__)
CORS(app)


@app.route('/api/calculate/', methods=['POST'])
def calculate_routes():
    """
    POST request từ frontend
    Body: {
        "num_vehicles_per_depot": 2,
        "strategy": "benchmark",  # hoặc "strategy1", "strategy2", "strategy3"
        "time_limit": 45
    }
    """
    try:
        data = request.json
        num_vehicles = data.get('num_vehicles_per_depot', 2)
        strategy = data.get('strategy', 'benchmark')
        time_limit = data.get('time_limit', 45)

        # Load dữ liệu
        with open('data/depots.json') as f:
            depots_data = json.load(f)
        with open('data/customers.json') as f:
            customers_data = json.load(f)

        # Chuyển đổi dữ liệu sang tọa độ (x, y)
        depots = [(d['longitude'], d['latitude']) for d in depots_data]
        customers = [(c['longitude'], c['latitude']) for c in customers_data]

        # Gọi solver
        result = solve_mdvrp_enhanced(
            depots=depots,
            customers=customers,
            num_vehicles_per_depot=num_vehicles,
            strategy=strategy,
            time_limit=time_limit
        )

        return jsonify({
            'status': 'success',
            'data': result
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400


@app.route('/api/strategies/', methods=['GET'])
def get_strategies():
    """Trả về danh sách các chiến lược có sẵn"""
    return jsonify({
        'strategies': [
            {'id': 'strategy1', 'name': 'PATH_CHEAPEST_ARC + GUIDED_LOCAL_SEARCH'},
            {'id': 'strategy2', 'name': 'PATH_MOST_CONSTRAINED_ARC + SIMULATED_ANNEALING'},
            {'id': 'strategy3', 'name': 'NEAREST_NEIGHBOR + TABU_SEARCH'},
            {'id': 'benchmark', 'name': 'Benchmark All Strategies'},
            {'id': 'benchmark_with_2opt', 'name': 'Benchmark + 2-opt Optimization'}
        ]
    })


if __name__ == '__main__':
    app.run(debug=True, port=8000)