## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: COSP -- A64 | **Class**: `system` | **XML ID**: `COSP_SYS`

**Architecture**: `FEAT_SPECRES2` (ARMv8.9)

**Summary**: Clear other speculative prediction restriction by context

**Description**:
This instruction prevents predictions,
other than Cache prefetch, Control flow, and Data Value predictions,
that predict execution addresses based on information gathered from
earlier execution within a particular execution context.
Predictions, other than Cache prefetch, Control flow, and
Data Value predictions, determined by the actions of code in the target
execution context or contexts appearing in program order before
the instruction cannot exploitatively control any speculative access
occurring after the instruction is complete and synchronized.

### Variant: `System`
- **Assembly**: `COSP  RCTX, <Xt>`
- **Alias of**: `SYS  #3, C7, C3, #6, <Xt>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  011 0111 0011 110 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose source register, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `COSP`
- isa: `A64`
- source: `cosp_sys.xml`
</details>