---
tags:
  - hardware
info: aberto.
date: 2024-08-01
type: post
layout: post
published: true
slug: laptop-alternative
title: 'Laptop alternative'
---

## You Don’t Need a Powerful Laptop Anymore

Yes, you read that right. You don’t need to invest thousands of dollars in a high-end laptop — in fact, you might not even need a laptop at all! While laptops have traditionally been essential for many tasks, advancements in technology have made it possible to perform complex computing tasks remotely, reducing the need for powerful local machines.

You might be thinking, “But I love my laptop! It’s my trusty companion for work and meetings.” Allow me to introduce you to a new paradigm in computing that leverages remote processing capabilities.

### The Vision of Remote Processing

Since 2009, I have predicted that humanity would become increasingly connected, with improvements in internet speed and reliability. The future of computing lies in powerful servers handling the heavy lifting while we use lightweight devices merely for display and interaction. This vision is now a reality, and I want to share how I’ve been utilizing this setup effectively over the past few months.

---

## The Setup

To embrace this new way of computing, you will need:

- A powerful workstation equipped with a GTX or RTX graphics card (if you have an AMD or Intel GPU, or prefer a simpler solution, consider using Parsec).
- The fastest internet connection available to you.
- A basic, lightweight laptop — a ThinkPad X1 Carbon with 4th Gen specs is a great option.
- A reliable mobile data link for connectivity.

The idea is to connect your powerful workstation to this lightweight laptop over the internet, using the laptop solely for displaying and streaming encrypted images, sound, and commands.

### Essential Equipment

To fully embrace this setup, consider the following:

- A high-resolution 4K monitor
- A comfortable keyboard and mouse
- A USB-C dock with HDMI and LAN ports (available from various online marketplaces)
- A robust 65W charger at each location
- Optionally, a smartphone for additional connectivity

If you frequently work on the go, a Samsung Galaxy Tab or an Apple iPad with a keyboard/trackpad folio case can serve as an excellent alternative, allowing you to maintain productivity with minimal weight.

---

## Setting It Up

### Host Configuration

1. **Choose Your Workstation:** Select a powerful machine. If you need Adobe software, opt for Microsoft Windows; for coding and performance, Linux is preferable.
2. **BIOS Configuration:** Set your BIOS to power on the device automatically when AC power is available to prevent downtime.
3. **Install Necessary Software:** Download and install the latest Nvidia drivers, Sunshine (for remote access), and MultiMonitorTool.

### Configure Sunshine

- Ensure Sunshine starts automatically with your machine. Use the Windows Run command (WIN + R), type `shell:startup`, and drag the Sunshine program into the Startup folder.
- Set a secure username and password in the Sunshine configuration menu.

### MultiMonitorTool Setup

- Place the MultiMonitorTool executable in the C: drive.
- Open it and select `File > Save Monitors Configuration`, saving it directly to the C: drive.

### Additional Sunshine Configuration

- Open Sunshine and navigate to the Configuration tab.
- Under "Do Command," enter:
  ```
  cmd /C C:\MultiMonitorTool.exe /SetMonitors "Name=\\.\DISPLAY1 Width=%SUNSHINE_CLIENT_WIDTH% Height=%SUNSHINE_CLIENT_HEIGHT% DisplayFrequency=%SUNSHINE_CLIENT_FPS%"
  ```
- Adjust the "Name=" parameter based on your monitor's name from MultiMonitorTool.
- Under "Undo Command," enter:
  ```
  cmd /C C:\MultiMonitorTool.exe /LoadConfig C:\MonitorsDefault.cfg
  ```

### Client Connection

You will connect clients after setting up port forwarding. Each client must be authorized individually.

### Internet Configuration

Forward the following ports on your router (exercise caution with the Web UI port):

- 47984 (TCP)
- 47989 (TCP)
- 48010 (TCP)
- 47998–48000 (UDP)

### Client Installation

- Install Moonlight apps (available for Android and iOS) or relevant programs on your client devices.
- Retrieve your external IP address by visiting a site like What Is My IP Address.
- Connect your device through mobile internet and add a client with that IP in your app.

Enter your device name and PIN in the Sunshine configuration panel under the “Pin” tab (`https://localhost:47990/pin`). You are now connected!

---

## Additional Tips for Optimal Performance

- Adjust your bandwidth settings for stability, starting with a minimum and increasing as needed.
- Enable V-Sync and experiment with different hardware encoding settings for optimal performance.
- Optimize mouse settings for remote desktop use to enhance responsiveness.

Welcome to the new era of computing!

And don’t forget to check out your favorite Snowmonkey flask, available at a 15% discount with the code **SuperShort15**!

---

## Q&A

**Is this just a Remote Desktop/VNC solution?**  
No, this setup is designed for high-performance tasks, including gaming, and can handle streaming at 120FPS or more. Unlike traditional Remote Desktop or VNC solutions, this method provides a seamless experience akin to working directly on the machine.

**Is there a simpler way to achieve this?**  
Yes, you can use Parsec, which offers a user-friendly interface and a free tier for basic use. However, the setup I described may provide better performance and lower CPU usage due to its hardware-based nature.

**What about security?**  
All traffic is encrypted, but for added security, consider using a VPN like WireGuard to connect to your home network.

**Is bandwidth a critical factor?**  
Yes, the faster your internet connection, the better the visual quality you can achieve. However, a standard mobile 4G connection should suffice for most tasks.

**Did you invent this technology?**  
No, I am sharing insights on existing technology that has matured to the point where it can deliver a smooth, responsive experience without the delays typical of older remote access solutions.