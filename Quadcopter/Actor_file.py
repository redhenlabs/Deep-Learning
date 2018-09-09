# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 00:11:48 2018

@author: shuchowdhury
"""

"""Deep Deterministic Policy Gradients (DDPG)
It is actually an actor-critic method, but the key idea is that the underlying policy function used is deterministic 
in nature, with some noise added in externally to produce the desired stochasticity in actions taken.
"""

from keras import layers, models, optimizers, regularizers
from keras import backend as K

class Actor:
    """Actor (Policy) Model."""

    def __init__(self, state_size, action_size, action_low, action_high):
        """Initialize parameters and build model.

        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            action_low (array): Min value of each action dimension
            action_high (array): Max value of each action dimension
        """
        self.state_size = state_size
        self.action_size = action_size
        self.action_low = action_low
        self.action_high = action_high
        self.action_range = self.action_high - self.action_low

        # Initialize any other variables here

        self.build_model()

    def build_model(self):
        """Build an actor (policy) network that maps states -> actions."""
        # Define input layer (states)
        states = layers.Input(shape=(self.state_size,), name='states')

        # Add hidden layers
        """keras.layers.Dense(units, activation=None, use_bias=True, kernel_initializer='glorot_uniform', 
            bias_initializer='zeros', kernel_regularizer=None, 
            bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)"""
        """
        net = layers.Dense(units=32, activation='relu')(states)
        net = layers.Dense(units=64, activation='relu')(net)
        net = layers.Dense(units=32, activation='relu')(net)
        """
        net = layers.Dense(units=32, activation='relu', use_bias=False, kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01))(states)
        net = layers.BatchNormalization()(net)
#        net = layers.Dropout(0.5)(net)
        net = layers.Dense(units=64, activation='relu', use_bias=False, kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01))(net)
        net = layers.BatchNormalization()(net)
        net = layers.Dropout(0.5)(net)
#        net = layers.Dense(units=128, activation='relu', use_bias=False, kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01))(net)
#        net = layers.Dropout(0.4)(net)
#        net = layers.Dense(units=256, activation='relu', use_bias=False, kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01))(net)
#        net = layers.Dropout(0.5)(net)
#        net = layers.Dense(units=128, activation='relu', use_bias=False, kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01))(net)
#        net = layers.Dropout(0.4)(net)
#        net = layers.Dense(units=64, activation='relu', use_bias=False, kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01))(net)
#        net = layers.Dropout(0.3)(net)
        net = layers.Dense(units=32, activation='relu', use_bias=False, kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01))(net)
        
        #net = layers.Dense(units=32, activation='relu')(states)
#        net = layers.Dense(units=32, use_bias=False, kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01))(states)
#        net = layers.BatchNormalization()(net)
#        net = layers.Activation('relu')(net)
#        net = layers.Dropout(0.5)(net)

        #net = layers.Dense(units=64, activation='relu')(states)
#        net = layers.Dense(units=64, use_bias=False, kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01))(net)
#        net = layers.BatchNormalization()(net)
#        net = layers.Activation('relu')(net)
#        net = layers.Dropout(0.5)(net)
        
        #net = layers.Dense(units=128, activation='relu')(net)
#        net = layers.Dense(units=128, use_bias=False, kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01))(states)
#        net = layers.BatchNormalization()(net)
#        net = layers.Activation('relu')(net)
#        net = layers.Dropout(0.5)(net)
        
        #net = layers.Dense(units=32, activation='relu')(net)
#        net = layers.Dense(units=64, use_bias=False, kernel_regularizer=regularizers.l2(0.01), activity_regularizer=regularizers.l1(0.01))(states)
#        net = layers.BatchNormalization()(net)
#        net = layers.Activation('relu')(net)
#        net = layers.Dropout(0.5)(net)

        # Try different layer sizes, activations, add batch normalization, regularizers, etc.

        # Add final output layer with sigmoid activation
        raw_actions = layers.Dense(units=self.action_size, activation='sigmoid',
            name='raw_actions')(net)

        # Scale [0, 1] output for each action dimension to proper range
        actions = layers.Lambda(lambda x: (x * self.action_range) + self.action_low,
            name='actions')(raw_actions)

        # Create Keras model
        self.model = models.Model(inputs=states, outputs=actions)

        # Define loss function using action value (Q value) gradients
        action_gradients = layers.Input(shape=(self.action_size,))
        loss = K.mean(-action_gradients * actions)

        # Incorporate any additional losses here (e.g. from regularizers)

        # Define optimizer and training function
        optimizer = optimizers.Adam()
        updates_op = optimizer.get_updates(params=self.model.trainable_weights, loss=loss)
        self.train_fn = K.function(
            inputs=[self.model.input, action_gradients, K.learning_phase()],
            outputs=[],
            updates=updates_op)