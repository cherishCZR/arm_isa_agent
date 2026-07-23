## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: GCSPUSHX -- A64 | **Class**: `system` | **XML ID**: `GCSPUSHX_SYS`

**Architecture**: `FEAT_GCS` (ARMv9.4)

**Summary**: Guarded Control Stack push exception return record

**Description**:
This instruction decrements the current
Guarded Control Stack pointer register by the size of a Guarded Control Stack
exception return record and stores an exception return record to the Guarded
Control Stack.

### Variant: `System`
- **Assembly**: `GCSPUSHX`
- **Alias of**: `SYS  #0, C7, C7, #4{, <Xt>}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  000 0111 0111 100 Rt  |
```

---
<details><summary>Metadata</summary>

- alias_mnemonic: `GCSPUSHX`
- isa: `A64`
- source: `gcspushx_sys.xml`
</details>