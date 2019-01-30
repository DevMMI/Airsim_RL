
import tensorflow as tf

from settings import Settings


def build_actor(states, trainable, scope):
    """
    Define an actor network that predicts the best continuous action to perform
    given the current state of an environment.

    Args:
        states   : a tensorflow placeholder to be feeded to get the network output
        trainable: whether the network is to be trained (main network) or to
                    have frozen weights (target network)
        scope    : the name of the tensorflow scope
    """
    with tf.variable_scope(scope):
        #
        layer = states

        # Convolution layers
        if hasattr(Settings, 'CONV_LAYERS') and Settings.CONV_LAYERS:
            for i, layer_settings in enumerate(Settings.CONV_LAYERS):
                layer = tf.layers.conv2d(inputs=layer,
                                         activation=tf.nn.relu,
                                         trainable=trainable,
                                         name='conv_'+str(i),
                                         **layer_settings)

            layer = tf.layers.flatten(layer)

        # Fully connected layers
        for i, nb_neurons in enumerate(Settings.HIDDEN_ACTOR_LAYERS):
            layer = tf.layers.dense(layer, nb_neurons,
                                    trainable=trainable,
                                    activation=tf.nn.relu,
                                    name='dense_'+str(i))

        actions_unscaled = tf.layers.dense(layer, Settings.ACTION_SIZE,
                                           trainable=trainable,
                                           name='dense_last')
        # Bound the actions to the valid range
        valid_range = Settings.HIGH_BOUND - Settings.LOW_BOUND
        actions = Settings.LOW_BOUND + (tf.nn.sigmoid(actions_unscaled) * valid_range)
        print("Shapes b {}".format(actions.shape))
    return actions


def build_critic(states, actions, trainable, reuse, scope, sess):
    """
    Define a critic network that predicts the Q-value of a given state and a
    given action Q(states, actions). This is obtained by feeding the network
    with the concatenation of the two inputs.

    Args:
        states   : a tensorflow placeholder containing the state of the
                    environment
        actions  : a tensorflow placeholder containing the best action
                    according to the actor network
        trainable: whether the network is to be trained (main network) or to
                    have frozen weights (target network)
        reuse    : whether to reuse the weights and biases of an older network
                    with the same scope name
        scope    : the name of the tensorflow scope
    """
    with tf.variable_scope(scope):
        # example feed dict
        # shapes state (1, 144, 256, 1)
        # shapes action (1, 1, 2)
        # shapes reward (1,)
        # shapes next_state (1, 144, 256, 1)
        # shapes not_done (1,)

        # shapes state (3, 144, 256, 1)
        # shapes action (3, 1, 2)
        # shapes reward (3,)
        # shapes next_state (3, 144, 256, 1)
        # shapes not_done (3,)

        # necessary paddings to get actions compatible for concat with state
        print("a state {}".format(states.shape))
        print("a action {}".format(actions.shape))
        actions = tf.expand_dims(actions, 3)
        #actions = tf.expand_dims(actions, 3)
        actions = tf.pad(actions, [[0, 0], [0, 0] , [0, 254], [0, 0]] )
        layer = tf.concat([states, actions], axis=1)

        print("state shape {}, action shape {}".format(states.shape, actions.shape))

        # Convolution layers
        if hasattr(Settings, 'CONV_LAYERS') and Settings.CONV_LAYERS:
            for i, layer_settings in enumerate(Settings.CONV_LAYERS):
                layer = tf.layers.conv2d(inputs=layer,
                                         activation=tf.nn.relu,
                                         reuse=reuse,
                                         trainable=trainable,
                                         name='conv_'+str(i),
                                         **layer_settings)

            layer = tf.layers.flatten(layer)

    # Fully connected layers
        for i, nb_neurons in enumerate(Settings.HIDDEN_CRITIC_LAYERS):
            layer = tf.layers.dense(layer, nb_neurons,
                                    trainable=trainable,
                                    reuse=reuse,
                                    activation=tf.nn.relu,
                                    name='dense_'+str(i))

        q_values = tf.layers.dense(layer, Settings.NB_ATOMS,
                                   trainable=trainable, reuse=reuse,
                                   activation=tf.nn.softmax, name='dense_last')
    return q_values
