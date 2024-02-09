#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import glob

d2c_files = glob.glob("sdg/-L_*_d2c.dat")
q2c_files = glob.glob("sdg/-Q_*_q2c.dat")
iops_files = glob.glob("sdg/*_iops_fp.dat")
throughput_files = glob.glob("sdg/*_mbps_fp.dat")

d2c = pd.read_csv(d2c_files[0], sep=" ", header=None)
d2c = d2c.rename(columns={0: "timestamp", 1: "latency"})
d2c_mask = d2c["timestamp"] > 1500
d2c = d2c[d2c_mask]

q2c = pd.read_csv(q2c_files[0], sep=" ", header=None)
q2c = q2c.rename(columns={0: "timestamp", 1: "latency"})
q2c_mask = q2c["timestamp"] > 1500
q2c = q2c[q2c_mask]

iops = pd.read_csv(iops_files[0], sep=" ", header=None)
iops = iops.rename(columns={0: "timestamp", 1: "iops"})
iops_mask = iops["timestamp"] > 1500
iops = iops[iops_mask]

throughput = pd.read_csv(throughput_files[0], sep=" ", header=None)
throughput = throughput.rename(columns={0: "timestamp", 1: "mbps"})
throughput_mask = throughput["timestamp"] > 1500
throughput = throughput[throughput_mask]

print(q2c["latency"].min(), q2c["latency"].quantile(q=0.5), q2c["latency"].quantile(q=0.75),
      q2c["latency"].quantile(q=0.90), q2c["latency"].quantile(q=0.95), q2c["latency"].quantile(q=0.99),
      q2c["latency"].quantile(q=0.999), q2c["latency"].quantile(q=0.9999), q2c["latency"].max())

print(q2c[q2c["latency"]>q2c["latency"].quantile(q=0.9999)])


plt.title("Latency and Throughput (sdg)")
plt.subplot(4, 1, 1)
plt.scatter(d2c["timestamp"], d2c["latency"], s=1, marker='.')
plt.subplot(4, 1, 2)
plt.scatter(q2c["timestamp"], q2c["latency"], s=1, marker='.')
plt.subplot(4, 1, 3)
plt.plot(iops["timestamp"], iops["iops"], '.-')
plt.xlabel("time (s)")
plt.ylabel("iops")
plt.subplot(4, 1, 4)
plt.plot(throughput["timestamp"], throughput["mbps"], '.-')
plt.xlabel("time (s)")
plt.ylabel("mbps")

plt.show()
