---
tags: [scratchpad]
info: aberto.
date: 2025-03-16
type: post
layout: post
published: true
slug: postmarketos-powered-kubernetes-cluster
title: 'postmarketOS-powered Kubernetes cluster'
---
bibref https://blog.denv.it/posts/pmos-k3s-cluster/

Having a few Raspberry Pi 4s at my disposal, I found myself somewhat dissatisfied with their processing capabilities and power management features.
This led me to explore alternative solutions, particularly given the collection of old smartphones gathering dust in my drawer. 
These devices, while outdated for daily use, still pack considerable computing power.
In this article, I'll walk through how I transformed these old smartphones into a functional Kubernetes cluster using postmarketOS, giving them a second life as computing nodes.

<!--more-->

<!-- toc -->

## Introduction

Applications nowadays are getting more resource-intensive. Depending on your use case, some of your homelab services might need a lot of processing power and memory.

Some of my (current and future) workloads include:
- CI/CD pipelines
- Photo library software such as [Immich](https://immich.app/)
    - Resizing / converting images
    - Running face recognition
- [Forgejo](https://forgejo.org/) (Git)
- [Woodpecker CI](https://woodpecker-ci.org/)
- [Vaultwarden](https://github.com/dani-garcia/vaultwarden)
- [Plex](https://plex.tv) / [Jellyfin](https://jellyfin.org/)
- [Docmost](https://github.com/docmost/docmost/)
- [Teslamate](https://github.com/teslamate-org/teslamate)
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/)
- [LobeChat](https://github.com/lobehub/lobe-chat)
- [Vikunja](https://vikunja.io/) (To-Do list)
- [openvscode-server](https://github.com/gitpod-io/openvscode-server)
- ...


Although it's rare that single services are so demanding, certain pipelines or workflows can be quite resource-intensive. 
The solution is usually to scale horizontally - but this can be expensive (in terms of money, amount of devices, power consumption, physical space).
Buying new devices is not the most sustainable solution, especially when you're surrounded by old devices that have a computing power that is comparable or even better than that of your next purchase.

## What are Raspberry Pis good for?

Raspberry Pis excel at running small services and functioning as [appliances](https://gokrazy.org/). Their GPIO capabilities make them perfect for physical computing projects, but as Kubernetes nodes, they have some limitations.

Here are the main challenges I've encountered:
- Physical size: With a case, they're relatively bulky for a computing node
- Power management: One power supply per device is often needed
- Power stability: Multi-port power supplies can be unreliable, causing simultaneous outages across nodes
- Performance: Limited computing power compared to modern mobile processors
- Price: [A Raspberry Pi 5 with 8 GB of RAM](https://www.digitec.ch/en/s1/product/raspberry-pi-new-raspberry-pi-5-8gb-development-boards-kits-38955607) costs around [85 CHF](https://www.xe.com/currencyconverter/convert/?Amount=85&From=CHF&To=USD): there are cheaper and more sustainable solutions

While I have used several Raspberry Pis for other projects (like my wedding photobooth, which I'll detail in another post), their I/O capabilities are often underutilized when serving purely as compute nodes.


## What's so compelling about old smartphones?

On one hand, a Raspberry Pi 4 is a great device for running small services and provides
a very good interface between hardware and software. On the other hand, old smartphones are often discarded due to their outdated software, but they still have a lot of computing power and memory.

Old devices are filling marketplaces and drawers. For a very low price, usually 0 if the device sits in your drawer, you can get a device with an octa-core CPU, 6/8 GB of RAM and 128+ GB of storage.
If you compare this with a Raspberry Pi 4, using an old smarthphone as a computing node could be a good idea.

### Comparison

Here is a small comparison of some of the devices I have at my disposal:

| Device | Year | Cores | Frequencies | RAM | Storage | Storage Type |
|:-------|-----:|----------:|------------:|----:|--------:|--------------|
| [Xiaomi Redmi Note 11 Pro](https://www.gsmarena.com/xiaomi_redmi_note_11_pro_5g-11333.php) | 2022 | 8 | 2x2.2 GHz, 6x1.7 GHz | 4/6/8GB | 64/128GB | UFS 2.2 |
| [Oneplus Nord](https://www.gsmarena.com/oneplus_nord-10289.php) | 2020 | 8 | 1x2.4 GHz, 1x2.2 GHz, 6x1.8 GHz | 6/8/12 GB | 64-256 GB | UFS 2.1 |
| [OnePlus 8 Pro](<https://wiki.postmarketos.org/wiki/OnePlus_8_Pro_(oneplus-instantnoodlep)>) | 2020 | 8 | 1x2.84 GHz, 3x2.42GHz, 4x1.8 GHz | 8/12 GB  | 128/256 GB | UFS 3.0 |
| [Raspberry Pi 4](https://en.wikipedia.org/wiki/Raspberry_Pi_4) | 2019 | 4 | 1.5 GHz| 2-8 GB | External | microSD |
| [OnePlus 5T](<https://wiki.postmarketos.org/wiki/OnePlus_5T_(oneplus-dumpling)>) | 2017 | 8 | 4x 2.45 GHz, 4x1.9 GHz| 6/8 GB | 64/128 GB | UFS 2.1 |


There's also inherent value in using smartphones: they come with built-in batteries that function as UPS (Uninterruptible Power Supply) units, and their integrated displays can serve as dashboard monitors. These features provide additional utility without requiring extra hardware components. You can of course turn off the backlight of the display to save power if you don't need it.


## What's bad about Linux on smartphones?

### No support for mainline Linux

Most of the Android smartphones out there have poor support for _mainline_ Linux. The kernel running on the average Android device is generally a heavy customized
version of the Linux kernel. This makes things complicated, and reduces security and performance.  
  
While this is not a problem of the smartphones per se, it's going to be a problem if you intend to use them as Kubernetes nodes, or use them for anything else that's not Android.  

### Unlocking the bootloader can be... tricky

> [!WARNING]  
> Unlocking the bootloader will delete all your data. Do not run the following commands if you haven't backed up your data.

Not all the devices can be unlocked easily. While some manufacturers allow you to `fastboot oem unlock` your device directly, others require you to perform long processes to unlock the bootloader, and sometimes you can't unlock it at all.  
  
If you're about to buy an used device for this purpose, make sure the brand is known for allowing bootloader unlocking.  
  
To save you some time, try to generally avoid:
- Xiaomi
    - Unlocking the bootloader takes from 7 to 30 days to unlock
    - During this time, you need to keep the same Xiaomi account connected to the device,
    - You'll have to use a Xiaomi-provided application... but [there are alternatives](https://github.com/topminipie/awesome-xiaomi-bootloader-unlock)
- Huawei / Honor
    - You can't unlock the bootloader anymore

... and prefer:

- Google
- OnePlus
- FairPhone

See a complete list on [Bootloader Unlock Wall Of Shame](https://github.com/melontini/bootloader-unlock-wall-of-shame).


### GPL is not always respected

The Linux kernel is licensed under the GPL, which means that if you modify it, you have to share your modifications.  
Despite this, many manufacturers are slow to release the kernel sources, or don't release them at all.

One example of this is [Xiaomi](https://github.com/MiCode/Xiaomi_Kernel_OpenSource/issues) ([HN discussion](https://news.ycombinator.com/item?id=35184859)), 
which has been criticized for not releasing the kernel sources for some of their devices.

### Your device is not supported

This is not really a problem caused by anyone really, there will always be a device that is not supported by the community - and sometimes _you_ will be the one
that has to put in the legwork to make it work.  

I'm by no means a kernel expert, but I've tried this road [a couple](https://github.com/pixelc-linux/documentation) [of times](https://github.com/linux-surface/surface-pro-x/issues?q=author%3Adenysvitali) - and, while it might be challenging, it's a very rewarding process and you get to learn a lot about how these devices work. 
In the next sections you'll see what I mean by this.  
  
Despite this, you can still play it safe and buy an used device that is already (partially) [supported by the community](https://wiki.postmarketos.org/wiki/Devices).  
  
Before you complain about the lack of support for your device: make sure to also check the "Testing" section of the [postmarketOS Devices](https://wiki.postmarketos.org/wiki/Devices) page:
it's easy to miss that part and might sound scary, but a "testing" device is generally just a device that doesn't have full support for all the features and that doesn't have a ready to use firmware image. With [`pmbootstrap`](https://docs.postmarketos.org/pmbootstrap/usage.html) setting up an already upstreamed testing device is really a breeze!

## What is postmarketOS?

Okay, we mentioned it a couple of times already, but I didn't explain what the heck [postmarketOS](https://postmarketos.org/) is: the shortest way to describe it is by saying that it's a rolling Linux distribution for smartphones based on [Alpine Linux](https://alpinelinux.org/).  
  
The interesting part of this distribution is that _it's meant to be run with the mainline Linux kernel_. This effectively means that postmarketOS is not just another Android ROM: it is the key to the long-term support of the devices.
  
Whilst I haven't seen anyone (yet) really using pmOS as a daily driver, and I myself am not doing that either (I'm using [GrapheneOS](https://grapheneos.org/)).  
  
Being a Linux distribution based on Alpine, you can really use your smartphone as if it's a computer (or in my case, a server): this means that you can install for example [sway](https://swaywm.org/), [KDE](https://kde.org/) or literally [any other desktop environment / user interfaces](https://wiki.postmarketos.org/wiki/Category:Interface) you want and run your favorite applications.  

## State of Linux on ARM
  
With the ["recent" Apple Silicon push](https://en.wikipedia.org/wiki/Apple_M1) and the amazing work of [aarch64-laptops](https://github.com/aarch64-laptops) / [Linaro](https://www.linaro.org/) ([thanks](https://old.linaro.org/blog/porting-linux-to-aarch64-laptops/) Bjorn & team!), Linux on ARM is growing fast and it's supported by many distros / forks (such as [Arch Linux ARM](https://archlinuxarm.org/), [Alpine Linux](https://wiki.alpinelinux.org/wiki/Alpine_on_ARM), [Debian](https://wiki.debian.org/Arm64Port#Official_Debian_port), ...) - so using a smartphone as a server / computer is not that crazy anymore as mobile devices aren't that different from (new) laptops anymore.  
  
There are still a few assumptions made by some software distributors (especially Docker Images) where they assume that you're running on `x86_64`, but this is getting better and better, especially given the "recent" additions of [multi-platform builds](https://docs.docker.com/build/building/multi-platform/) on Docker.

If that's your thing, you can also connect a mouse, keyboard (and monitor) to your device and use it as a desktop computer.


## Setting up a node

### Lessons learned

Before I start with the details, I want to immediately share some lessons learned - so that you can avoid some of the mistakes I made:

- **Don't spend half a day debugging `iptables`**: postmarketOS comes with `nftables` and the default rules in `/etc/nftables.nft` are the reason why your Kubernetes network might get messed up

- Docker, Kubernetes and K3s require some kernel modules / configs to be enabled:
    - Try to run a Docker container first, and eventually use [moby's `check-config.sh`](https://github.com/moby/moby/blob/master/contrib/check-config.sh)

    - Use [k3s's `check-config.sh`](https://github.com/k3s-io/k3s/blob/master/contrib/util/check-config.sh) to check if your kernel is ready. In my case ([`dumpling`](https://wiki.postmarketos.org/wiki/OnePlus_5T_(oneplus-dumpling)) was missing some kernel configs, but [`instantnoodlep`](https://wiki.postmarketos.org/wiki/OnePlus_8_Pro_(oneplus-instantnoodlep)) was fine)

    - Kubernetes doesn't come with a `check-config.sh` file - but your Container Network Interface (CNI) might require some kernel features that Docker / K3s don't need. In the case of Flannel, make sure you have most / all the `CONFIG_NETFILTER_XTABLES` options enabled in your kernel, as well as `CONFIG_VXLAN`.

### OnePlus 5T (dumpling)

According to the [postmarketOS wiki](https://wiki.postmarketos.org/wiki/OnePlus_5T_(oneplus-dumpling)), the OnePlus 5T is a "testing" device, which means that it's not fully supported yet. Despite this, I was able to run postmarketOS on it without any issue.  
  
The most important features for me (Wi-Fi) and USB ethernet worked out of the box.

If, like me, this is your first time running postmarketOS - one nice feature is that they support USB ethernet out of the box. Initially, I thought this meant supporting an USB to Ethernet adapter, but it actually means that you can connect your smartphone to your computer, and this will be recognized as an USB ethernet device.  
  
```plain
% ip addr show enp0s20f0u1
149: enp0s20f0u1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether ca:fe:ba:be:00:42 brd ff:ff:ff:ff:ff:ff
    inet 172.16.42.2/24 brd 172.16.42.255 scope global dynamic noprefixroute enp0s20f0u1
       valid_lft 3628776sec preferred_lft 3628776sec
    inet6 fe80::504a:1ee0:5015:da8d/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
```

With this, you can simply SSH into your device and start working on it:
  
```bash
$ ssh root@172.16.42.1
Welcome to postmarketOS! o/

This distribution is based on Alpine Linux.
First time using postmarketOS? Make sure to read the cheatsheet in the wiki:

-> https://postmarketos.org/cheatsheet

You may change this message by editing /etc/motd.
dumpling:~#
```
  


> [!TIP]  
> For whatever reason, after many tries, I started using the wrong IP (`172.16.42.2`) to SSH into the device and got confused on why it wasn't accepting my device password anymore. Don't be as dumb as me and double check the IP you're `ssh`ing into, which should be `172.16.42.1`.


#### Connecting the device to the Wi-Fi

Now that you're able to connect to the device, you should be able to see `wlan0` as an interface:

```bash
$ ip addr show wlan0
4: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP qlen 1000
    link/ether 02:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff
```

this means that you're ready to connect to your Wi-Fi network!

You can check the list of Wi-Fi networks with [NetworkManager](https://wiki.archlinux.org/title/NetworkManager)'s CLI:

```bash
$ nmcli d wifi
IN-USE  BSSID              SSID                   MODE   CHAN  RATE        SIGNAL  BARS  SECURITY
        00:00:00:00:00:00  MyNetwork              Infra  1     54 Mbit/s  100     ▂▄▆█  WPA2
```

If you want to connect to a network, you can use the following command:

```bash
nmcli d wifi connect MyNetwork --ask
```

this assumes that the network is visible, and it will ask you for the password.

If you want to connect to a hidden network, you can use the following command:

```bash
HIDDEN_SSID="your_ssid"
nmcli d wifi connect --ask "$HIDDEN_SSID" name "$HIDDEN_SSID" hidden yes
```

If everything went well, NetworkManager will tell you that you're connected to the network:

```plain
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/1)
```

#### Using the device as a Kubernetes node

> [!IMPORTANT]
> This part shows how the process of setting up Kubernetes on `dumpling` should look like - unfortunately this isn't exactly how it should be done as of today. Do not follow all these steps blindly - read the full section first :)


Since our goal is to use this device as a Kubernetes node, we'll have to configure the device accordingly. In my setup, I'll be using [k3s](https://k3s.io/), a lightweight Kubernetes distribution that is perfect for low-resource devices.  
  
This part assumes that you've already setup the master node(s) somewhere else, but if you want this to be the master node, you can adapt my steps and follow the [documentation](https://docs.k3s.io/installation/configuration).

Assuming:
- A master node with the IP `192.168.10.11`
- A token to join the cluster `000000::server::f0000`

##### Installing `k3s`

If you haven't done so during the pmOS wizard, you can `apk add k3s` to install k3s on your device.

##### Configuring `k3s` agent

Create an `/etc/rancher/k3s/config.yaml` file as follows:

```yaml
token: "000000::server::f0000"
server: "https://192.168.10.11:6443"
prefer-bundled-bin: true
flannel-iface: wlan0
with-node-id: true
node-label:
    - com.example.mylabel/type=foo
    - com.example.mylabel/net=wireless
```

This configuration file will tell `k3s` to connect to the master node, and to use the `wlan0` interface for the [Flannel](https://www.sysspace.net/post/kubernetes-networking-explained-flannel-network-model_) network.

Make sure the `/etc/conf.d/k3s` file has the following content:

```bash
export PATH="/usr/libexec/cni/:$PATH"
K3S_EXEC="agent"
K3S_OPTS=""
```

This will make sure that we start `k3s` in agent mode, and that we can use the `cni` binaries (for flannel).

##### Starting `k3s`

You can now start `k3s` (once) and enable it at boot:

```bash
service k3s start
rc-update add k3s
```

You can now check the logs with `tail -f /var/log/k3s.log` and see if the node is joining the cluster...

... except that, it won't work.

##### Missing kernel features

If you haven't skipped over the "Lessons learned" section, you might have noticed that I mentioned that you should check if your kernel is ready for Docker / Kubernetes / K3s. We generally take for granted that the kernels shipped with our distributions are ready for using containers and orchestrators, but this is not always the case.  
  
Specifically, in the case of the `dumpling` kernel (`msm8998`), it seems like the [kernel config](https://gitlab.postmarketos.org/postmarketOS/pmaports/-/blob/master/device/testing/linux-postmarketos-qcom-msm8998/config-postmarketos-qcom-msm8998.aarch64) is missing some key features that are required to run `docker` and `k3s`.  
  
You can get a list of all the missing configs by running k3s's [`check-config.sh`](https://github.com/k3s-io/k3s/blob/master/contrib/util/check-config.sh) script.


##### Recompiling the kernel

Thankfully, changing the kernel configuration is pretty straightforward. You can follow the [postmarketOS Kernel configuration/Adjusting one kernel](https://wiki.postmarketos.org/wiki/Kernel_configuration/Adjusting_one_kernel) to get started.

In my case, it was as easy as running:

```
pmbootstrap kconfig edit linux-postmarketos-qcom-msm8998
```

I then `/` searched for the needed config entries as reported by `check-config.sh` and enabled them. This was enough to run some Docker containers, but apparently not enough to have a fully working Kubernetes node as the flannel network was not working.

For this, you'll most likely need to enable all the `NETFILTER_XTABLES_*` options. Although probably unnecessary, you can find my kernel config [here](https://pastebin.com/pnNXrhb0).

##### Trying again

After recompiling the kernel, copying and installing resulting `.apk` file (`scp linux-postmarketos-qcom-msm8998-6.0-r2.apk root@dumpling` and `apk add -u linux-postmarketos-qcom-msm8998-6.0-r2.apk`) and rebooting, I was able to start `k3s` and see the node joining the cluster.

Unfortunately, in that moment, my cluster started having some issues. After a quick diagnosis, I found out that DNS resolution was broken. This made me realize the newly joined node was able to pull images from the internet, but the containers themselves were not able to reach the internet.


##### Network issues

To debug the network issues, I've used `netshoot`:

```bash
kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot
```

This spawned a shell in a container that had all the network tools I needed to debug the issue. Of course I had to make sure that the container was running on the affected node (I actually used a `DaemonSet` to make sure it was running on all the nodes).

The problems were:

- None of the containers were able to reach the internet
    - `ping 1.1.1.1` was not working
- Containers on the same network (node) were not able to reach each other
    - `ping 10.42.3.11` was not working from `10.42.3.13`
- Containers on different networks (on another node) were not able to reach each other
    - `ping 10.42.1.10` was not working from `10.42.0.3`
    - Flannel was likely not working here


```plain
# tcpdump -i any icmp
tcpdump: WARNING: any: That device doesn't support promiscuous mode
(Promiscuous mode not supported on the "any" device)
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on any, link-type LINUX_SLL2 (Linux cooked v2), snapshot length 262144 bytes
11:22:21.229307 veth50680d5c P   IP 10.42.3.13 > 10.42.3.11: ICMP echo request, id 10, seq 1, length 64
11:22:22.264132 veth50680d5c P   IP 10.42.3.13 > 10.42.3.11: ICMP echo request, id 10, seq 2, length 64
11:22:23.288137 veth50680d5c P   IP 10.42.3.13 > 10.42.3.11: ICMP echo request, id 10, seq 3, length 64
11:22:24.312629 veth50680d5c P   IP 10.42.3.13 > 10.42.3.11: ICMP echo request, id 10, seq 4, length 64
11:22:25.336390 veth50680d5c P   IP 10.42.3.13 > 10.42.3.11: ICMP echo request, id 10, seq 5, length 64

```

After investigating further, I discovered that there was a problem with the packet forwarding: none of the packets were being forwarded. The strangest part was that the `iptables -t nat` rules were correct, and nothing strange was happening in the `FORWARD` chain.

This kept me busy for a very long time as I was going crazy trying to understand why the packets were being dropped despite being allowed by `iptables`...


##### The solution

As spoilered in the "Lessons learned" section, the issue was with the `nftables` rules that were blocking the traffic. This took me an incredible amount of time to figure out, because I assumed that the issue was with either flannel using wthe wrong interface, with the kernel configuration or with... iptables.

If you're not aware of the difference between `iptables` and `nftables`, [`nftables`](https://wiki.archlinux.org/title/Nftables) is pretty much the new default in the Linux kernel (previously, it was `iptables`), and nowadays `iptables` _should_ just be a frontend for `nftables`.  
  
Unfortunately for me, the `nftables` rules were not visible from `iptables` (the opposite is true) - which made me investigate the wrong part of the system for a long time.

After adapting the `/etc/nftables.nft` file (as follows), the containers on the node were finally able to reach the internet and the other containers in the cluster.

```plain
#!/usr/sbin/nft -f
# vim: set ts=4 sw=4:
# You can find examples in /usr/share/nftables/.

# Clear all prior state
flush ruleset

# The state of stateful objects saved on the nftables service stop.
include "/var/lib/nftables/*.nft"

# Rules
```

##### Final steps

After fixing the issues with the network, I was able to run some workloads on the node. Since this node is connected via Wi-Fi and I can only get around 200 Mbit/s of DL and UL - I've marked this node with a label (`com.example.mylabel/net=wireless`) so that I can schedule workloads that are not latency or network intensive.

To finish the setup, I've created an Ansible playbook with the steps above and added one finishing touch:

```bash
echo 0 > /sys/class/backlight/c994000.dsi.0/brightness
```

This command completely turns off the backlight of the display, saving lots of power.

### OnePlus 8 Pro (instantnoodlep)

After the experience with the OnePlus 5T, I decided it was time to extend my cluster by adding another device.
With the learnings from the previous experience and the promising features list (Wi-Fi marked as working, mainline kernel, USB Networking working), I decided to go with the OnePlus 8 Pro.

I've followed the same steps as before, and then, as soon as I wrote `ip link show wlan0`, I realized there was something wrong...

```plain
$ ip link show wlan0
ip: can't find device 'wlan0'
```

... what?

#### A missing Wi-Fi chip

After reading the `dmesg` output and trying to find references to the Wi-Fi / BT chip (QCA6390), I realized that the [Device Tree (dtb)](https://wiki.postmarketos.org/wiki/Device_Tree_(dtb)) was missing the Wi-Fi / Bluetooth chip.  
  
I wasn't quickly able to spot the issue there, so I decided to look on the internet for answers - and that's where I found something that at the time looked promising: [a patch to add support for the OnePlus 8T (kebab)](https://patches.linaro.org/project/linux-input/patch/20240624-oneplus8-v1-7-388eecf2dff7@postmarketos.org/) (which is pretty much the same as the OnePlus 8 Pro).

I therefore decided to try out the patch - I cloned the kernel repository, applied the patch, compiled the DTS (`make dtbs`) and obtained the new `dtb` file.

#### Using the newly built DTB

Since I didn't want to follow the full `.img` creating process, I decided to unpack the original `boot.img` file and re-pack it with my own `dtb` file:

```bash
$ unpack_bootimg --boot_img $PMOS_ROOT/chroot_rootfs_oneplus-instantnoodlep/boot/boot.img --format=mkbootimg
$ cp ~/git/linux/arch/arm64/boot/dts/qcom/sm8250-oneplus-instantnoodlep.dtb /tmp/firmware/out/dtb
$ mkbootimg --header_version 2 --kernel out/kernel --ramdisk out/ramdisk --dtb out/dtb --pagesize 0x00001000 --base 0x00000000 --kernel_offset 0x00008000 --ramdisk_offset 0x01000000 --second_offset 0x00000000 --tags_offset 0x00000100 --dtb_offset 0x0000000001f00000 --board '' --cmdline 'clk_ignore_unused pd_ignore_unused  pmos_boot_uuid=d86a5f31-2802-4333-b5aa-ff8a59e4d66e pmos_root_uuid=efbc85d5-1ba9-45ff-af90-1eecd5235327 pmos_rootfsopts=defaults' -o boot-repacked.img
```

With the new image ready to be flashed, I connected the device to my computer and ran the following command:

```bash
$ fastboot flash boot boot-repacked.img
$ fastboot reboot
```

... and the device didn't boot.

#### Trying one small change at the time

When a device doesn't boot and you don't have a serial console - you're pretty much clueless on what's going on.
The only thing you can really do is to go back to the last working state (in my case, the original `dtb`) and try to change one small thing at the time until you find the issue.

In this particular phase, I've tried to adapt the `dtb` by following other references: the [`sm8250-mainline`](https://gitlab.com/sm8250-mainline) kernel already includes lots of other devices using the same chip and with a similar configuration. For example, the [Xiaomi Mi Pad 5 Pro (elish)](https://wiki.postmarketos.org/wiki/Xiaomi_Mi_Pad_5_Pro_(xiaomi-elish)) used the same chip and described it as being part of the PCI0 port as seen in its dts file: [
`sm8250-xiaomi-elish-common.dtsi`](https://gitlab.com/sm8250-mainline/linux/-/blob/sm8250/v6.11/arch/arm64/boot/dts/qcom/sm8250-xiaomi-elish-common.dtsi?ref_type=heads#L824-839).  
  
Additionally, the device tree also described [some GPIOs to enable the chip](https://gitlab.com/sm8250-mainline/linux/-/blob/sm8250/v6.11/arch/arm64/boot/dts/qcom/sm8250-xiaomi-elish-common.dtsi?ref_type=heads#L1008-1022), together with a [voltage regulator](https://gitlab.com/sm8250-mainline/linux/-/blob/sm8250/v6.11/arch/arm64/boot/dts/qcom/sm8250-xiaomi-elish-common.dtsi?ref_type=heads#L108-167) to power the chip.

After many trial and errors in adapting and stiching together some configuration, I was finally able to see the chip getting recognized:

```plain
# dmesg | grep ath11k
[   11.524348] ath11k_pci 0000:01:00.0: Adding to iommu group 13
[   11.524578] ath11k_pci 0000:01:00.0: BAR 0 [mem 0x60400000-0x604fffff 64bit]: assigned
[   11.524642] ath11k_pci 0000:01:00.0: enabling device (0000 -> 0002)
[   11.524983] ath11k_pci 0000:01:00.0: MSI vectors: 32
[   11.525005] ath11k_pci 0000:01:00.0: qca6390 hw2.0
[   12.796173] ath11k_pci 0000:01:00.0: chip_id 0x0 chip_family 0xb board_id 0xff soc_id 0xffffffff
[   12.796205] ath11k_pci 0000:01:00.0: fw_version 0x10121492 fw_build_timestamp 2021-11-04 11:23 fw_build_id
```

I then checked that the adapter was being recognized (`ip link show wlan0`) and tried to connect to my Wi-Fi network.
Everything worked perfectly: I was able to join this device to the cluster and run some workloads on it, as with the previous device.  
  
Since I deeply care about reducing e-waste and getting others to use their old devices, I've submitted my patch to the [sm8250-mainline kernel repo](https://gitlab.com/sm8250-mainline/linux/-/merge_requests/8) and added a note on the [device page](https://wiki.postmarketos.org/wiki/OnePlus_8_Pro_(oneplus-instantnoodlep)#Known_Issues) until the patch is picked up by the postmarketOS kernel.

#### Backlight

Unfortunately this device doesn't have the backlight described in the device tree, and it's therefore not possible (at the moment) to turn it off. This is not a big issue for me, but it would be a good candidate for a future patch.


## Conclusion

After joining the second node to the cluster, I have now a small cluster of 3 nodes that I can use to run my workloads, and I'm happy that I can reuse old devices that would have otherwise kept collecting dust in my drawer.

```plain
$ kubectl get nodes
NAME                               STATUS   ROLES                  AGE    VERSION
k3s-node-dumpling-cf0b07d4         Ready    <none>                 15d    v1.31.2-k3s1
k3s-node-instantnoodlep-e577c75e   Ready    <none>                 2d8h   v1.31.2-k3s1
master-1                           Ready    control-plane,master   14d    v1.31.2-k3s1
```


### Pre-built images

Since I've spent quite some time re-packing the boot image for `instantnoodlep`, I've decided to share the `boot.img`.
Granted that you should never trust a random kernel image from the internet, this could save you a bit of time.

- [`boot-repacked.img`](https://drive.google.com/file/d/1pQ5A0yJDBMO92uh4-qROcdpHTemuzKGx/view?usp=sharing)