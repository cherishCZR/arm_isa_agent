## STADD_LDADD `[ALIAS]`
_ARM A64 Instruction_ (Alias of ldadd.xml)

**Title**: STADD, STADDL -- A64 | **Class**: `general` | **XML ID**: `STADD_LDADD`

**Architecture**: `FEAT_LSE` (ARMv8.1)

**Summary**: Atomic add on word or doubleword in memory, without return

**Description**:
This instruction
atomically loads a 32-bit word or 64-bit doubleword from memory, adds the value
held in a register to it, and stores the result back to memory.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Integer (STADD_LDADD_32_memop)` (32-bit no memory ordering)
- **Condition**: `size == 10 && R == 0`
- **Assembly**: `STADD  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????0???????0?`
- **Alias of**: `LDADD  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  0   R   1   Rs  0   000 00  Rn  11111 |
```

### Variant: `Integer (STADDL_LDADDL_32_memop)` (32-bit release)
- **Condition**: `size == 10 && R == 1`
- **Assembly**: `STADDL  <Ws>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????1???????0?`
- **Alias of**: `LDADDL  <Ws>, WZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  0   R   1   Rs  0   000 00  Rn  11111 |
```

### Variant: `Integer (STADD_LDADD_64_memop)` (64-bit no memory ordering)
- **Condition**: `size == 11 && R == 0`
- **Assembly**: `STADD  <Xs>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????0???????1?`
- **Alias of**: `LDADD  <Xs>, XZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  0   R   1   Rs  0   000 00  Rn  11111 |
```

### Variant: `Integer (STADDL_LDADDL_64_memop)` (64-bit release)
- **Condition**: `size == 11 && R == 1`
- **Assembly**: `STADDL  <Xs>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????1???????1?`
- **Alias of**: `LDADDL  <Xs>, XZR, [<Xn|SP>]`
  Condition: Unconditionally
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  0   R   1   Rs  0   000 00  Rn  11111 |
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
- source: `stadd_ldadd.xml`
</details>