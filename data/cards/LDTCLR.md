## LDTCLR
_ARM A64 Instruction_

**Title**: LDTCLR, LDTCLRA, LDTCLRAL, LDTCLRL -- A64 | **Class**: `general` | **XML ID**: `LDTCLR`

**Architecture**: `FEAT_LSUI` (ARMv9.6)

**Summary**: Atomic bit clear unprivileged

**Description**:
This instruction atomically loads a 32-bit word or
64-bit doubleword from memory, performs a
bitwise AND with the complement of the value held in a register on
it, and stores the result back to memory.
The value initially loaded from memory is returned in the destination register.

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

Explicit Memory  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

### Variant: `Integer (LDTCLR_32_memop_unpriv)` (32-bit no memory ordering)
- **Condition**: `sz == 0 && A == 0 && R == 0`
- **Assembly**: `LDTCLR  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`0`, `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00??????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 A   R   1   Rs  0   001 01  Rn  Rt  |
```

#### Decode (A64.ldst.memop_unpriv.LDTCLR_32_memop_unpriv)

```
if !IsFeatureImplemented(FEAT_LSUI) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);

constant integer datasize = 32 << UInt(sz);
constant integer regsize = if datasize == 64 then 64 else 32;

constant boolean acquire = A == '1' && Rt != '11111';
constant boolean release = R == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.memop_unpriv.LDTCLR_32_memop_unpriv)

```
bits(64) address;

constant boolean privileged = AArch64.IsUnprivAccessPriv();
constant AccessDescriptor accdesc = CreateAccDescAtomicOp(MemAtomicOp_BIC, acquire, release,
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
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSUI)` |

### Variant: `Integer (LDTCLRA_32_memop_unpriv)` (32-bit acquire)
- **Condition**: `sz == 0 && A == 1 && R == 0`
- **Assembly**: `LDTCLRA  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`0`, `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01??????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 A   R   1   Rs  0   001 01  Rn  Rt  |
```

### Variant: `Integer (LDTCLRAL_32_memop_unpriv)` (32-bit acquire-release)
- **Condition**: `sz == 0 && A == 1 && R == 1`
- **Assembly**: `LDTCLRAL  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`0`, `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11??????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 A   R   1   Rs  0   001 01  Rn  Rt  |
```

### Variant: `Integer (LDTCLRL_32_memop_unpriv)` (32-bit release)
- **Condition**: `sz == 0 && A == 0 && R == 1`
- **Assembly**: `LDTCLRL  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`0`, `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10??????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 A   R   1   Rs  0   001 01  Rn  Rt  |
```

### Variant: `Integer (LDTCLR_64_memop_unpriv)` (64-bit no memory ordering)
- **Condition**: `sz == 1 && A == 0 && R == 0`
- **Assembly**: `LDTCLR  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`1`, `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00??????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 A   R   1   Rs  0   001 01  Rn  Rt  |
```

### Variant: `Integer (LDTCLRA_64_memop_unpriv)` (64-bit acquire)
- **Condition**: `sz == 1 && A == 1 && R == 0`
- **Assembly**: `LDTCLRA  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`1`, `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01??????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 A   R   1   Rs  0   001 01  Rn  Rt  |
```

### Variant: `Integer (LDTCLRAL_64_memop_unpriv)` (64-bit acquire-release)
- **Condition**: `sz == 1 && A == 1 && R == 1`
- **Assembly**: `LDTCLRAL  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`1`, `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11??????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 A   R   1   Rs  0   001 01  Rn  Rt  |
```

### Variant: `Integer (LDTCLRL_64_memop_unpriv)` (64-bit release)
- **Condition**: `sz == 1 && A == 0 && R == 1`
- **Assembly**: `LDTCLRL  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `sz`=`1`, `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10??????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   sz  011001 A   R   1   Rs  0   001 01  Rn  Rt  |
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
- source: `ldtclr.xml`
</details>