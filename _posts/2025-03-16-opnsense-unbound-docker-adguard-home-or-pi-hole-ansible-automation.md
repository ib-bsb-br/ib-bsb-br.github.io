---
tags: [scratchpad]
info: aberto.
date: 2025-03-16
type: post
layout: post
published: true
slug: opnsense-unbound-docker-adguard-home-or-pi-hole-ansible-automation
title: 'OPNsense + Unbound + Docker (AdGuard Home or Pi-hole) + Ansible Automation'
---
## Scenario Overview

- **Purpose**: Construct a resilient, robust homelab infrastructure to cover firewall, routing, DHCP, DNS resolution and ad-blocking using proven open-source tools.  
- **Components Integrated**:
  - **OPNsense** — Firewall, Router, DHCP, DNS rebinding protection
  - **Unbound** (integrated within OPNsense) — Local recursive DNS resolver (self-hosted DNS queries)
  - **AdGuard Home OR Pi-hole** (in Docker) — DNS sinkhole (ad-blocking, tracker blocking, DNS-over-HTTPS capability)
  - **Docker** — Lightweight and flexible service encapsulation
  - **Ansible** — Automated infrastructure deployment, backups, and recovery.

---

## STEP 1 - Deploy OPNsense Firewall Router (Bare Metal / Virtual Machine)

### Installation

Download installer from official source:
- Official Image: [https://opnsense.org/download/](https://opnsense.org/download/)  
- Recommendation: latest stable ISO version, amd64 architecture  

Install OPNsense on dedicated hardware or virtualization hypervisor (recommended hypervisors: Proxmox, VMware ESXi, XCP-ng).

### Network Interfaces

- Assign at least two interfaces:
  - `WAN` → ISP modem (public facing)
  - `LAN` → Switch (internal network, client-facing)

Adjust default interface settings to match your network.

---

## STEP 2 - OPNsense Configuration Essentials

Login:  
`https://opnsense-ip` (Web GUI default user: root, password: opnsense)

### LAN Interface Configuration

Example addressing scheme:
- LAN Network: `192.168.10.0/24`  
- OPNsense LAN IP: `192.168.10.1`

Configure at:
- Interfaces → LAN: static IPv4, CIDR `192.168.10.1/24`

### DHCP Server Setup

- In **Services → DHCPv4 → LAN**:
  - Enable DHCPv4 server
  - Range: `192.168.10.100 - 192.168.10.200`
  - Gateway: `192.168.10.1`
  - DNS Server: Will be assigned later (AdGuard Home)

### Firewall Basic Rules (default recommended rules):

- LAN interface → allow LAN to Any via IPv4 (default outbound rule provided by OPNsense)
- WAN interface → default deny incoming, allow responses from LAN initiated traffic (default)

---

## STEP 3 - Unbound DNS Configuration (In OPNsense)

Location: `Services → Unbound DNS`

- Enable Unbound service (**check**)
- DNSSEC Validation (**check**)
- Listen interfaces (**check both**): LAN and Localhost only
- Access Lists: Allowed networks ("192.168.10.0/24")
- Advanced settings (recommended):
```
server:
  cache-max-ttl: 86400
  cache-min-ttl: 300
  num-threads: 2
  outgoing-num-tcp: 10
  incoming-num-tcp: 10
  msg-cache-size: 32m
  rrset-cache-size: 64m
  infra-cache-numhosts: 5000
  infra-host-ttl: 3600
  ratelimit: 1000
```

- Enable DNS rebinding protection (**check**) under System → Settings → Administration → DNS settings ("Enable DNS Rebinding Checks").

---

## STEP 4 - Docker Host Preparation (AdGuard Home or Pi-hole)

Deploy on dedicated physical server or VM, e.g., Ubuntu Server 22.04 LTS:

### Set static IP on Docker host (example):
```
sudo nano /etc/netplan/00-installer-config.yaml
```

Configure static IP:
```yaml
network:
  ethernets:
    ens18:
      dhcp4: false
      addresses: [192.168.10.5/24]
      gateway4: 192.168.10.1
      nameservers:
        addresses: [192.168.10.1]
  version: 2
```

Apply and reboot:
```
sudo netplan apply
sudo reboot
```

### Installing Docker (Ubuntu Example):
```bash
sudo apt update
sudo apt install ca-certificates curl gnupg apt-transport-https software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu jammy stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update
sudo apt install docker-ce docker-ce-cli docker-compose-plugin -y
sudo usermod -aG docker $USER
sudo reboot
```

---

## STEP 5 - Deploy DNS Sinkhole (Pick One)

### OPTION A) AdGuard Home via Docker

Create directories:
```bash
mkdir -p ~/docker/adguard/{work,conf}
```

Launch AdGuard Home via Docker Compose:
```yaml
# ~/docker/adguard/docker-compose.yml
version: '3'
services:
  adguardhome:
    image: adguard/adguardhome:latest
    container_name: adguardhome
    restart: unless-stopped
    network_mode: host
    volumes:
      - ./work:/opt/adguardhome/work
      - ./conf:/opt/adguardhome/conf
```

Deploy:
```
docker compose up -d
```

Web login to AdGuard Home at:  
`http://192.168.10.5:3000`

After setup, change DHCP DNS entry in OPNsense DHCP server to `192.168.10.5`

### OPTION B) Pi-hole via Docker

Create directories:
```bash
mkdir -p ~/docker/pihole/{etc-pihole,etc-dnsmasq.d}
```

Docker Compose YAML (`~/docker/pihole/docker-compose.yml`):
```yaml
version: "3"
services:
  pihole:
    image: pihole/pihole:latest
    container_name: pihole
    restart: unless-stopped
    environment:
      TZ: 'Europe/Berlin'
      WEBPASSWORD: 'StrongPasswordHere'
    ports:
      - "53:53/tcp"
      - "53:53/udp"
      - "80:80/tcp"
    volumes:
      - ./etc-pihole:/etc/pihole
      - ./etc-dnsmasq.d:/etc/dnsmasq.d
```

Start Pi-hole:
```
docker compose up -d
```

Access WebGUI at:  
`http://192.168.10.5/admin`

Set DHCP DNS IP to `192.168.10.5` in OPNsense DHCP server.

---

## STEP 6 - Ansible Infrastructure-as-Code & Backups

Install Ansible (on local PC, Linux):
```
sudo apt install ansible git -y
```

Project Directory structure:
```
homelab-ansible/
├── inventory.yml
├── roles/
│   ├── docker_host/
│   │   └── tasks/main.yml
│   └── opnsense_backup/
│       └── tasks/main.yml
└── site.yml
```

`inventory.yml`:
```yaml
docker_host:
  hosts:
    docker01:
      ansible_host: 192.168.10.5
      ansible_user: youruser
opnsense_host:
  hosts:
    firewall:
      ansible_host: 192.168.10.1
      ansible_user: root
```

`site.yml`:
```yaml
- hosts: docker_host
  roles:
    - docker_host
- hosts: opnsense_host
  roles:
    - opnsense_backup
```

`roles/docker_host/tasks/main.yml`:
```yaml
- name: Copy config files and restart containers
  copy:
    src: ~/docker/
    dest: ~/docker/
  notify: restart docker compose
```

`roles/opnsense_backup/tasks/main.yml` (ex. OPNsense backup):
```yaml
- name: Backup OPNsense config.xml
  fetch:
    src: /conf/config.xml
    dest: backups/firewall_config.xml
```

Run Ansible Playbook (periodically):
```
ansible-playbook -i inventory.yml site.yml
```

---

## STEP 7 - Confirm Final Integration

Clients → DHCP DNS server (`192.168.10.5`) → AdGuard or Pi-hole → Unbound (OPNsense at `192.168.10.1`) → Internet DNS Root servers  

**Backup strategy** — Fully automated via Ansible, consistently reproducible.

Homelab complete and optimized!