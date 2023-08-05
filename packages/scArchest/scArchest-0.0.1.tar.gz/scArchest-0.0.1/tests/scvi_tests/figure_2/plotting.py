import json
import os
import matplotlib.pyplot as plt
import numpy as np

x = [538, 1077, 2154, 3231, 4308, 5387]
save_path = os.path.expanduser('~/Documents/benchmark_results/modified/surgery_freeze_exp_freeze/')
with open(save_path + "results.txt") as filehandle:
    m_surgery_exp_freeze = np.array(json.load(filehandle)).T

save_path = os.path.expanduser('~/Documents/benchmark_results/modified/surgery_freeze/')
with open(save_path + "results.txt") as filehandle:
    m_surgery_freeze = np.array(json.load(filehandle)).T

save_path = os.path.expanduser('~/Documents/benchmark_results/modified/only_query/')
with open(save_path + "results.txt") as filehandle:
    m_only_query = np.array(json.load(filehandle)).T

save_path = os.path.expanduser('~/Documents/benchmark_results/base/prediction/')
with open(save_path + "results.txt") as filehandle:
    b_predict = np.array(json.load(filehandle)).T

save_path = os.path.expanduser('~/Documents/benchmark_results/base/only_query/')
with open(save_path + "results.txt") as filehandle:
    b_only_query = np.array(json.load(filehandle)).T

fig, axs = plt.subplots(3, 1)
axs[0].plot(x, m_surgery_exp_freeze[0], label="Modified Surgery EXP F")
axs[0].plot(x, m_surgery_freeze[0], label="Modified Surgery F")
axs[0].plot(x, m_only_query[0], label="Modified Only Query")
axs[0].plot(x, b_predict[0], label="Base Prediction")
axs[0].plot(x, b_only_query[0], label="Base Only Query")
axs[0].set_xlabel('Subsamples')
axs[0].set_ylabel('EBM SCORE')

axs[1].plot(x, m_surgery_exp_freeze[1], label="Modified Surgery EXP F")
axs[1].plot(x, m_surgery_freeze[1], label="Modified Surgery F")
axs[1].plot(x, m_only_query[1], label="Modified Only Query")
axs[1].plot(x, b_predict[1], label="Base Prediction")
axs[1].plot(x, b_only_query[1], label="Base Only Query")
axs[0].set_xlabel('Subsamples')
axs[1].set_ylabel('KNNP SCORE')

axs[2].plot(x, m_surgery_exp_freeze[2], label="Modified Surgery EXP F")
axs[2].plot(x, m_surgery_freeze[2], label="Modified Surgery F")
axs[2].plot(x, m_only_query[2], label="Modified Only Query")
axs[2].plot(x, b_predict[2], label="Base Prediction")
axs[2].plot(x, b_only_query[2], label="Base Only Query")
axs[0].set_xlabel('Subsamples')
axs[2].set_ylabel('ACC SCORE')
plt.legend()
plt.show()
