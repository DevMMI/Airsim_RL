from setuptools import setup
import os

setup(
    name = "nimbus_airsim",
    version = "1.0",
    author = "Mohamed Isse",
    author_email = "MiMohamud012@gmail.com",
    description = ("Integration of AirSim as OpenAI Gym enviroment for reinforcement learning"),
    license = "MIT",
    keywords = "reinforcement learning, AirSim, OpenAI GYM, Gym",
    url = "https://github.com/DevMohamedMI/Airsim_RL",
    install_requires=['keras=2.2.4'],
    extras_require={
          'gym': ['gym'],
      }
)
