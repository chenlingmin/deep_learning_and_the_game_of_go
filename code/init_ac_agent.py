import argparse

import h5py
from keras import Input, Model
from keras.src.layers import ZeroPadding2D, Conv2D, Flatten, Dense

from dlgo import encoders, rl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--board-size', type=int, default=19)
    parser.add_argument('output_file')
    args = parser.parse_args()
    board_size = args.board_size
    output_file = args.output_file

    encoder = encoders.get_encoder_by_name('simple', board_size)

    board_input = Input(shape=encoder.shape(), name='board_input')

    conv1a = ZeroPadding2D((2, 2))(board_input)
    conv1b = Conv2D(64, (5, 5), activation='relu')(conv1a)

    conv2a = ZeroPadding2D((1, 1))(conv1b)
    conv2b = Conv2D(64, (3, 3), activation='relu')(conv2a)

    flat = Flatten()(conv2b)
    processed_board = Dense(512)(flat)

    policy_hidden_layer = Dense(
        512, activation='relu')(processed_board)
    policy_output = Dense(
        encoder.num_points(), activation='softmax')(
        policy_hidden_layer)

    value_hidden_layer = Dense(
        512, activation='relu')(
        processed_board)
    value_output = Dense(1, activation='tanh')(
        value_hidden_layer)

    model = Model(inputs=board_input,
                  outputs=[policy_output, value_output])


    new_agent = rl.ACAgent(model, encoder)
    with h5py.File(output_file, 'w') as outf:
        new_agent.serialize(outf)


if __name__ == '__main__':
    main()
