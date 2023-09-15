import h5py

from dlgo.encoders import AlphaGoEncoder
from dlgo.networks import alphago_model
from dlgo.rl import load_experience
from dlgo.rl.value import ValueAgent

rows, cols = 19, 19
encoder = AlphaGoEncoder()
input_shape = (encoder.num_planes, rows, cols)
alphago_value_network = alphago_model(input_shape)

alphago_value = ValueAgent(alphago_value_network, encoder)

experience = load_experience(h5py.File('alphago_rl_experience.h5', 'r'))
alphago_value.train(experience)

with h5py.File('alphago_value.h5', 'w') as value_agent_out:
    alphago_value.serialize(value_agent_out)


