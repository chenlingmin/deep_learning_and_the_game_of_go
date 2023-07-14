import keras

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
# import tensorflow as tf

# tf.config.set_visible_devices([], 'GPU')

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

x_train /= 255
x_test /= 255

y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)
# end::mnist_mlp_preprocessing[]

model = Sequential()
model.add(Dense(392, activation='relu', input_shape=(784,)))
model.add(Dense(196, activation='relu'))
model.add(Dense(98, activation='relu'))
model.add(Dense(49, activation='relu'))
model.add(Dense(10, activation='relu'))
model.summary()

model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=128, epochs=20)
score = model.evaluate(x_test, y_test)

print('Test loss:', score[0])
print('Test accuracy:', score[1])
