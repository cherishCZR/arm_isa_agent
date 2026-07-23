## SYS `[ALIAS]`
_ARM A64 Instruction_ (Alias of sys.xml)

**Title**: GCSSS1 -- A64 | **Class**: `system` | **XML ID**: `GCSSS1_SYS`

**Architecture**: `FEAT_GCS` (ARMv9.4)

**Summary**: Guarded Control Stack switch stack 1

**Description**:
This instruction validates that the stack being
switched to contains a Valid cap entry, stores an In-progress cap entry to
the stack that is being switched to, and sets the current Guarded control
stack pointer to the stack that is being switched to.

If the instruction generates a synchronous Data Abort exception, Watchpoint exception,
GPC exception, or GCS Data Check exception, the value of GCSPR_ELx
for the current Exception level is restored to the value held in the register before
the instruction was executed.

### Variant: `System`
- **Assembly**: `GCSSS1  <Xt>`
- **Alias of**: `SYS  #3, C7, C7, #2, <Xt>`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  28  25  21 20  18  15  11   7   4  |
|--------------------------------|
| 110 101 0100 0   01  011 0111 0111 010 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose source register, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- alias_mnemonic: `GCSSS1`
- isa: `A64`
- source: `gcsss1_sys.xml`
</details>