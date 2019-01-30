
from multiprocessing import cpu_count
# how many cores?

class Settings:

    ###########################################################################
    # Environment settings

    ENV = "NimbusEnv-v0"

    LOAD    = True
    DISPLAY = True
    GUI     = True

    TRAINING_EPS  = 1000

    MAX_EPISODE_STEPS = 40
    FRAME_SKIP        = 0
    EP_ELONGATION     = 10


    ###########################################################################
    # Network settings


    CONV_LAYERS = [
                    {'filters': 32, 'kernel_size': [8, 8], 'strides': [4, 4]},
                    {'filters': 64, 'kernel_size': [4, 4], 'strides': [2, 2]},
                    {'filters': 64, 'kernel_size': [3, 3], 'strides': [1, 1]}
                  ]

    HIDDEN_ACTOR_LAYERS  = [8, 8, 8]
    HIDDEN_CRITIC_LAYERS = [8, 8, 8]

    NB_ATOMS             = 51 # number of atoms
    ACTOR_LEARNING_RATE  = 5e-4
    CRITIC_LEARNING_RATE = 5e-4


    ###########################################################################
    # Algorithm hyper-parameters

    NB_ACTORS = 1  # cpu_count() - 2

    DISCOUNT      = 0.99
    N_STEP_RETURN = 5
    DISCOUNT_N    = DISCOUNT ** N_STEP_RETURN

    MIN_Q = -2000
    MAX_Q = 2000

    BUFFER_SIZE = 100000
    BATCH_SIZE  = 64

    UPDATE_TARGET_FREQ = 1
    UPDATE_TARGET_RATE = 0.05

    UPDATE_ACTORS_FREQ = 1


    ###########################################################################
    # Exploration settings

    NOISE_SCALE = 0.3
    NOISE_DECAY = 0.99


    ###########################################################################
    # Features frequencies

    EP_REWARD_FREQ = 50
    PLOT_FREQ      = 100
    RENDER_FREQ    = 1000
    GIF_FREQ       = 2000
    SAVE_FREQ      = 1000
    PERF_FREQ      = 100


    ###########################################################################
    # Save settings

    RESULTS_PATH = 'results/'
    MODEL_PATH   = 'model/'
    GIF_PATH     = 'results/gif/'
    MAX_NB_GIF   = 5


    ###########################################################################

    import gym
    setting_env = gym.make(ENV)

    if 'CONV_LAYERS' in locals(): # locals returns a dict of the local namespace
    #     STATE_SIZE = [84, 84, 4]
    # else:
        STATE_SIZE  = list(setting_env.observation_space.shape)
        #FIRST_TENSOR_SIZE = [None, STATE_SIZE]
    # these are of type https://github.com/openai/gym/blob/master/gym/spaces/box.py
    # meaning that they are probability distribution
    # example right here https://github.com/alibaba/gym-starcraft/blob/master/gym_starcraft/envs/single_battle_env.py
    ACTION_SHAPE = list(setting_env.action_space.shape)
    ACTION_SIZE = setting_env.action_space.shape[1]
    LOW_BOUND   = setting_env.action_space.low
    HIGH_BOUND  = setting_env.action_space.high

    del setting_env
