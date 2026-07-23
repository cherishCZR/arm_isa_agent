## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: GCSPUSHM -- A64 | **Class**: `system` | **XML ID**: `GCSPUSHM_SYS`

**Architecture**: `FEAT_GCS` (ARMv9.4)

**Summary**: Guarded Control Stack push

**Description**:
This instruction decrements the current Guarded Control Stack
pointer register by the size of a Guarded control procedure return record
and stores an entry to the Guarded Control Stack.

### Variant: `System`
- **Assembly**: `GCSPUSHM  <Xt>`
- **Alias of**: `SYS  #3, C7, C7, #0, <Xt>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  011 0111 0111 000 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose source register, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `GCSPUSHM`
- isa: `A64`
- source: `gcspushm_sys.xml`
</details>