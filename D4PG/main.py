
import os
import sys
# include modules
utils_ = "/".join(os.getcwd().split("/")[:-1]) + '/utils'
airgym_ = "/".join(os.getcwd().split("/")[:-1]) + '/nimbus_airgym'
sys.path.append(utils_)
sys.path.append(airgym_)
import pyglet
import threading
import tensorflow as tf
import time

from Agent import Agent
from QNetwork import QNetwork
from ExperienceBuffer import ExperienceBuffer

import GUI
import Saver
import Displayer

from settings import Settings


################################################################################
#                                    DEBUG                                     #
from tensorflow.python.client import timeline
# tf.session, A class for running TensorFlow operations.
# A Session object encapsulates the environment in which Operation objects are executed, and Tensor objects are evaluated.
class Sess(tf.Session):
    def __init__(self, options, meta, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.op = options
        self.meta = meta
    def run(self, *args, **kwargs):
        return super().run(options=self.op, run_metadata=self.meta, *args, **kwargs)
#                                                                              #
################################################################################

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
if __name__ == '__main__':

    tf.reset_default_graph()

################################################################################
#                                    DEBUG                                     #
    # options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
    # meta = tf.RunMetadata()
    # config = tf.ConfigProto(log_device_placement=True,
    #                       device_count={"CPU:12", "GPU:1"},
    #                       inter_op_parallelism_threads=10)

    # with Sess(options, meta, config=config) as sess:
#                                                                              #
################################################################################

            # sess  : the main tensorflow session in which to create the networks
            # saver : a Saver instance to save the network weights
            # buffer: the buffer that keeps the experiences to learn from

    with tf.Session(config=config) as sess:
    #with tf.Session() as sess:

        saver = Saver.Saver(sess)
        displayer = Displayer.Displayer()
        buffer = ExperienceBuffer()

        gui = GUI.Interface(['ep_reward', 'plot', 'render', 'gif', 'save'])
        gui_thread = threading.Thread(target=gui.run)

        threads = []
        # create agents for each cpu core we have available
        for i in range(Settings.NB_ACTORS):
            agent = Agent(sess, i, gui, displayer, buffer)
            threads.append(threading.Thread(target=agent.run))

        # with tf.device('/device:GPU:0'):
        learner = QNetwork(sess, gui, saver, buffer, displayer)
        threads.append(threading.Thread(target=learner.run))

        if not saver.load():
            sess.run(tf.global_variables_initializer())

        gui_thread.start()
        for t in threads:
            t.start()

        print("Running...")

        try:
            while not gui.STOP:
                time.sleep(1)

        except KeyboardInterrupt:
            pass

        for t in threads:
            t.join()

################################################################################
#                                    DEBUG                                     #
        # f_t = timeline.Timeline(meta.step_stats)
        # chrome_trace = f_t.generate_chrome_trace_format()
        # with open("timeline.json", 'w') as f:
        #     f.write(chrome_trace)
#                                                                              #
################################################################################

        saver.save(learner.total_eps)
        displayer.disp()

        gui_thread.join()
