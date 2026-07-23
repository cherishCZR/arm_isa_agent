## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: CFP -- A64 | **Class**: `system` | **XML ID**: `CFP_SYS`

**Architecture**: `FEAT_SPECRES` (PROFILE_R)

**Summary**: Control flow prediction restriction by context

**Description**:
This instruction prevents
control flow predictions that predict execution addresses
based on information gathered from earlier execution within
a particular execution context. Control flow predictions
determined by the actions of code in the target execution
context or contexts appearing in program order before the
instruction cannot be used to exploitatively control speculative
execution occurring after the instruction is complete and synchronized.

For more information, see
CFP RCTX, Control Flow Prediction Restriction by Context.

### Variant: `System`
- **Assembly**: `CFP  RCTX, <Xt>`
- **Alias of**: `SYS  #3, C7, C3, #4, <Xt>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  011 0111 0011 100 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose source register, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `CFP`
- isa: `A64`
- source: `cfp_sys.xml`
</details>