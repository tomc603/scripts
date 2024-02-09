#!/usr/bin/env bash
files=("/etc/nftables.conf" "/etc/keepalived/keepalived.conf" "/etc/systemd/network/10-lan0.network" "/etc/bind/named.conf.options" "/etc/bind/named.conf.default-zones")
services=("nftables.service" "named.service" "nut-monitor.service")
old_net="${1}"
new_net="${2}"

if [[ -z ${old_net} ]] || [[ -z ${new_net} ]]; then
    echo "You need to define and old and new network"
    exit 1
fi

sed -i  "s/${old_net}/${new_net}/g" "${files[@]}"

echo "Reloading network config"
sudo networkctl reload

for svc in "${services[@]}"; do
    echo "Restarting ${svc}"
    systemctl restart "${svc}"
done

