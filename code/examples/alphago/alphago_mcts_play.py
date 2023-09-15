from dlgo.agent import load_prediction_agent, load_policy_agent, AlphaGoMCTS
from dlgo.httpfrontend import get_web_app
from dlgo.rl import load_value_agent
import h5py

fast_policy = load_prediction_agent(h5py.File('alphago_sl_policy.h5', 'r'))
strong_policy = load_policy_agent(h5py.File('alphago_rl_policy.h5', 'r'))
value = load_value_agent(h5py.File('alphago_value.h5', 'r'))

alphago = AlphaGoMCTS(strong_policy, fast_policy, value)

web_app = get_web_app({'predict': alphago})
web_app.run()
