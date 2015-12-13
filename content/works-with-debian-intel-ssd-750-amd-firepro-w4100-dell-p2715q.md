Title: Works with Debian: Intel SSD 750, AMD FirePro W4100, Dell P2715Q
Date: 2015-12-13T08:58+0000
Summary: New hardware was installed into a Debian workstation with minor issues.

I recently installed new hardware in my primary computer running Debian
unstable. The disk used for the `/` and `/home` filesystem was replaced with an
[Intel SSD 750 series] NVM Express card. The graphics card was replaced by an
[AMD FirePro W4100] card, and two [Dell P2715Q] monitors were installed.

### [Intel SSD 750 series] NVM Express card

This is an 800 GB SSD on a PCI-Express x4 card (model number `SSDPEDMW800G4X1`)
using the relatively new [NVM Express] interface, which appears as a
`/dev/nvme*` device. The stretch alpha 4 Debian installer was able to detect and
install onto this device, but [grub-installer] 1.127 on the installer media was
unable to install the boot loader. This was due to a bug recently fixed in
1.128:

``` .boxed
grub-installer (1.128) unstable; urgency=high

  * Fix buggy /dev/nvme matching in the case statement to determine
    disc_offered_devfs (Closes: #799119). Thanks, Mario Limonciello!

 -- Cyril Brulebois <kibi@debian.org>  Thu, 03 Dec 2015 00:26:42 +0100
```

I was able to download and install the updated .udeb by hand in the installer
environment and complete the installation.

This card was installed on a [Supermicro X10SAE] motherboard, and the UEFI BIOS
was able to boot Debian directly from the NVMe card, although I updated to the
latest available BIOS firmware prior to the installation. It appears in `lspci`
like this:

``` .boxed
02:00.0 Non-Volatile memory controller: Intel Corporation PCIe Data Center SSD (rev 01)
(prog-if 02 [NVM Express])
	Subsystem: Intel Corporation SSD 750 Series [Add-in Card]
	Flags: bus master, fast devsel, latency 0
	Memory at f7d10000 (64-bit, non-prefetchable) [size=16K]
	Expansion ROM at f7d00000 [disabled] [size=64K]
	Capabilities: [40] Power Management version 3
	Capabilities: [50] MSI-X: Enable+ Count=32 Masked-
	Capabilities: [60] Express Endpoint, MSI 00
	Capabilities: [100] Advanced Error Reporting
	Capabilities: [150] Virtual Channel
	Capabilities: [180] Power Budgeting <?>
	Capabilities: [190] Alternative Routing-ID Interpretation (ARI)
	Capabilities: [270] Device Serial Number 55-cd-2e-41-4c-90-a8-97
	Capabilities: [2a0] #19
	Kernel driver in use: nvme
```

The card itself appears very large in marketing photos, but this is a visual
trick: the photographs are taken with the low-profile PCI bracket installed,
rather than the [standard height PCI bracket] which it ships installed with.

smartmontools [fails to read SMART data] from the drive, although it is still
able to retrieve basic device information, including the temperature:

``` .boxed
root@chase{0}:~# smartctl -d scsi -a /dev/nvme0n1
smartctl 6.4 2015-06-04 r4109 [x86_64-linux-4.3.0-trunk-amd64] (local build)
Copyright (C) 2002-15, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===
Vendor:               NVMe
Product:              INTEL SSDPEDMW80
Revision:             0135
Compliance:           SPC-4
User Capacity:        800,166,076,416 bytes [800 GB]
Logical block size:   512 bytes
Rotation Rate:        Solid State Device
Logical Unit id:      8086INTEL SSDPEDMW800G4                     1000CVCQ531500K2800EGN  
Serial number:        CVCQ531500K2800EGN
Device type:          disk
Local Time is:        Sun Dec 13 01:48:37 2015 EST
SMART support is:     Unavailable - device lacks SMART capability.

=== START OF READ SMART DATA SECTION ===

Current Drive Temperature:     31 C
Drive Trip Temperature:        85 C

Error Counter logging not supported


[GLTSD (Global Logging Target Save Disable) set. Enable Save with '-S on']
Device does not support Self Test logging
root@chase{4}:~# 
```

Simple tests with `cat /dev/nvme0n1 >/dev/null` and `iotop` show that the card
can read data at about 1 GB/sec, about twice as fast as the SATA-based SSD that
it replaced. apt/dpkg now run about as fast on the NVMe SSD as they do on a
`tmpfs`.

Hopefully this device doesn't at some point require updated firmware, like some
[infamous SSDs have].

### [AMD FirePro W4100] graphics card

This is a graphics card capable of driving multiple DisplayPort displays at
["4K" resolution] and at a 60 Hz refresh rate. It has four Mini DisplayPort
connectors, although I only use two of them.

It was difficult to find a sensible graphics card. Most discrete graphics cards
[appear to be marketed towards video gamers] who apparently must seek out bulky
cards that occupy multiple PCI slots and have excessive cooling devices. (To
take a random example, the [ASUS STRIX R9 390X] has three fans and brags about
its "Mega Heatpipes".)

AMD markets a separate line of ["FirePro" graphics cards] intended for
professionals rather than gamers, although they appear to be based on the same
GPUs as their "Radeon" video cards. The [AMD FirePro W4100] is a normal
half-height PCI-E card that fits into a single PCI slot and has a relatively
small cooler with a single fan. It doesn't even require an auxilliary power
connection and is [about the same dimensions] as older video cards that I've
successfully used with Debian.

It was difficult to determine whether the W4100 card was actually supported by
an open source driver before buying it. The word "FirePro" appears nowhere on
the webpage for the [X.org Radeon driver], but I was able to find a "CAPE VERDE"
listed as an engineering name which appears to match the "Cape Verde" code name
for the FirePro W4100 given on Wikipedia's [List of AMD graphics processing
units]. This explains the "verde" string that appears in the firmware filenames
requested by the kernel (available only in the [non-free/firmware-amd-graphics
package]):

``` .boxed
[drm] initializing kernel modesetting (VERDE 0x1002:0x682C 0x1002:0x2B1E).
[drm] Loading verde Microcode
radeon 0000:01:00.0: firmware: direct-loading firmware radeon/verde_pfp.bin
radeon 0000:01:00.0: firmware: direct-loading firmware radeon/verde_me.bin
radeon 0000:01:00.0: firmware: direct-loading firmware radeon/verde_ce.bin
radeon 0000:01:00.0: firmware: direct-loading firmware radeon/verde_rlc.bin
radeon 0000:01:00.0: firmware: direct-loading firmware radeon/verde_mc.bin
radeon 0000:01:00.0: firmware: direct-loading firmware radeon/verde_smc.bin
```

The card appears in `lspci` like this:

``` .boxed
01:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Cape Verde GL [FirePro W4100]
(prog-if 00 [VGA controller])
	Subsystem: Advanced Micro Devices, Inc. [AMD/ATI] Device 2b1e
	Flags: bus master, fast devsel, latency 0, IRQ 55
	Memory at e0000000 (64-bit, prefetchable) [size=256M]
	Memory at f7e00000 (64-bit, non-prefetchable) [size=256K]
	I/O ports at e000 [size=256]
	Expansion ROM at f7e40000 [disabled] [size=128K]
	Capabilities: [48] Vendor Specific Information: Len=08 <?>
	Capabilities: [50] Power Management version 3
	Capabilities: [58] Express Legacy Endpoint, MSI 00
	Capabilities: [a0] MSI: Enable+ Count=1/1 Maskable- 64bit+
	Capabilities: [100] Vendor Specific Information: ID=0001 Rev=1 Len=010 <?>
	Capabilities: [150] Advanced Error Reporting
	Capabilities: [200] #15
	Capabilities: [270] #19
	Kernel driver in use: radeon
```

The W4100 appears to work just fine, except for a few bizarre error messages
that are printed to the kernel log when the displays are woken from power saving
mode:

``` .boxed
[Sun Dec 13 00:24:41 2015] [drm:si_dpm_set_power_state [radeon]] *ERROR* si_enable_smc_cac failed
[Sun Dec 13 00:24:41 2015] [drm:si_dpm_set_power_state [radeon]] *ERROR* si_enable_smc_cac failed
[Sun Dec 13 00:24:41 2015] [drm:radeon_dp_link_train [radeon]] *ERROR* displayport link status failed
[Sun Dec 13 00:24:41 2015] [drm:radeon_dp_link_train [radeon]] *ERROR* clock recovery failed
[Sun Dec 13 00:24:41 2015] [drm:radeon_dp_link_train [radeon]] *ERROR* displayport link status failed
[Sun Dec 13 00:24:41 2015] [drm:radeon_dp_link_train [radeon]] *ERROR* clock recovery failed
[Sun Dec 13 00:24:41 2015] [drm:si_dpm_set_power_state [radeon]] *ERROR* si_enable_smc_cac failed
[Sun Dec 13 00:24:41 2015] [drm:radeon_dp_link_train [radeon]] *ERROR* displayport link status failed
[Sun Dec 13 00:24:41 2015] [drm:radeon_dp_link_train [radeon]] *ERROR* clock recovery failed
[Sun Dec 13 00:24:41 2015] [drm:radeon_dp_link_train [radeon]] *ERROR* displayport link status failed
[Sun Dec 13 00:24:41 2015] [drm:radeon_dp_link_train [radeon]] *ERROR* clock recovery failed
```

There don't appear to be any ill effects from these error messages, though. I
have the following package versions installed:

``` .boxed
||/ Name                          Version             Description
+++-=============================-===================-================================================
ii  firmware-amd-graphics         20151207-1          Binary firmware for AMD/ATI graphics chips
ii  linux-image-4.3.0-trunk-amd64 4.3-1~exp2          Linux 4.3 for 64-bit PCs
ii  xserver-xorg-video-radeon     1:7.6.1-1           X.Org X server -- AMD/ATI Radeon display driver
```

The [Supermicro X10SAE] motherboard has two PCI-E 3.0 slots, but they're listed
as functioning in either "16/NA" or "8/8" mode, which apparently means that
putting anything in the second slot (like the Intel 750 SSD, which uses an x4
link) causes the video card to run at a smaller x8 link width. This can be
verified by looking at the widths reported in the "LnkCap" and "LnkSta" lines in
the `lspci -vv` output:

``` .boxed
root@chase{0}:~# lspci -vv -s 01:00.0 | egrep '(LnkCap|LnkSta):'
		LnkCap:	Port #0, Speed 8GT/s, Width x16, ASPM L0s L1, Exit Latency L0s <64ns, L1 <1us
		LnkSta:	Speed 8GT/s, Width x8, TrErr- Train- SlotClk+ DLActive- BWMgmt- ABWMgmt-
root@chase{0}:~# 
```

I did not notice any visible artifacts or performance degradation because of
the smaller link width.

The `sensors` utility from the `lm-sensors` package is capable of reporting the
temperature of the GPU:

``` .boxed
root@chase{0}:~# sensors radeon-pci-0100
radeon-pci-0100
Adapter: PCI adapter
temp1:        +55.0°C  (crit = +120.0°C, hyst = +90.0°C)

root@chase{0}:~# 
```

## [Dell P2715Q] monitors

Two new 27" Dell monitors with a native resolution of 3840x2160 were attached
to the new graphics card. They replaced two ten year old [Dell 2001FP] monitors
with a native resolution of 1600x1200 that had experienced burn-in, providing
4.32 times as many pixels. (TV and monitor manufacturers now shamelessly refer
to the 3840x2160 resolution as ["4K" resolution] even though neither dimension
reaches 4000 pixels.)

There was very little to setup beyond plugging the DisplayPort inputs on these
monitors into the DisplayPort outputs on the graphics card. Most of the setup
involved reconfiguring software to work with the very high resolution.

X.org, for tl;dr [CLOSED NOTABUG] reasons doesn't set the DPI correctly. These
monitors have ~163 DPI resolution, so I added `-dpi 168` to
`/etc/X11/xdm/Xservers`. (168 is an even 1.75x multiple of 96.) Software like
Google Chrome and xfce4-terminal rendered fonts and graphical elements at the
right size, but other software like notion, pidgin, and virt-manager did not
fully understand the high DPI. E.g., pidgin renders fonts at the correct size,
but icons are too small.

The default X cursor was also too small. To fix this, I installed the
[dmz-cursor-theme package], ran `update-alternatives --config x-cursor-theme`
and selected `/usr/share/icons/DMZ-Black/cursor.theme` as the cursor theme.

Overall, these displays are much brighter and more readable than the ones they
replaced.


[Intel SSD 750 series]: http://www.intel.com/content/www/us/en/solid-state-drives/solid-state-drives-750-series.html
[AMD FirePro W4100]: http://www.amd.com/en-us/products/graphics/workstation/firepro-3d/4100
[Dell P2715Q]: http://accessories.us.dell.com/sna/productdetail.aspx?c=us&cs=04&l=en&sku=210-ADOF
[NVM Express]: https://en.wikipedia.org/wiki/NVM_Express
[grub-installer]: https://tracker.debian.org/pkg/grub-installer
[Supermicro X10SAE]: http://www.supermicro.com/products/motherboard/Xeon/C220/X10SAE.cfm
[standard height PCI bracket]: https://commons.wikimedia.org/wiki/File:Intel_SSD_750_series,_400_GB_add-in_card_model,_top_view.jpg
[fails to read SMART data]: http://marc.info/?l=smartmontools-support&m=141555614628846&w=2
[infamous SSDs have]: http://www.anandtech.com/show/9196/samsung-releases-second-840-evo-fix
["4K" resolution]: https://en.wikipedia.org/wiki/4K_resolution#Ultra_HD
[appear to be marketed towards video gamers]: http://femfreq.tumblr.com/image/84553495875
[ASUS STRIX R9 390X]: https://www.asus.com/us/Graphics-Cards/STRIXR9390XDC3OC8GD5GAMING/
["FirePro" graphics cards]: https://en.wikipedia.org/wiki/AMD_FirePro
[about the same dimensions]: https://commons.wikimedia.org/wiki/File:Trident_video_card.png
[X.org Radeon driver]: http://xorg.freedesktop.org/wiki/RadeonFeature/
[non-free/firmware-amd-graphics package]: https://tracker.debian.org/pkg/firmware-nonfree
[List of AMD graphics processing units]: https://en.wikipedia.org/wiki/List_of_AMD_graphics_processing_units#FirePro_Workstation_Series_.28Wx100.29
[Dell 2001FP]: http://www.dell.com/downloads/global/products/monitors/en/spec_2001fp_en.pdf
[CLOSED NOTABUG]: https://bugs.freedesktop.org/show_bug.cgi?id=23705
[dmz-cursor-theme package]: https://tracker.debian.org/pkg/dmz-cursor-theme
