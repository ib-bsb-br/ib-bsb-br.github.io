---
tags: [scratchpad]
info: aberto.
date: 2025-02-12
type: post
layout: post
published: true
slug: rk3588-linux-system-flashing-operation-instructions
title: 'RK3588 Linux System Flashing Operation Instructions'
---
## Prerequisites

### Hardware

- Computer (notebook)
- Android data cable  
  *Note: Use a Type-C data cable for the 3399 board.*

### Software

- Motherboard driver tool
- 3288 motherboard 7.1 system flashing tool
- Linux system flashing tool

> **Note:** To obtain the driver tool and flashing tool, please contact after-sales technical support.

---

## Flashing Operation

### 1. Install the Motherboard Driver Installation Tool on the Computer

#### 1-1.
- Unzip the driver tool.
- Double-click the `DriverInstall` application.

*Page: 1 of 8*

#### 1-2.
- Click **[Driver Installation]**.  
  The computer will automatically install the motherboard driver (this takes about 30 seconds).  
  Once finished, the installation is successful.

*Page: 2 of 8*

---

### 2. Connect the Motherboard to the Computer Using the Android Data Cable

#### 2-1.
- **Data cable type:** Android data cable

#### 2-2.
- Connect the motherboard and the computer as follows:
  - Plug the smaller end of the data cable into the motherboard’s MicroUSB port.
  - Plug the larger end into the computer’s USB port.

*Page: 3 of 8*

---

### 3. Linux System Flashing

> **Important Note:**  
> If the motherboard is previously running an Android system, please ensure it is running Android version 7.1.  
> If it is not version 7.1, first flash it to version 7.1; otherwise, after converting to the Linux system, the screen parameters and other system parameters cannot be programmed.

#### Additional Notes

1. If the motherboard originally had an Android system, the first flash must be done by forcing entry into Mask ROM mode.  
   *(If the forced software method fails, use hardware by shorting the designated test point on the motherboard to enter Mask ROM.)*
2. Flashing in Mask ROM mode is generally required only if the motherboard previously ran an Android system.

#### 3-1.
- Unzip the rk8linux flashing toolkit.
- Double-click the `AndroidTool` application.

*Page: 5 of 8*

#### 3-2.
- Use your hand or tweezers to press and hold the **flash button** on the motherboard.
- Power on the motherboard.
- The flashing program will display **"Found a LOADER device"**.
- Release the button.
- Select **[Advanced Features]** and click **[Enter Mask ROM]**.
- The flashing program will display **"Found a MASKROM device"**.

*Page: 6 of 8*

#### Next Steps
- Select **[Download Image]**.
- Click **[Execute]**.  
  The system will automatically flash the image.
- Wait for 5 to 6 minutes until the flashing program displays **"Download Complete"**.

*Page: 7 of 8*

---

*Page: 8 of 8*

At this point, the Linux system flashing on the 3399 motherboard is complete.  
Disconnect the data cable, then power on the motherboard; the display should light up.