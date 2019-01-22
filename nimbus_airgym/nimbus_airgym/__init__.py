from gym.envs.registration import register

register(
    id='NimbusEnv-v0',
    entry_point='nimbus_airgym.envs:ForestEnv',
)

