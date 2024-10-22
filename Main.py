from flask import Flask, request, jsonify, send_file
from processor import binary_to_image
import os
import io
import requests

app = Flask(__name__)


# Endpoint to accept binary data and return generated image with suggestions
@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()

    # Check if 'binary_data' key is in the request data
    if 'binary_data' not in data:
        return jsonify({"error": "Missing 'binary_data' in request."}), 400

    binary_data = data['binary_data']

    # Validate binary data (ensure it's a list of strings)
    if not isinstance(binary_data, list) or not all(isinstance(row, str) for row in binary_data):
        return jsonify({"error": "Invalid binary data format. Must be a list of strings."}), 400

    # Output image file name
    output_file = "generated_image.png"

    # Convert binary data to image
    binary_to_image(binary_data, output_file)

    # Send the generated image to the suggestion model
    suggestion_response = get_drawing_suggestions(output_file)

    # Clean up the generated image file
    if os.path.exists(output_file):
        os.remove(output_file)

    # Return the suggestions along with success response
    return jsonify(suggestion_response)


def get_drawing_suggestions(image_file):
    # URL of your suggestion model's API
    suggestion_api_url = 'http://127.0.0.1:8080/suggest'  # Replace with actual URL

    # Open the image file and send it to the suggestion model
    with open(image_file, 'rb') as img:
        files = {'image': img}
        response = requests.post(suggestion_api_url, files=files)

    # Return the JSON response from the suggestion model
    if response.status_code == 200:
        return response.json()  # Assumes the suggestion model returns a JSON response
    else:
        return {"error": "Failed to get suggestions from the model."}


if __name__ == "__main__":
    app.run(debug=True)
