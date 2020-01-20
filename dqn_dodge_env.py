import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adamax
import gym_dodge
import matplotlib.pyplot as plt

EPISODES = 200
score = []
episodes = []
mean_score = []

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))

        model.compile(loss='mse', optimizer=Adamax(lr=self.learning_rate))
        return model

    def memorize(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward

            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


if __name__ == "__main__":
    env = gym.make('Dodge-v0')
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    done = False
    batch_size = 32

    for e in range(EPISODES):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        for time in range(501):
            #env.render()
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])
            agent.memorize(state, action, reward, next_state, done)
            state = next_state
            if done:
                print(f"Episode: {e}, Score: {time}, Epsilon: {agent.epsilon:.2}")
                #print(reward)
                episodes.append(e)
                score.append(time)
                mean_score.append(np.mean(score))
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
    
    #plot results
    cum_average = np.cumsum(score) / (np.arange(1, EPISODES+1))
    np.savetxt("learning_rate.txt", cum_average)
    #plt.bar(episodes, score, label="Reward pro Episode",color='#01cdfe', width=1)
    plt.plot(episodes, cum_average, label="Durchschnittlicher Score", color = '#ffa500', linewidth=2)
    plt.xlabel('Episoden')
    plt.ylabel('Score')
    plt.title("Epsilon Decay geringer")
    plt.legend()
    plt.show()
