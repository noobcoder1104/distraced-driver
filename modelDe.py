import keras
from keras.layers import Dropout, Flatten, Dense

def modelDeDe():
	vgg = keras.applications.vgg16.VGG16(weights='imagenet')

	vgg.layers.pop()
	vgg.layers.pop()
	vgg.layers.pop()
	vgg.layers.pop()

	m = keras.models.Sequential()

	for l in vgg.layers:	m.add(l)

	for _layer in m.layers: 	_layer.trainable = False

	m.add(Flatten())
	m.add(Dense(256, activation='relu'))
	m.add(Dropout(0.5))
	m.add(Dense(10, activation='softmax'))

	return m