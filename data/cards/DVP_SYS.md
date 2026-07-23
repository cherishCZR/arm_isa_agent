## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: DVP -- A64 | **Class**: `system` | **XML ID**: `DVP_SYS`

**Architecture**: `FEAT_SPECRES` (PROFILE_R)

**Summary**: Data value prediction restriction by context

**Description**:
This instruction prevents
data value predictions that predict execution addresses
based on information gathered from earlier execution within
a particular execution context. Data value predictions
determined by the actions of code in the target execution
context or contexts appearing in program order before the
instruction cannot be used to exploitatively control speculative
execution occurring after the instruction is complete and synchronized.

For more information, see
DVP RCTX, Data Value Prediction Restriction by Context.

### Variant: `System`
- **Assembly**: `DVP  RCTX, <Xt>`
- **Alias of**: `SYS  #3, C7, C3, #5, <Xt>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  011 0111 0011 101 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose source register, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `DVP`
- isa: `A64`
- source: `dvp_sys.xml`
</details>