from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import Image, ImageGrab
from io import BytesIO
import numpy as np
import base64

last_frame = None

class ScreenshareHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global last_frame

        if last_frame is not None:
            # Set the headers for a multipart response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes(last_frame, "utf8"))  
        # Set bbox to None to capture the full screen
        bbox = None

        # Capture a frame from the screen
        image = np.array(ImageGrab.grab(bbox=bbox))

        # Resize the image to 320x200 pixels
        image = Image.fromarray(image).resize((320, 200))

        # Convert the image to a JPEG byte buffer
        buffer = BytesIO()
        image.save(buffer, 'JPEG')
        buffer.seek(0)

        # Convert the JPEG byte buffer to a base64 string
        last_frame = base64.b64encode(buffer.getvalue()).decode('utf-8')

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, ScreenshareHandler)
    print('Server running at http://localhost:8000/')
    httpd.serve_forever()