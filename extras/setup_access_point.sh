#!/bin/bash

set -e

echo "🔧 Instalando paquetes necesarios..."
sudo apt update
sudo apt install -y hostapd dnsmasq

echo "🛑 Deteniendo servicios temporalmente..."
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

echo "⚙️ Configurando IP fija para wlan0..."
sudo tee -a /etc/dhcpcd.conf > /dev/null <<EOF

interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
EOF

echo "📡 Creando archivo de configuración de hostapd..."
sudo tee /etc/hostapd/hostapd.conf > /dev/null <<EOF
interface=wlan0
driver=nl80211
ssid=RedDomotica
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=clave1234
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF

echo "📁 Enlazando configuración de hostapd..."
sudo sed -i 's|#DAEMON_CONF=""|DAEMON_CONF="/etc/hostapd/hostapd.conf"|' /etc/default/hostapd

echo "🧠 Configurando dnsmasq..."
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo tee /etc/dnsmasq.conf > /dev/null <<EOF
interface=wlan0
dhcp-range=192.168.4.10,192.168.4.40,255.255.255.0,24h
EOF

echo "🔓 Habilitando y reiniciando servicios..."
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq

echo "✅ Reiniciando servicios de red..."
sudo systemctl restart dhcpcd
sudo systemctl restart hostapd
sudo systemctl restart dnsmasq

echo "✅ Access Point configurado correctamente."
echo "📶 Nombre de red: RedDomotica"
echo "🔑 Contraseña:    clave1234"
echo "📡 IP del AP:     192.168.4.1"
echo "🔄 Reiniciando Raspberry Pi en 5 segundos..."

sleep 5
sudo reboot
