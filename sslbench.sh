#!/usr/bin/env bash

# Host requires the following packages
# sudo apt install linux-generic linux-generic-hwe-20.04 linux-tools-generic linux-tools-generic-hwe-20.04
# sudo apt install lm-sensors i2c-tools fancontrol read-edid intel-cmt-cat libatasmart4 libbson-1.0-0 libopenipmi0 libowcapi-3.2-3 libyajl2 rrdtool librrds-perl libregexp-common-perl libconfig-general-perl 
# sudo apt install collectd --no-install-recommends
declare -a sensor_jobs
declare -a ssl_jobs

LOGPATH="logs"
procs=$(awk -F "-" '{ print $2 }' /sys/devices/system/cpu/online)

if [[ ! -d "${LOGPATH}" ]]; then
    mkdir -p "${LOGPATH}"
fi

# Start host monitors
ipmiwatch.sh &
sensor_jobs+=("$!")
sysfswatch.sh &
sensor_jobs+=("$!")

# Test the powersave and performance CPU governor
for governor in powersave performance; do
  echo "Setting CPU governor to ${governor}."
  echo "${governor}" | sudo tee -a /sys/devices/system/cpu/cpufreq/policy*/scaling_governor
  # for core in $(seq 0 ${procs}); do
  #   openssl speed -seconds 10 &> ${LOGPATH}/openssl-speed.${governor}.${core}.log &
  # done
  openssl speed -multi "${procs}" -seconds 10 &> "${LOGPATH}/openssl-speed.${governor}.multi-${procs}.log" &
  ssl_jobs+=("$!")
  echo "Waiting for test completion..."
  wait "${ssl_jobs[@]}"
done

# Stop up host monitors
echo "Stopping monitors"
for monitor_pid in "${sensor_jobs[@]}"; do
    kill "${monitor_pid[@]}"
done

