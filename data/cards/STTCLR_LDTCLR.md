## STTCLR_LDTCLR `[ALIAS]`
_ARM A64 Instruction_ (Alias of ldtclr.xml)

**Title**: STTCLR, STTCLRL -- A64 | **Class**: `general` | **XML ID**: `STTCLR_LDTCLR`

**Architecture**: `FEAT_LSUI` (ARMv9.6)

**Summary**: Atomic bit clear unprivileged, without return

**Description**:
This instruction
atomically loads a 32-bit word or 64-bit doubleword from memory, performs a
bitwise AND with the complement of the value held in a register on
it, and stores the result back to memory.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Integer (STTCLR_LDTCLR_32_memop_unpriv)` (32-bit no memory ordering)
- **Condition**: `sz == 0 && R == 0`
- **Assembly**: `STTCLR  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????0???????0?`
- **Alias of**: `LDTCLR  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 0   R   1   Rs  0   001 01  Rn  11111 |
```

### Variant: `Integer (STTCLRL_LDTCLRL_32_memop_unpriv)` (32-bit release)
- **Condition**: `sz == 0 && R == 1`
- **Assembly**: `STTCLRL  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????1???????0?`
- **Alias of**: `LDTCLRL  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 0   R   1   Rs  0   001 01  Rn  11111 |
```

### Variant: `Integer (STTCLR_LDTCLR_64_memop_unpriv)` (64-bit no memory ordering)
- **Condition**: `sz == 1 && R == 0`
- **Assembly**: `STTCLR  <Xs>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????0???????1?`
- **Alias of**: `LDTCLR  <Xs>, XZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 0   R   1   Rs  0   001 01  Rn  11111 |
```

### Variant: `Integer (STTCLRL_LDTCLRL_64_memop_unpriv)` (64-bit release)
- **Condition**: `sz == 1 && R == 1`
- **Assembly**: `STTCLRL  <Xs>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????1???????1?`
- **Alias of**: `LDTCLRL  <Xs>, XZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 0   R   1   Rs  0   001 01  Rn  11111 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the general-purpose register holding the data value to be operated on with the contents of the memory location, encoded in the " |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Xs>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the general-purpose register holding the data value to be operated on with the contents of the memory location, encoded in the " |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sttclr_ldtclr.xml`
</details>