---
tags: [scratchpad]
info: aberto.
date: 2025-05-24
type: post
layout: post
published: true
slug: optimizing-rk3588-performance
title: 'Optimizing RK3588 Performance '
---
bibref https://sbcwiki.com/news/articles/tune-your-rk3588/

This article details methods to enhance the performance of the Rockchip RK3588 system-on-chip (SoC). By adjusting configurations for the **CPU**, **GPU**, and **RAM**, it is possible to achieve significant performance improvements beyond default settings, potentially increasing overall system performance by **up to 40%** in specific benchmarks.

The techniques described leverage capabilities present in the hardware that may not be fully utilized by standard software configurations. This guide is based on testing performed using the latest Armbian Build with the Rockchip BSP Kernel version `6.1.115` but the overlays can be adapted to any distro.

> **Warning**
> 
> 
> This guide involves operating hardware components outside their default specifications. This constitutes overclocking and carries a risk of instability, increased heat generation, and potential hardware damage. Implementing these modifications is done at your own risk. Ensure adequate cooling is in place before proceeding.

CPU Performance Optimization [#](https://sbcwiki.com/news/articles/tune-your-rk3588/#cpu-performance-optimization)
------------------------------------------------------------------------------------------------------------------

Optimizing the CPU frequency on the RK3588 can be achieved through device-tree modifications. Depending on the specific silicon quality, many RK3588 units are capable of stable operation at **2.4GHz** with a minor adjustment to the core voltage from a fixed **1v** to **1.05v**.

This optimization is typically implemented using a device-tree overlay. In Armbian, the `rockchip-rk3588-opp-oc-24ghz` overlay is provided for this purpose. This overlay modifies the CPU’s [Operating Performance Point (OPP) table](https://www.kernel.org/doc/Documentation/devicetree/bindings/opp/opp.txt) to include the desired higher frequency and corresponding voltage.

To apply the overlay you have to:

1.   `sudo run armbian-config`
2.   ![Image 3: CPU-OC-Step1](https://sbcwiki.com/news/articles/tune-your-rk3588/armbian-config-1_hu_859bd22d7137399f.webp)
3.   ![Image 4: CPU-OC-Step2](https://sbcwiki.com/news/articles/tune-your-rk3588/armbian-config-2_hu_1c56005696a5d371.webp)
4.   ![Image 5: CPU-OC-Step3](https://sbcwiki.com/news/articles/tune-your-rk3588/armbian-config-3_hu_b3d2726ebf993da3.webp)
5.   ![Image 6: CPU-OC-Step4](https://sbcwiki.com/news/articles/tune-your-rk3588/armbian-config-4_hu_394758f8035ac909.webp)
6.   Save & Reboot

### CPU Optimization Results [#](https://sbcwiki.com/news/articles/tune-your-rk3588/#cpu-optimization-results)

Applying the CPU overclock to 2.4GHz resulted in performance improvements of up to **+9%** in Single-Core tests and **+4%** in Multi-Core tests within Geekbench 6.

GPU Clock Correction [#](https://sbcwiki.com/news/articles/tune-your-rk3588/#gpu-clock-correction)
--------------------------------------------------------------------------------------------------

Analysis of RK3588 configurations reveals that the integrated Mali-G610 MP4 GPU, while rated for a **1GHz** clock speed, often operates at a lower frequency, commonly around **850MHz**, in default software configurations. It has been observed that the devfreq subsystem may report the intended 1GHz clock even when the hardware is running slower.

To verify the actual GPU clock speed, the clk_summary debugfs interface can be consulted:

```
cat /sys/kernel/debug/clk/clk_summary | grep gpu
```

If the reported actual frequency is below 1GHz, a configuration discrepancy exists. Correcting the device-tree to properly set the GPU clock to its rated 1GHz is necessary to utilize its full potential. If this issue is present in your OS build, reporting it to the maintainers is recommended.

### GPU Clock Correction Results [#](https://sbcwiki.com/news/articles/tune-your-rk3588/#gpu-clock-correction-results)

Ensuring the GPU operates at its rated 1GHz frequency yields a substantial performance increase. Testing with `glmark2-wayland` in the demanding ’terrain’ scene, a common benchmark for embedded GPUs, shows an improvement of approximately **18%**.

RAM Optimization (LPDDR5 Models) [#](https://sbcwiki.com/news/articles/tune-your-rk3588/#ram-optimization-lpddr5-models)
------------------------------------------------------------------------------------------------------------------------

This section details a method for optimizing memory performance on RK3588 boards equipped with LPDDR5 RAM. The Technical Reference Manual specifies „optimized“ support for LPDDR5-5500 MT/s (here equivalent to a 2736MHz clock). However, testing indicates the memory controller is capable of operating at higher speeds, specifically the maximum standard LPDDR5 speed of **6400 MT/s** (corresponding to a 3200MHz clock).

Implementing this requires _verifying_ that the installed LPDDR5 modules on your board are rated for 6400 MT/s or higher. This can be done by identifying the RAM chip model number (usually printed on the chip) and consulting its datasheet or searching online.

For reference, testing was conducted on:

*   A Radxa Rock-5T using SKHynix H58G56AK6B-X069 modules, rated for LPDDR5-6400.
*   A 24GB Rock-5B-Plus using two 12GB SKHynix H58GG8AK8Q-X103 modules.

While rated for LPDDR5X-8533, these operate in LPDDR5 backwards compatibility mode and are fully capable of LPDDR5-6400 operation.

Achieving 6400 MT/s operation requires two steps:

1.   Enable a device-tree overlay: The `rockchip-rk3588-dmc-oc-3500mhz` overlay is required to enable the necessary memory controller frequency steps, despite the name indicating 3500MHz.

2.   Apply timing parameters with RKDDR Tool: The specific low-level timing parameters for 3200MHz (6400 MT/s) must be loaded into the ddr blob. This is accomplished using [Hbiyik’s RKDDR Tool](https://github.com/hbiyik/rkddr). The tool requires setting specific register values, illustrated by the following configuration: ![Image 7: RKDDR](https://sbcwiki.com/news/articles/tune-your-rk3588/RKDDR_hu_5a57348b4ed75b9e.png)

### RAM Optimization Results [#](https://sbcwiki.com/news/articles/tune-your-rk3588/#ram-optimization-results)

The increase in memory bandwidth significantly impacts overall system performance, particularly in memory-intensive tasks. Re-evaluating the glmark2-wayland terrain test used previously, applying the 6400 MT/s RAM optimization in addition to the GPU clock correction resulted in a further performance increase. The benchmark score rose from 100-105 FPS (stock) to 120-125 FPS (GPU clock corrected) to **140 FPS** (GPU clock corrected + RAM optimized). This represents an approximate 20% performance gain in this test attributed to the RAM optimization alone, and a **cumulative +40% over stock**.

This improvement in memory performance translates to enhanced responsiveness and throughput across a wide range of applications, not limited to graphics benchmarks.

For additional tuning [#](https://sbcwiki.com/news/articles/tune-your-rk3588/#for-additional-tuning)
----------------------------------------------------------------------------------------------------

I can recommend applying Thomas Kaiser’s `‌/etc/sysfs.d/tk-optimize-rk3588.conf` from [here](https://github.com/ThomasKaiser/Knowledge/blob/master/articles/Quick_Preview_of_ROCK_5B.md#important-insights-and-suggested-optimisations). He goes in-depth about his results in the linked article.

Full Link to Thomas Kaisers optimizations: [https://github.com/ThomasKaiser/Knowledge/blob/master/articles/Quick_Preview_of_ROCK_5B.md#important-insights-and-suggested-optimisations](https://github.com/ThomasKaiser/Knowledge/blob/master/articles/Quick_Preview_of_ROCK_5B.md#important-insights-and-suggested-optimisations)

Conclusion [#](https://sbcwiki.com/news/articles/tune-your-rk3588/#conclusion)
------------------------------------------------------------------------------

By applying these optimizations – increasing the CPU frequency and voltage, correcting the GPU clock speed to its rated value, and configuring the LPDDR5 RAM for 6400 MT/s operation – the performance of the RK3588 SoC can be substantially improved. As demonstrated, **cumulative gains of around 40%** in specific benchmarks are achievable.

Users undertaking these modifications should proceed cautiously, acknowledging the inherent risks associated with operating hardware outside standard parameters and ensuring adequate thermal management is implemented to maintain system stability.