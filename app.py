from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Store calculation history (in memory)
history = []

@app.route('/')
def index():
    return render_template('index.html', history=history)


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        expression = data['expression']

        # Allow only safe math characters
        allowed = set('0123456789+-*/.() ')
        if not all(c in allowed for c in expression):
            return jsonify({'error': 'Invalid characters!'})

        result = eval(expression)

        # Save history
        history.append(f"{expression} = {result}")
        if len(history) > 10:
            history.pop(0)

        return jsonify({
            'result': result,
            'history': history
        })

    except Exception:
        return jsonify({'error': 'Invalid expression!'})


@app.route('/clear-history', methods=['POST'])
def clear_history():
    global history
    history = []
    return jsonify({'history': history})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)