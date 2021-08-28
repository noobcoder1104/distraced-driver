import numpy as np
import io
from PIL import Image
import keras
import base64
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from flask import request
from flask import jsonify
from flask import Flask, render_template
import re
from werkzeug.utils import secure_filename
import operator
import os

app = Flask(__name__)

def get_model():
	global model
	model = load_model('_weights.h5')
	print("Model is loaded Successfully!")

#This function resizeses the image and convert it into a valid dimension for neural network
def preprocess_image(img, tSize):
	if img.mode != "RGB": img = img.convert("RGB")
	img = img_to_array(img.resize(tSize))
	img = np.expand_dims(img, axis=0)
	return img/255

# this function converts the image into a valid format
def convertImage(imgData1):
	imgstr = re.search(r'base64,(.*)',imgData1).group(1)
	with open('output.png','wb') as output:
		output.write(imgstr.decode('base64'))

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/parth")
def test():
	return ("dir:-"+os.getcwd())


@app.route("/predict", methods=["POST"])
def predict():
	encodedFile = request.files['img_form']
	encodedFile.save(secure_filename(encodedFile.filename))
	image = load_img(encodedFile.filename, target_size=(150,150))
	image_arr = img_to_array(image) # converts the PIL Image to NumPy array image
	image_arr = (np.expand_dims(image_arr, axis=0))/255
	class_labels_list = ['safe_driving', 'texting_right', 'talking_on_phone_right', 'texting_left', 'talking_on_phone_left',
                'operating_radio', 'drinking', 'reaching_behind', 'doing_hair_makeup', 'talking_to_passanger']
	model = load_model('_weights.h5')
	predictions = model.predict(image_arr)
	decoded_predictions = dict(zip(class_labels_list, predictions[0]))
	decoded_predictions = sorted(decoded_predictions.items(), key=operator.itemgetter(1), reverse=True)
	count = 1
	for k, v in decoded_predictions[:1]:
	    print("{}. {}: {:8f}%".format(count, k, v*100))
	    pred = k
	    count+=1

	resp = { 'Prediction': str(pred)}
	os.remove(encoded.filename)
	K.clear_session()
	return jsonify(resp)


