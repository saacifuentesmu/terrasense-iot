---
doc-id: TS-HW-001
title: TerraSense IoT — PoC Hardware Inventory
version: "0.1"
status: draft
owner: Studio Lead
last-reviewed: 2026-07-12
---

# PoC Hardware Inventory (v0.1)

What the PoC actually runs on. Fill in exact models/revisions at the bench audit;
the provenance column records ownership — only project-owned equipment is used.

## Roles

| Role | Hardware | Exact model / rev | Provenance | Notes |
|------|----------|-------------------|------------|-------|
| Border router host | Raspberry Pi 4 | TBD (RAM, OS image) | TBD | [otbr-setup.md](../gateway/otbr-setup.md) |
| RCP radio | nRF52840 dongle PCA10059 | TBD (qty) | TBD | flashed as `ot-rcp` |
| Sensor node MCU | nRF52840 breakout | **TBD at bench audit** | TBD | needs exposed I²C + programming path |
| SWD probe | TBD | TBD | TBD | needed unless node board has UF2/DFU |
| T/RH sensor | TBD | TBD — RTM says SHT4x (POC-01) | TBD | if it's SHT3x/BME280/SCD4x instead, amend POC-01, don't deviate silently |
| CO₂ sensor | TBD | TBD | TBD | deferred to system RTM (MEAS-03); inventory anyway |

## Bench audit checklist

- [ ] Identify each nRF52840 board: exact product, onboard debugger yes/no, USB bootloader yes/no
- [ ] Identify sensor part numbers; check Zephyr driver exists upstream
- [ ] Confirm an SWD probe is available if the node board lacks a bootloader
- [ ] Confirm provenance: all equipment project-owned
- [ ] Update this table + amend POC-01 if the sensor differs from SHT4x
