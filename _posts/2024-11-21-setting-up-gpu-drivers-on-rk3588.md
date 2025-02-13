---

tags: [linux, hardware>rockchip]
info: aberto.
date: 2024-11-21
type: post
layout: post
published: true
slug: setting-up-gpu-drivers-on-rk3588
title: 'Setting Up GPU Drivers on RK3588'
---
MLC LLM is a universal deployment solution that allows efficient CPU/GPU code generation without AutoTVM-based performance tuning. This guide focuses on setting up a generic GPU environment and troubleshooting common issues on the RK3588 (RK3588 based SBC).

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [OpenCL SDK Installation](#opencl-sdk-installation)
3. [RK3588 Setup](#orange-pi-5-setup)
    - [Installing Ubuntu 22.04](#installing-ubuntu-2204)
    - [Installing Mali GPU Driver](#installing-mali-gpu-driver)
    - [Configuring OpenCL ICD Loader](#configuring-opencl-icd-loader)
    - [Installing OpenCL Libraries](#installing-opencl-libraries)
    - [Installing Dependencies](#installing-dependencies)
    - [Verifying Installation with clinfo](#verifying-installation-with-clinfo)
4. [Troubleshooting](#troubleshooting)
5. [References](#references)

## Prerequisites

Before beginning the installation process, ensure that you have:

- An RK3588 (RK3588 based Single Board Computer)
- A stable internet connection
- Basic knowledge of using the Linux command line
- Physical access to the RK3588 for setup

## OpenCL SDK Installation

The OpenCL SDK is essential if you plan to build your own models for the OpenCL backend. Follow the steps below to install the OpenCL SDK:

1. **Access OpenCL's GitHub Repository:**

   Visit the [OpenCL SDK GitHub Repository](https://github.com/KhronosGroup/OpenCL-SDK) for detailed installation instructions and resources.

## RK3588 Setup

This section guides you through setting up the RK3588 for running models using the OpenCL backend.

### Installing Ubuntu 22.04

1. **Download Ubuntu 22.04 Image:**

   Download the Ubuntu 22.04 image tailored for the RK3588 from [here](https://github.com/Joshua-Riek/ubuntu-rockchip/releases/tag/v1.22).

2. **Flash Ubuntu to SD Card:**

   Use a tool like `balenaEtcher` or `Rufus` to flash the downloaded image onto an SD card.

3. **Boot RK3588:**

   Insert the SD card into your RK3588 and power it on. Follow the on-screen instructions to complete the initial setup.

### Installing Mali GPU Driver

To enable the Mali GPU for OpenCL operations, install the Mali GPU driver.

1. **Download `libmali-g610.so`:**

   ```bash
   cd /usr/lib
   sudo wget https://github.com/JeffyCN/mirrors/raw/libmali/lib/aarch64-linux-gnu/libmali-valhall-g610-g6p0-x11-wayland-gbm.so -O libmali-g610.so
   ```

2. **Ensure Firmware File Exists:**

   Verify if `mali_csffw.bin` exists in the `/lib/firmware` directory:

   ```bash
   cd /lib/firmware
   ls mali_csffw.bin
   ```

   If the file does not exist, download it:

   ```bash
   sudo wget https://github.com/JeffyCN/mirrors/raw/libmali/firmware/g610/mali_csffw.bin
   ```

### Configuring OpenCL ICD Loader

Set up the OpenCL Installable Client Driver (ICD) loader to recognize the Mali GPU.

1. **Update Package List:**

   ```bash
   sudo apt update
   ```

2. **Install Mesa OpenCL ICD:**

   ```bash
   sudo apt install mesa-opencl-icd -y
   ```

3. **Create OpenCL Vendors Directory:**

   ```bash
   sudo mkdir -p /etc/OpenCL/vendors
   ```

4. **Add Mali ICD Configuration:**

   ```bash
   echo "/usr/lib/libmali-g610.so" | sudo tee /etc/OpenCL/vendors/mali.icd
   ```

### Installing OpenCL Libraries

Install the OpenCL development libraries required for compiling OpenCL applications.

```bash
sudo apt install ocl-icd-opencl-dev -y
```

### Installing Dependencies

Install necessary dependencies for the Mali OpenCL backend.

```bash
sudo apt install libxcb-dri2-0 libxcb-dri3-0 libwayland-client0 libwayland-server0 libx11-xcb1 -y
```

### Verifying Installation with clinfo

1. **Install clinfo:**

   ```bash
   sudo apt install clinfo -y
   ```

2. **Run clinfo to Validate Installation:**

   ```bash
   clinfo
   ```

   **Expected Output:**

   Look for GPU information similar to the following in the output:

   ```bash
   arm_release_ver: g13p0-01eac0, rk_so_ver: 3
   Number of platforms: 2
   Platform Name: ARM Platform
   Platform Vendor: ARM
   Platform Version: OpenCL 2.1 v1.g6p0-01eac0.2819f9d4dbe0b5a2f89c835d8484f9cd
   Platform Profile: FULL_PROFILE
   ...
   ```

   This output confirms that the OpenCL runtime and Mali GPU driver are correctly installed and recognized by the system.

## Troubleshooting

If you encounter issues during the installation process, consider the following steps:

- **Check Network Connectivity:** Ensure that your RK3588 has a stable internet connection for downloading packages and dependencies.
- **Verify File Downloads:** Re-download any files if the download was interrupted or corrupted.
- **Review Command Outputs:** Carefully read any error messages during command execution to identify missing dependencies or permissions issues.
- **Consult Logs:** Check system logs for detailed error information using `dmesg` or reviewing logs in `/var/log/`.

## References

1. [OpenCL SDK GitHub Repository](https://github.com/KhronosGroup/OpenCL-SDK)
2. [MLC LLM GitHub Repository](https://github.com/mlc-ai/mlc-llm)
3. [Ubuntu Rockchip Releases](https://github.com/Joshua-Riek/ubuntu-rockchip/releases/tag/v1.22)
4. [Mali GPU Drivers](https://github.com/JeffyCN/mirrors/raw/libmali/lib/aarch64-linux-gnu/)
5. [Orange Pi Official Website](https://www.orangepi.org/)
6. [clinfo Documentation](https://github.com/obfuscated12/clinfo)
7. [Ubuntu Official Documentation](https://ubuntu.com/tutorials)

---

By following this comprehensive guide, you should be able to successfully set up GPU drivers and SDKs on your RK3588, enabling efficient OpenCL backend operations with MLC LLM.
