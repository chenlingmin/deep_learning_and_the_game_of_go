# tag::train_generator_imports[]
from multiprocessing import freeze_support

from keras.src import Sequential
from keras.src.layers import Dense
from keras.src.optimizers.optimizer_v1 import rmsprop

from dlgo.data.parallel_processor import GoDataProcessor
from dlgo.encoders.oneplane import OnePlaneEncoder
from dlgo.encoders.sevenplane import SevenPlaneEncoder
from dlgo.encoders.simple import SimpleEncoder

from dlgo.networks import small, large
# from keras.layers import S
# from keras.models import Sequential
# from keras.layers import Dense
from keras.callbacks import ModelCheckpoint  # <1>

def main():

    # <1> With model checkpoints we can store progress for time-consuming experiments
    # end::train_generator_imports[]

    # tag::train_generator_generator[]
    go_board_rows, go_board_cols = 19, 19
    num_classes = go_board_rows * go_board_cols
    num_games = 1000

    encoder = SimpleEncoder((go_board_rows, go_board_cols))  # <1>

    processor = GoDataProcessor(encoder=encoder.name())  # <2>

    generator = processor.load_go_data('train', num_games, use_generator=True)  # <3>
    test_generator = processor.load_go_data('test', num_games, use_generator=True)

    # <1> First we create an encoder of board size.
    # <2> Then we initialize a Go Data processor with it.
    # <3> From the processor we create two data generators, for training and testing.
    # end::train_generator_generator[]

    # tag::train_generator_model[]
    input_shape = (encoder.num_planes, go_board_rows, go_board_cols)
    network_layers = small.layers(input_shape)
    model = Sequential()
    for layer in network_layers:
        model.add(layer)
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy',  metrics=['accuracy'])
    # end::train_generator_model[]

    # tag::train_generator_fit[]
    epochs = 50
    batch_size = 128
    model.fit(generator.generate(batch_size, num_classes),  # <1>
                        epochs=epochs,
                        steps_per_epoch=generator.get_num_samples() / batch_size,  # <2>
                        validation_data=test_generator.generate(batch_size, num_classes),  # <3>
                        validation_steps=test_generator.get_num_samples() / batch_size,  # <4>
                        callbacks=[ModelCheckpoint('../checkpoints/small_model_epoch_{epoch}.h5')]
              )  # <5>

    model.evaluate(test_generator.generate(batch_size, num_classes),
                             steps=test_generator.get_num_samples() / batch_size)  # <6>
    # <1> We specify a training data generator for our batch size...
    # <2> ... and how many training steps per epoch we execute.
    # <3> An additional generator is used for validation...
    # <4> ... which also needs a number of steps.
    # <5> After each epoch we persist a checkpoint of the model.
    # <6> For evaluation we also speficy a generator and the number of steps.
    # end::train_generator_fit[]

if __name__ == '__main__':
    freeze_support()
    main()

