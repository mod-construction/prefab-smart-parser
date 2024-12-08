from flask import Flask, request, jsonify
import ParseThatLocal as ParseThat
app = Flask(__name__)


@app.route('/api/parseit_local', methods=['GET'])
def call_function():
   # Get the 'input' parameter from the query string
    input_data = request.args.get('input')
    print(input_data)
    if not input_data:
        return jsonify({"error": "Missing 'input' in query parameters"}), 400

    # Call your function with the input data
    result = ParseThat.wrapper(input_data)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=False, port=5000)  # Runs on http://localhost:5000
