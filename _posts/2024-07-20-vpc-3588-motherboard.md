---
tags:
  - hardware
info: aberto.
date: 2024-07-20
type: post
layout: post
published: true
slug: vpc-3588-motherboard
title: 'VPC-3588 Motherboard'
---

The VPC-3588 motherboard is based on the Rockchip RK3588 high-performance application processor platform. It integrates advanced features suitable for various applications, including digital signage, touch interaction, consumer electronics, and entertainment systems.

## 1. Chip Overview
- **CPU**: RK3588 Quad-core Cortex-A76 + Quad-core Cortex-A55, up to 2.4GHz
- **GPU**: ARM Mali-G610 MC4, supports OpenGL ES 1.1/2.0/3.1/3.2, OpenCL 1.1/1.2/2.0, Vulkan 1.1/1.2
- **NPU**: 6 TOPS AI computing power, supports int4/int8/int16/FP16/BF16/TF32
- **Multimedia**: Supports H.265/H.264/AV1/VP9/AVS2 video decoding, up to 8K@60FPS; supports H.264/H.265 video encoding, up to 8K@30FPS
- **Display**: Supports multi-screen output, up to 8K@60FPS; various display interfaces including EDP/DP/HDMI2.1/MIPI
- **Video Input**: Supports multiple camera inputs (4*4 lanes or 4*2 lanes + 2*4 lanes) MIPI CSI-2 and DVP interfaces; 32MP ISP, supports HDR and 3DNR; supports HDMI 2.0 input, up to 4K@60FPS
- **High-Speed Interfaces**: Supports PCIe 3.0/PCIe 2.0/SATA 3.0/RGMII/TYPE-C/USB 3.1/USB 2.0

## 2. Product Overview
The VPC-3588 motherboard is designed for ultra-thin applications with strict material selection and design. It features a compact size and rich interfaces for easy integration into complete systems.

## 3. Specifications List

### General Specifications
- **Physical Size**: 170mm x 170mm x 17mm
- **Operating Temperature**: -20°C to 70°C
- **Operating Humidity**: 0% to 95% (non-condensing)

### CPU
- **Model**: RK3588
- **Cores**: 8 cores (4 Cortex-A76 + 4 Cortex-A55)
- **Max Frequency**: 2.4GHz

### Memory
- **Type**: LPDDR4
- **Capacity Options**: 2GB (expandable to 32GB)

### Storage
- **Default Storage**: 16GB eMMC NAND (expandable up to 128GB)
- **SATA Interfaces**: 4 standard SATA 3.0 hard disk interfaces (with power supply pins)
- **mSATA Interface**: 1 industry-standard mSATA module interface

### Video Output
- **HDMI Output**: 1 HDMI 2.1 standard output (up to 8K)
- **HDMI Input**: 1 HDMI 2.0/1.4b input (up to 2160p@60Hz)
- **VGA Output**: Standard DB-15 VGA output (up to 1080P)
- **LVDS Interface**: 30-pin dual LVDS interface (supports up to 1080P)
- **EDP Interface**: 20-pin EDP interface (supports up to 4K@60Hz)

### USB Interfaces
- **USB 3.0**: 4 external USB 3.0 ports (3 Host + 1 OTG)
- **USB 2.0**: 7 internal USB 2.0 headers (6 Hub + 1 Host)
- **USB 3.0 Type A**: 3 USB 3.0 Type A sockets

### Serial Communication
- **TTL/RS-232/RS-485 Ports**: 1 TTL, 2 TTL/RS-232/RS-485 compatible, 2 TTL/RS-232 compatible, 4 extensions
- **CAN Bus Interfaces**: 2 CAN pin headers for CAN bus peripherals

### Audio
- **Audio Output**: Dual audio amplifier output (6W @ 8 Ohm)
- **Headphone Output**: Stereo headphone output
- **Microphone Input**: Differential MIC input

### Networking
- **Ethernet**: 1 Gigabit Ethernet RJ45 port + 4-pin PoE header
- **Wi-Fi**: Built-in high-performance SDIO interface for Wi-Fi 6 module
- **Bluetooth**: Built-in high-performance Bluetooth module (supports up to BT 5.0)

### GPIO and I2C
- **GPIO**: Up to 8 GPIO signals for buttons and/or 3.3V input/output
- **I2C Interface**: I2C pin header for I2C devices

### Power Supply
- **Input Voltage**: DC 12V (supports 9-15V)
- **Fan Headers**: SYS fan power header and CPU fan power header

### Additional Features
- **Real-Time Clock**: Ultra-low-power RTC circuit with CR1220 battery
- **Tamper Control**: 1 tamper control port
- **LED Indicators**: Red standby and green working indicators

## 4. Interface Definitions

### Power Interfaces
- **DC-12V Socket**: For power input
- **SATA Power Supply Headers**: For SATA drives

### Data Interfaces
- **HDMI Output/Input**: For video output/input
- **VGA Output**: For connecting VGA monitors
- **LVDS/EDP Interfaces**: For connecting LCD panels

### USB Interfaces
- **USB 3.0/2.0 Ports**: For connecting USB devices

### Serial Interfaces
- **TTL/RS-232/RS-485 Ports**: For serial communication

### Expansion Slots
- **PCIe x4 Slot**: For graphics cards or other PCIe devices

## 5. Compatible Peripherals
The VPC-3588 motherboard supports a wide range of peripherals, including:
- **Storage Devices**: mSATA SSDs, SATA HDDs/SSDs
- **Graphics Cards**: PCIe x4 compatible graphics cards
- **Networking Devices**: Ethernet cards, Wi-Fi modules
- **Audio Devices**: Sound cards, microphones, speakers
- **Display Devices**: HDMI displays, VGA monitors, LVDS/EDP panels
- **Input Devices**: Keyboards, mice, touchscreens
- **Serial Communication Devices**: Various serial devices, CAN bus peripherals
- **USB Devices**: USB hubs, external storage
- **Power Over Ethernet (PoE) Devices**: Devices that support PoE