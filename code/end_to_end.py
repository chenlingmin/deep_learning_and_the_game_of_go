from multiprocessing import freeze_support

import h5py
from keras import Sequential
from keras.src.layers import Dense

from dlgo.agent.predict import DeepLearningAgent, load_prediction_agent
from dlgo.data import GoDataProcessor
from dlgo.encoders.sevenplane import SevenPlaneEncoder
from dlgo.httpfrontend import get_web_app
from dlgo.networks import large, small


def main():

    go_board_rows, go_board_cols = 19, 19
    nb_classes = go_board_rows * go_board_cols
    encoder = SevenPlaneEncoder((go_board_rows, go_board_cols))
    processor = GoDataProcessor(encoder=encoder.name())

    X, y = processor.load_go_data(num_samples=200)

    input_shape = (encoder.num_planes, go_board_rows, go_board_cols)
    model = Sequential()
    network_layers = small.layers(input_shape)
    for layer in network_layers:
        model.add(layer)
    model.add(Dense(nb_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit(X, y, batch_size=128, epochs=10, verbose=1)

    deep_learning_bot = DeepLearningAgent(model, encoder)
    deep_learning_bot.serialize(h5py.File("deep_bot.h5", "w"))

    model_file = h5py.File("deep_bot.h5", "r")
    bot_from_file = load_prediction_agent(model_file)

    web_app = get_web_app({'predict': bot_from_file})
    web_app.run()


if __name__ == '__main__':
    freeze_support()
    main()

