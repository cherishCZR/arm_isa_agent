## STCLR_LDCLR `[ALIAS]`
_ARM A64 Instruction_ (Alias of ldclr.xml)

**Title**: STCLR, STCLRL -- A64 | **Class**: `general` | **XML ID**: `STCLR_LDCLR`

**Architecture**: `FEAT_LSE` (ARMv8.1)

**Summary**: Atomic bit clear on word or doubleword in memory, without return

**Description**:
This instruction
atomically loads a 32-bit word or 64-bit doubleword from memory, performs a
bitwise AND with the complement of the value held in a register on
it, and stores the result back to memory.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Integer (STCLR_LDCLR_32_memop)` (32-bit no memory ordering)
- **Condition**: `size == 10 && R == 0`
- **Assembly**: `STCLR  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????0???????0?`
- **Alias of**: `LDCLR  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  0   R   1   Rs  0   001 00  Rn  11111 |
```

### Variant: `Integer (STCLRL_LDCLRL_32_memop)` (32-bit release)
- **Condition**: `size == 10 && R == 1`
- **Assembly**: `STCLRL  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????1???????0?`
- **Alias of**: `LDCLRL  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  0   R   1   Rs  0   001 00  Rn  11111 |
```

### Variant: `Integer (STCLR_LDCLR_64_memop)` (64-bit no memory ordering)
- **Condition**: `size == 11 && R == 0`
- **Assembly**: `STCLR  <Xs>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????0???????1?`
- **Alias of**: `LDCLR  <Xs>, XZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  0   R   1   Rs  0   001 00  Rn  11111 |
```

### Variant: `Integer (STCLRL_LDCLRL_64_memop)` (64-bit release)
- **Condition**: `size == 11 && R == 1`
- **Assembly**: `STCLRL  <Xs>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????1???????1?`
- **Alias of**: `LDCLRL  <Xs>, XZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  0   R   1   Rs  0   001 00  Rn  11111 |
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
- source: `stclr_ldclr.xml`
</details>