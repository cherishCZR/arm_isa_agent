## STUMAXH_LDUMAXH `[ALIAS]`
_ARM A64 Instruction_ (Alias of ldumaxh.xml)

**Title**: STUMAXH, STUMAXLH -- A64 | **Class**: `general` | **XML ID**: `STUMAXH_LDUMAXH`

**Architecture**: `FEAT_LSE` (ARMv8.1)

**Summary**: Atomic unsigned maximum on halfword in memory, without return

**Description**:
This instruction
atomically loads a 16-bit halfword from memory,
compares it against the value held in a register,
and stores the larger value back to memory,
treating the values as unsigned numbers.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Integer (STUMAXH_LDUMAXH_32_memop)` (No memory ordering)
- **Condition**: `R == 0`
- **Assembly**: `STUMAXH  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `R`=`0`
- **Bit Pattern**: `??????????????????????0?????????`
- **Alias of**: `LDUMAXH  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 01  111 0   00  0   R   1   Rs  0   110 00  Rn  11111 |
```

### Variant: `Integer (STUMAXLH_LDUMAXLH_32_memop)` (Release)
- **Condition**: `R == 1`
- **Assembly**: `STUMAXLH  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `R`=`1`
- **Bit Pattern**: `??????????????????????1?????????`
- **Alias of**: `LDUMAXLH  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 01  111 0   00  0   R   1   Rs  0   110 00  Rn  11111 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the general-purpose register holding the data value to be operated on with the contents of the memory location, encoded in the " |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `stumaxh_ldumaxh.xml`
</details>