## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: GCSPOPCX -- A64 | **Class**: `system` | **XML ID**: `GCSPOPCX_SYS`

**Architecture**: `FEAT_GCS` (ARMv9.4)

**Summary**: Guarded Control Stack pop and compare exception return record

**Description**:
This instruction loads an
exception return record from the location indicated by the current Guarded
control stack pointer register, compares the loaded values with the current
ELR_ELx, SPSR_ELx, and LR, and increments the pointer by the size of a
Guarded Control Stack exception return record.

### Variant: `System`
- **Assembly**: `GCSPOPCX`
- **Alias of**: `SYS  #0, C7, C7, #5{, <Xt>}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  000 0111 0111 101 Rt  |
```

---
<details><summary>Metadata</summary>

- alias_mnemonic: `GCSPOPCX`
- isa: `A64`
- source: `gcspopcx_sys.xml`
</details>