from flask import Flask, render_template, request, jsonify
from waitress import serve
from nfa import My_NFA

app = Flask(__name__)
nfa = My_NFA()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', effects=nfa.get_all_effects())

@app.route('/find_recipe', methods=['POST'])
def find_recipe():
    """Handle recipe finding mode"""
    data = request.json
    initial_effects = set(data.get('initial', []))
    target_effects = set(data.get('target', []))
    
    path, side_effects = nfa.find_shortest_path_from_initial(
        initial_effects=initial_effects,
        target_effects=target_effects
    )
    
    result = {
        'success': path is not None,
        'path': path if path is not None else [],
        'side_effects': list(side_effects) if side_effects else [],
        'already_has_target': path == []
    }
    
    return jsonify(result)

@app.route('/maximize_price', methods=['POST'])
def maximize_price():
    """Handle maximization mode"""
    data = request.json
    initial_effects = set(data.get('initial', []))
    max_time = int(data.get('max_time', 10))
    budget = float(data.get('budget', 50.0))
    
    solution = nfa.solve_knapsack(
        budget=budget,
        max_time=max_time,
        initial_state=frozenset(initial_effects) if initial_effects else frozenset({'Nothing'})
    )
    
    return jsonify(solution)

@app.route('/effects', methods=['GET'])
def get_effects():
    """Return all available effects"""
    return jsonify(nfa.get_all_effects())

@app.route('/ingredients', methods=['GET'])
def get_ingredients():
    """Return all available ingredients with prices"""
    return jsonify({
        ingredient: nfa.ingredient_prices.get(ingredient, 0)
        for ingredient in nfa.all_ingredients
    })

if __name__ == '__main__':
    # app.run(debug=True)
    serve(app, host='0.0.0.0', port=5000)