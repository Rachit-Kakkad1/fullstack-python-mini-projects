import qrcode
import io
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS # Import the CORS library

# Initialize the Flask app
app = Flask(__name__)

# IMPORTANT: Enable CORS to allow your Netlify frontend 
# to make requests to this backend.
CORS(app)

# The index route is no longer needed, as Netlify will serve the HTML.

@app.route('/generate', methods=['POST'])
def generate_qr():
    """
    Generates the QR code. This is the only endpoint the server needs.
    """
    try:
        data = request.get_json(silent=True)
        if data is None:
             return jsonify({'error': 'Invalid request. No JSON data received.'}), 400

        qr_type = data.get('qr_type')
        fill_color = data.get('fill', '#000000')
        bg_color = data.get('bg', '#FFFFFF')
        
        qr_data_string = ""

        if qr_type == 'wifi':
            ssid = data.get('ssid')
            password = data.get('password')
            if not ssid:
                return jsonify({'error': 'SSID cannot be empty for WiFi QR.'}), 400
            security = "WPA" if password else "nopass"
            qr_data_string = f"WIFI:S:{ssid};T:{security};P:{password if password else ''};;"
        
        elif qr_type == 'url':
            url = data.get('url')
            if not url:
                 return jsonify({'error': 'URL cannot be empty.'}), 400
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            qr_data_string = url

        elif qr_type == 'text':
            qr_data_string = data.get('text')
            if not qr_data_string:
                 return jsonify({'error': 'Text cannot be empty.'}), 400
        else:
            return jsonify({'error': 'Invalid QR Type specified.'}), 400
        
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_data_string)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color=fill_color, back_color=bg_color)
        
        buf = io.BytesIO()
        qr_img.save(buf, format='PNG')
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        data_uri = f"data:image/png;base64,{img_base64}"
        
        return jsonify({'qr_image_uri': data_uri})

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'An unexpected error occurred on the server.'}), 500

# The app.run() part is not needed for production servers like Render.
# They use gunicorn to run the 'app' object directly.
