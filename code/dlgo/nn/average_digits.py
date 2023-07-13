import numpy as np

from dlgo.nn.layers import sigmoid_double
from dlgo.nn.load_mnist import load_data


def average_digit(data, digit):
    filtered_data = [x[0] for x in data if np.argmax(x[1]) == digit]
    filtered_array = np.asarray(filtered_data)
    return np.average(filtered_array, axis=0)


train, test = load_data()
avg_eight = average_digit(train, 8)

from matplotlib import pyplot as plt

img = (np.reshape(avg_eight, (28, 28)))
plt.imshow(img)
plt.show()

# tag::eval_eight[]
x_3 = train[2][0]  # <1>
x_18 = train[17][0]  # <2>

W = np.transpose(avg_eight)
print(np.dot(W, x_3))  # <3>
print(np.dot(W, x_18))  # <3>


def predict(x, W, b):
    return sigmoid_double(np.dot(W, x) + b)


b = -45

print(predict(x_3, W, b))
print(predict(x_18, W, b))


def evaluate(data, digit, threshold, W, b):
    total_samples = 1.0 * len(data)
    correct_predications = 0
    for x in data:
        if (predict(x[0], W, b) > threshold and np.argmax(x[1]) == digit):
            correct_predications += 1
        if (predict(x[0], W, b) <= threshold and np.argmax(x[1]) != digit):
            correct_predications += 1
    return correct_predications / total_samples


print(evaluate(data=train, digit=8, threshold=0.5, W=W, b=b))
print(evaluate(data=test, digit=8, threshold=0.5, W=W, b=b))

eight_test = [x for x in test if np.argmax(x[1]) == 8]
print(evaluate(data=eight_test, digit=8, threshold=0.5, W=W, b=b))

