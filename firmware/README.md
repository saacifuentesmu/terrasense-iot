# firmware

Sensor-node firmware — **nRF Connect SDK / Zephyr**, target **nRF52840** (DK now).

## Responsibilities
- Read SHT4x (T/RH) and, on CO₂ nodes, SCD41 over I²C.
- Join the Thread mesh; report telemetry to the bridge over CoAP (see
  [../docs/data-contract.md](../docs/data-contract.md)).
- Sleep between samples (Sleepy End Device) for battery nodes.
- (Stretch) BLE commissioning/config concurrently with Thread — see
  [ADR-0001](../docs/decisions/0001-nrf-over-esp.md).

## Board abstraction
All pins/peripherals in **devicetree** under `boards/` — dev kit and future custom board
are two board definitions over one app (PROC-03 / [ADR-0003](../docs/decisions/0003-devkit-to-custom-board.md)).

## Build (to fill in Phase 1)
```
west build -b nrf52840dk/nrf52840 app
west flash
```
