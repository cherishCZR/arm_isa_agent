## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: GCSPOPX -- A64 | **Class**: `system` | **XML ID**: `GCSPOPX_SYS`

**Architecture**: `FEAT_GCS` (ARMv9.4)

**Summary**: Guarded Control Stack pop exception return record

**Description**:
This instruction loads an exception return
record from the location indicated by the current Guarded Control Stack
pointer register, checks that the record is an exception return record, and
increments the pointer by the size of a Guarded Control Stack exception
return record.

### Variant: `System`
- **Assembly**: `GCSPOPX`
- **Alias of**: `SYS  #0, C7, C7, #6{, <Xt>}`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  000 0111 0111 110 Rt  |
```

---
<details><summary>Metadata</summary>

- alias_mnemonic: `GCSPOPX`
- isa: `A64`
- source: `gcspopx_sys.xml`
</details>