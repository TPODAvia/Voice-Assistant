import os

model_path = 'D:\\Coding_AI\\venv\\lib\\site-packages\\openwakeword\\resources\\models\\alexa_v0.1.onnx'
if os.path.exists(model_path):
    print("Model file found.")
else:
    print("Model file not found, please check the path.")