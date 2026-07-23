## STSMIN_LDSMIN `[ALIAS]`
_ARM A64 Instruction_ (Alias of ldsmin.xml)

**Title**: STSMIN, STSMINL -- A64 | **Class**: `general` | **XML ID**: `STSMIN_LDSMIN`

**Architecture**: `FEAT_LSE` (ARMv8.1)

**Summary**: Atomic signed minimum on word or doubleword in memory, without return

**Description**:
This instruction
atomically loads a 32-bit word or 64-bit doubleword from memory,
compares it against the value held in a register,
and stores the smaller value back to memory,
treating the values as signed numbers.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Integer (STSMIN_LDSMIN_32_memop)` (32-bit no memory ordering)
- **Condition**: `size == 10 && R == 0`
- **Assembly**: `STSMIN  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????0???????0?`
- **Alias of**: `LDSMIN  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  0   R   1   Rs  0   101 00  Rn  11111 |
```

### Variant: `Integer (STSMINL_LDSMINL_32_memop)` (32-bit release)
- **Condition**: `size == 10 && R == 1`
- **Assembly**: `STSMINL  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????1???????0?`
- **Alias of**: `LDSMINL  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  0   R   1   Rs  0   101 00  Rn  11111 |
```

### Variant: `Integer (STSMIN_LDSMIN_64_memop)` (64-bit no memory ordering)
- **Condition**: `size == 11 && R == 0`
- **Assembly**: `STSMIN  <Xs>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????0???????1?`
- **Alias of**: `LDSMIN  <Xs>, XZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  0   R   1   Rs  0   101 00  Rn  11111 |
```

### Variant: `Integer (STSMINL_LDSMINL_64_memop)` (64-bit release)
- **Condition**: `size == 11 && R == 1`
- **Assembly**: `STSMINL  <Xs>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????1???????1?`
- **Alias of**: `LDSMINL  <Xs>, XZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  0   R   1   Rs  0   101 00  Rn  11111 |
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
- source: `stsmin_ldsmin.xml`
</details>