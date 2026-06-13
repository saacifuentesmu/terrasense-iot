# hardware

Node hardware — dev kits now, custom module-based board later
([ADR-0003](../docs/decisions/0003-devkit-to-custom-board.md)).

## v1 (demo) — off-the-shelf
- nRF52840 DK (or Xiao nRF52840 for a smaller form factor)
- SHT4x breakout (T/RH), SCD41 breakout (CO₂) on at least one node
- Mains/USB power for v1; battery (2×AA) as a stretch

## Later — custom board
- Pre-certified nRF52840 module (Raytac MDBT50Q / Fanstel BT840)
- I²C sensor headers, power (LDO / boost for AA), test points
- Enclosure: vented sensor opening with PTFE membrane for 95 %RH rooms (ENV-02)

## Contents (as produced)
- `bom/` — bills of materials
- `schematic/`, `layout/` — KiCad files
- Reference: schematic-review / DFM checklists live in `seekio-internal/docs/qms/checklists/`
