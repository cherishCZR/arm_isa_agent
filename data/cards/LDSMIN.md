## LDSMIN
_ARM A64 Instruction_

**Title**: LDSMIN, LDSMINA, LDSMINAL, LDSMINL -- A64 | **Class**: `general` | **XML ID**: `LDSMIN`

**Architecture**: `FEAT_LSE` (ARMv8.1)

**Summary**: Atomic signed minimum on word or doubleword in memory

**Description**:
This instruction
atomically loads a 32-bit word or 64-bit doubleword from memory,
compares it against the value held in a register,
and stores the smaller value back to memory,
treating the values as signed numbers.
The value initially loaded from memory is returned in the destination register.

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Integer (LDSMIN_32_memop)` (32-bit no memory ordering)
- **Condition**: `size == 10 && A == 0 && R == 0`
- **Assembly**: `LDSMIN  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00??????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  0   101 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop.LDSMIN_32_memop)

```
if !IsFeatureImplemented(FEAT_LSE) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);

constant integer datasize = 8 << UInt(size);
constant integer regsize = if datasize == 64 then 64 else 32;

constant boolean acquire = A == '1' && Rt != '11111';
constant boolean release = R == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.memop.LDSMIN_32_memop)

```
bits(64) address;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescAtomicOp(MemAtomicOp_SMIN, acquire, release,
                                                          tagchecked, privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant bits(datasize) comparevalue = bits(datasize) UNKNOWN; // Irrelevant when not executing CAS
constant bits(datasize) value = X[s, datasize];
constant bits(datasize) data = MemAtomic(address, comparevalue, value, accdesc);

if t != 31 then
    X[t, regsize] = ZeroExtend(data, regsize);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSE)` |

### Variant: `Integer (LDSMINA_32_memop)` (32-bit acquire)
- **Condition**: `size == 10 && A == 1 && R == 0`
- **Assembly**: `LDSMINA  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01??????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  0   101 00  Rn  Rt  |
```

### Variant: `Integer (LDSMINAL_32_memop)` (32-bit acquire-release)
- **Condition**: `size == 10 && A == 1 && R == 1`
- **Assembly**: `LDSMINAL  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11??????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  0   101 00  Rn  Rt  |
```

### Variant: `Integer (LDSMINL_32_memop)` (32-bit release)
- **Condition**: `size == 10 && A == 0 && R == 1`
- **Assembly**: `LDSMINL  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10??????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  0   101 00  Rn  Rt  |
```

### Variant: `Integer (LDSMIN_64_memop)` (64-bit no memory ordering)
- **Condition**: `size == 11 && A == 0 && R == 0`
- **Assembly**: `LDSMIN  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00??????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  0   101 00  Rn  Rt  |
```

### Variant: `Integer (LDSMINA_64_memop)` (64-bit acquire)
- **Condition**: `size == 11 && A == 1 && R == 0`
- **Assembly**: `LDSMINA  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01??????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  0   101 00  Rn  Rt  |
```

### Variant: `Integer (LDSMINAL_64_memop)` (64-bit acquire-release)
- **Condition**: `size == 11 && A == 1 && R == 1`
- **Assembly**: `LDSMINAL  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11??????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  0   101 00  Rn  Rt  |
```

### Variant: `Integer (LDSMINL_64_memop)` (64-bit release)
- **Condition**: `size == 11 && A == 0 && R == 1`
- **Assembly**: `LDSMINL  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10??????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  0   101 00  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the general-purpose register holding the data value to be operated on with the contents of the memory location, encoded in the " |
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Xs>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the general-purpose register holding the data value to be operated on with the contents of the memory location, encoded in the " |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ldsmin.xml`
</details>