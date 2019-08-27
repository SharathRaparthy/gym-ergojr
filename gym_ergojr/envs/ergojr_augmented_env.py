import gym
import gym_ergojr
# from gym_ergojr.envs.ergo_reacher_augmented import ErgoReacherAugmentedEnv
# from gym_ergojr.models.networks import LstmNetRealv1
# class ErgojrAugmentedEnv(ErgoReacherAugmented):
#     def __init__(self):
#
#         HIDDEN_NODES = 128
#         LSTM_LAYERS = 3
#         model = LstmNetRealv1(
#                 n_input_state_sim=12,
#                 n_input_state_real=12,
#                 n_input_actions=6,
#                 nodes=HIDDEN_NODES,
#                 layers=LSTM_LAYERS)
#         model_path = '/home/sharath/neural_augmented_simulator/trained_models/ErgoReacher-Headless-MultiGoal-Halfdisk-v1.pt'
#
#         ErgoReacherAugmented.__init__(self,  model, model_path, headless=False, simple=False, backlash=False, max_force=1, max_vel=18, goal_halfsphere=False, multi_goal=False, goals=3, gripper=True)


env = gym.make("ErgoReacherAugmented-Headless-MultiGoal-Halfdisk-v1")
obs = env.reset()
for step in range(3):
    actions = env.action_space.sample()
    obs, reward, done, _ = env.step(actions)