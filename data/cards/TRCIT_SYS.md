## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: TRCIT -- A64 | **Class**: `system` | **XML ID**: `TRCIT_SYS`

**Architecture**: `FEAT_ITE` (ARMv9.4)

**Summary**: Trace instrumentation

**Description**:
This instruction generates an instrumentation trace packet
that contains the value of the provided register.

### Variant: `System`
- **Assembly**: `TRCIT  <Xt>`
- **Alias of**: `SYS  #3, C7, C2, #7, <Xt>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  011 0111 0010 111 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose source register, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `TRCIT`
- isa: `A64`
- source: `trcit_sys.xml`
</details>