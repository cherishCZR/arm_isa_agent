## STTSET_LDTSET `[ALIAS]`
_ARM A64 Instruction_ (Alias of ldtset.xml)

**Title**: STTSET, STTSETL -- A64 | **Class**: `general` | **XML ID**: `STTSET_LDTSET`

**Architecture**: `FEAT_LSUI` (ARMv9.6)

**Summary**: Atomic bit set unprivileged, without return

**Description**:
This instruction
atomically loads a 32-bit word or 64-bit doubleword from memory, performs a
bitwise OR with the value held in a register on
it, and stores the result back to memory.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Integer (STTSET_LDTSET_32_memop_unpriv)` (32-bit no memory ordering)
- **Condition**: `sz == 0 && R == 0`
- **Assembly**: `STTSET  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????0???????0?`
- **Alias of**: `LDTSET  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 0   R   1   Rs  0   011 01  Rn  11111 |
```

### Variant: `Integer (STTSETL_LDTSETL_32_memop_unpriv)` (32-bit release)
- **Condition**: `sz == 0 && R == 1`
- **Assembly**: `STTSETL  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????1???????0?`
- **Alias of**: `LDTSETL  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 0   R   1   Rs  0   011 01  Rn  11111 |
```

### Variant: `Integer (STTSET_LDTSET_64_memop_unpriv)` (64-bit no memory ordering)
- **Condition**: `sz == 1 && R == 0`
- **Assembly**: `STTSET  <Xs>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????0???????1?`
- **Alias of**: `LDTSET  <Xs>, XZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 0   R   1   Rs  0   011 01  Rn  11111 |
```

### Variant: `Integer (STTSETL_LDTSETL_64_memop_unpriv)` (64-bit release)
- **Condition**: `sz == 1 && R == 1`
- **Assembly**: `STTSETL  <Xs>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????1???????1?`
- **Alias of**: `LDTSETL  <Xs>, XZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 0   R   1   Rs  0   011 01  Rn  11111 |
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
- source: `sttset_ldtset.xml`
</details>