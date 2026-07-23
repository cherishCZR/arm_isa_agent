## SWP
_ARM A64 Instruction_

**Title**: SWP, SWPA, SWPAL, SWPL -- A64 | **Class**: `general` | **XML ID**: `SWP`

**Architecture**: `FEAT_LSE` (ARMv8.1)

**Summary**: Swap word or doubleword in memory

**Description**:
This instruction
atomically loads a 32-bit word or 64-bit doubleword from a memory location,
and stores the value held in a register back to the same memory location.
The value initially loaded from memory is returned in the destination register.

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Integer (SWP_32_memop)` (32-bit SWP)
- **Condition**: `size == 10 && A == 0 && R == 0`
- **Assembly**: `SWP  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00??????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  1   000 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop.SWP_32_memop)

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

#### Execute (A64.ldst.memop.SWP_32_memop)

```
bits(64) address;
bits(datasize) data;
bits(datasize) store_value;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescAtomicOp(MemAtomicOp_SWP, acquire, release,
                                                          tagchecked, privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

store_value = X[s, datasize];

constant bits(datasize) comparevalue = bits(datasize) UNKNOWN; // Irrelevant when not executing CAS
data = MemAtomic(address, comparevalue, store_value, accdesc);

X[t, regsize] = ZeroExtend(data, regsize);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSE)` |

### Variant: `Integer (SWPA_32_memop)` (32-bit SWPA)
- **Condition**: `size == 10 && A == 1 && R == 0`
- **Assembly**: `SWPA  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01??????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  1   000 00  Rn  Rt  |
```

### Variant: `Integer (SWPAL_32_memop)` (32-bit SWPAL)
- **Condition**: `size == 10 && A == 1 && R == 1`
- **Assembly**: `SWPAL  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11??????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  1   000 00  Rn  Rt  |
```

### Variant: `Integer (SWPL_32_memop)` (32-bit SWPL)
- **Condition**: `size == 10 && A == 0 && R == 1`
- **Assembly**: `SWPL  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10??????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  1   000 00  Rn  Rt  |
```

### Variant: `Integer (SWP_64_memop)` (64-bit SWP)
- **Condition**: `size == 11 && A == 0 && R == 0`
- **Assembly**: `SWP  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00??????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  1   000 00  Rn  Rt  |
```

### Variant: `Integer (SWPA_64_memop)` (64-bit SWPA)
- **Condition**: `size == 11 && A == 1 && R == 0`
- **Assembly**: `SWPA  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01??????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  1   000 00  Rn  Rt  |
```

### Variant: `Integer (SWPAL_64_memop)` (64-bit SWPAL)
- **Condition**: `size == 11 && A == 1 && R == 1`
- **Assembly**: `SWPAL  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11??????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  1   000 00  Rn  Rt  |
```

### Variant: `Integer (SWPL_64_memop)` (64-bit SWPL)
- **Condition**: `size == 11 && A == 0 && R == 1`
- **Assembly**: `SWPL  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10??????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 1x  111 0   00  A   R   1   Rs  1   000 00  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the general-purpose register to be stored, encoded in the "Rs" field. |
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Xs>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the general-purpose register to be stored, encoded in the "Rs" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `swp.xml`
</details>