import gym
import gym_dodge
import gym
import numpy as np
import matplotlib.pyplot as plt

env = gym.make('Dodge-v0')
env.reset()
score = []
episodes = []
for i_episode in range(1000):
    observation = env.reset()
    for t in range(201):
        #env.render()
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print(f"Score: {t+1}")
            score.append(t+1)
            episodes.append(i_episode)
            break
env.close()

#plot results
cum_average = np.cumsum(score) / (np.arange(1,1000+1))
np.savetxt("random.txt", cum_average)
#plt.bar(episodes, score, label="Reward pro Episode",color='#01cdfe', width=1)
plt.plot(episodes, cum_average, label="Durchschnittlicher Score", color = '#ffa500', linewidth=2)
plt.xlabel('Episoden')
plt.ylabel('Score')
plt.title("Zufällige Aktionen")
plt.legend()
plt.show()