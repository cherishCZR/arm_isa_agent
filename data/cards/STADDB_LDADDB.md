## STADDB_LDADDB `[ALIAS]`
_ARM A64 Instruction_ (Alias of ldaddb.xml)

**Title**: STADDB, STADDLB -- A64 | **Class**: `general` | **XML ID**: `STADDB_LDADDB`

**Architecture**: `FEAT_LSE` (ARMv8.1)

**Summary**: Atomic add on byte in memory, without return

**Description**:
This instruction
atomically loads an 8-bit byte from memory, adds the value held in a register
to it, and stores the result back to memory.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Integer (STADDB_LDADDB_32_memop)` (No memory ordering)
- **Condition**: `R == 0`
- **Assembly**: `STADDB  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `R`=`0`
- **Bit Pattern**: `??????????????????????0?????????`
- **Alias of**: `LDADDB  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 0   00  0   R   1   Rs  0   000 00  Rn  11111 |
```

### Variant: `Integer (STADDLB_LDADDLB_32_memop)` (Release)
- **Condition**: `R == 1`
- **Assembly**: `STADDLB  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `R`=`1`
- **Bit Pattern**: `??????????????????????1?????????`
- **Alias of**: `LDADDLB  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 0   00  0   R   1   Rs  0   000 00  Rn  11111 |
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
- source: `staddb_ldaddb.xml`
</details>