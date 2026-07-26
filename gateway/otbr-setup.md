# Border router bring-up runbook (Phase 2)

Target: **Raspberry Pi 4 + nRF52840 dongle (PCA10059)** as RCP, per
[ADR-0004](../docs/decisions/0004-border-router-platform.md). Done when `ot-ctl state`
says `leader` and the bridge runs on the Pi (POC-05).

## 1. Flash the dongle as RCP (on the PC)

Build OpenThread's `ot-rcp` and push it over the dongle's built-in USB bootloader —
no debugger needed:

```bash
git clone https://github.com/openthread/ot-nrf528xx && cd ot-nrf528xx
./script/bootstrap
./script/build nrf52840 USB_trans -DOT_BOOTLOADER=USB
arm-none-eabi-objcopy -O ihex build/bin/ot-rcp ot-rcp.hex
nrfutil pkg generate --hw-version 52 --sd-req 0 \
  --application ot-rcp.hex --application-version 1 rcp.zip
# press the side RESET button → red LED pulses = bootloader mode
nrfutil dfu usb-serial -pkg rcp.zip -p /dev/ttyACM0
```

Alternative: the NCS `coprocessor` sample (`west build -b nrf52840dongle/nrf52840`)
produces the same RCP if staying inside the Nordic toolchain is preferred.

## 2. OTBR on the Pi

Raspberry Pi OS Lite 64-bit, Docker installed, then:

```bash
sudo docker run -d --name otbr --restart unless-stopped --network host --privileged \
  -v /dev/ttyACM0:/dev/ttyACM0 openthread/otbr \
  --radio-url spinel+hdlc+uart:///dev/ttyACM0
```

> **RF gotcha:** the Pi 4's USB3 ports radiate broadband noise into 2.4 GHz. Put the
> dongle on a **USB2 port, on a short extension cable**, away from the board — or later
> range problems will look like mesh bugs.

## 3. Form the Thread network

```bash
sudo docker exec -it otbr ot-ctl dataset init new
sudo docker exec -it otbr ot-ctl dataset commit active
sudo docker exec -it otbr ot-ctl ifconfig up
sudo docker exec -it otbr ot-ctl thread start
sudo docker exec -it otbr ot-ctl state          # → "leader" = POC-05 done
sudo docker exec -it otbr ot-ctl dataset active -x   # hex blob — SAVE THIS
```

The active-dataset hex is what sensor nodes use to join the mesh. It contains the
**network key — keep it out of git**; store it with the service-account JSON
(both already gitignored).

## 4. Bridge on the Pi

Clone this repo on the Pi and follow [README.md](README.md) — run
`python -m bridge --dry-run` on the Pi, then `tools/simnode.py --host <pi-ip>` from
another machine. That proves the Pi hosts the full gateway role before any firmware
exists.

## Record as you go

Log exact hardware (dongle revision, Pi model, OS image, container tag) in
[../docs/hardware.md](../docs/hardware.md) — that's the traceability the PoC summary
(POC-11) cites.
