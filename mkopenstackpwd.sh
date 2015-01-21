#!/bin/bash

RABBIT_PASS=$(openssl rand -base64 24)
KEYSTONE_DBPASS=$(openssl rand -base64 24)
ADMIN_TOKEN=$(openssl rand -base64 24)
ADMIN_PASS=$(openssl rand -base64 24)
GLANCE_DBPASS=$(openssl rand -base64 24)
GLANCE_PASS=$(openssl rand -base64 24)
NOVA_DBPASS=$(openssl rand -base64 24)
NOVA_PASS=$(openssl rand -base64 24)
DASH_DBPASS=$(openssl rand -base64 24)
CINDER_DBPASS=$(openssl rand -base64 24)
CINDER_PASS=$(openssl rand -base64 24)
NEUTRON_DBPASS=$(openssl rand -base64 24)
NEUTRON_PASS=$(openssl rand -base64 24)
HEAT_DBPASS=$(openssl rand -base64 24)
HEAT_PASS=$(openssl rand -base64 24)
CEILOMETER_DBPASS=$(openssl rand -base64 24)
CEILOMETER_PASS=$(openssl rand -base64 24)

echo "RABBIT_PASS=\"${RABBIT_PASS}\""
echo "KEYSTONE_DBPASS=\"${KEYSTONE_DBPASS}\""
echo "ADMIN_TOKEN=\"${ADMIN_TOKEN}\""
echo "ADMIN_PASS=\"${ADMIN_PASS}\""
echo "GLANCE_DBPASS=\"${GLANCE_DBPASS}\""
echo "GLANCE_PASS=\"${GLANCE_PASS}\""
echo "NOVA_DBPASS=\"${NOVA_DBPASS}\""
echo "NOVA_PASS=\"${NOVA_PASS}\""
echo "DASH_DBPASS=\"${DASH_DBPASS}\""
echo "CINDER_DBPASS=\"${CINDER_DBPASS}\""
echo "CINDER_PASS=\"${CINDER_PASS}\""
echo "NEUTRON_DBPASS=\"${NEUTRON_DBPASS}\""
echo "NEUTRON_PASS=\"${NEUTRON_PASS}\""
echo "HEAT_DBPASS=\"${HEAT_DBPASS}\""
echo "HEAT_PASS=\"${HEAT_PASS}\""
echo "CEILOMETER_DBPASS=\"${CEILOMETER_DBPASS}\""
echo "CEILOMETER_PASS=\"${CEILOMETER_PASS}\""
