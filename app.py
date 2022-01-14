from flask import Flask
import cv2 
import pytesseract

app = Flask(__name__)

SECRET_KEY = 'jfdlkajflajfklafjlka'
app.secret_key = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

@app.route('/')
def helloworld():
    img = cv2.imread('1-1.jpeg')
    text = pytesseract.image_to_string(img)
    return "<p>" + text + "</p>"

# Run the app
if __name__ == '__main__':
    app.run()