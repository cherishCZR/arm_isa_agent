## LDFMINNM
_ARM A64 Instruction_

**Title**: LDFMINNM, LDFMINNMA, LDFMINNMAL, LDFMINNML -- A64 | **Class**: `advsimd` | **XML ID**: `LDFMINNM`

**Architecture**: `FEAT_LSFE` (ARMv9.6)

**Summary**: Floating-point atomic minimum number in memory

**Description**:
This instruction atomically loads a 16-bit, 32-bit, or 64-bit value from memory,
computes the floating-point minimum number with the value held in a register,
and stores the result back to memory.
The value initially loaded from memory is returned in the destination register.

This instruction:

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Floating-point (LDFMINNM_16)` (Half-precision no memory ordering)
- **Condition**: `size == 01 && A == 0 && R == 0`
- **Assembly**: `LDFMINNM  <Hs>, <Ht>, [<Xn|SP>]`
- **Fixed bits**: `size`=`01`, `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00??????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  A   R   1   Rs  0   111 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop.LDFMINNM_16)

```
if !IsFeatureImplemented(FEAT_LSFE) then EndOfDecode(Decode_UNDEF);

constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer s = UInt(Rs);

constant integer datasize = 8 << UInt(size);
constant boolean acquire = A == '1';
constant boolean release = R == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.memop.LDFMINNM_16)

```
CheckFPEnabled64();
bits(64) address;
bits(datasize) value;
bits(datasize) data;
constant AccessDescriptor accdesc = CreateAccDescFPAtomicOp(MemAtomicOp_FPMINNM, acquire,
                                                            release, tagchecked);

value = V[s, datasize];
if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant bits(datasize) comparevalue = bits(datasize) UNKNOWN; // Irrelevant when not executing CAS
data = MemAtomic(address, comparevalue, value, accdesc);

V[t, datasize] = data;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSFE)` |

### Variant: `Floating-point (LDFMINNMA_16)` (Half-precision acquire)
- **Condition**: `size == 01 && A == 1 && R == 0`
- **Assembly**: `LDFMINNMA  <Hs>, <Ht>, [<Xn|SP>]`
- **Fixed bits**: `size`=`01`, `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01??????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  A   R   1   Rs  0   111 00  Rn  Rt  |
```

### Variant: `Floating-point (LDFMINNMAL_16)` (Half-precision acquire-release)
- **Condition**: `size == 01 && A == 1 && R == 1`
- **Assembly**: `LDFMINNMAL  <Hs>, <Ht>, [<Xn|SP>]`
- **Fixed bits**: `size`=`01`, `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11??????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  A   R   1   Rs  0   111 00  Rn  Rt  |
```

### Variant: `Floating-point (LDFMINNML_16)` (Half-precision release)
- **Condition**: `size == 01 && A == 0 && R == 1`
- **Assembly**: `LDFMINNML  <Hs>, <Ht>, [<Xn|SP>]`
- **Fixed bits**: `size`=`01`, `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10??????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  A   R   1   Rs  0   111 00  Rn  Rt  |
```

### Variant: `Floating-point (LDFMINNM_32)` (Single-precision no memory ordering)
- **Condition**: `size == 10 && A == 0 && R == 0`
- **Assembly**: `LDFMINNM  <Ss>, <St>, [<Xn|SP>]`
- **Fixed bits**: `size`=`10`, `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00??????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  A   R   1   Rs  0   111 00  Rn  Rt  |
```

### Variant: `Floating-point (LDFMINNMA_32)` (Single-precision acquire)
- **Condition**: `size == 10 && A == 1 && R == 0`
- **Assembly**: `LDFMINNMA  <Ss>, <St>, [<Xn|SP>]`
- **Fixed bits**: `size`=`10`, `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01??????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  A   R   1   Rs  0   111 00  Rn  Rt  |
```

### Variant: `Floating-point (LDFMINNMAL_32)` (Single-precision acquire-release)
- **Condition**: `size == 10 && A == 1 && R == 1`
- **Assembly**: `LDFMINNMAL  <Ss>, <St>, [<Xn|SP>]`
- **Fixed bits**: `size`=`10`, `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11??????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  A   R   1   Rs  0   111 00  Rn  Rt  |
```

### Variant: `Floating-point (LDFMINNML_32)` (Single-precision release)
- **Condition**: `size == 10 && A == 0 && R == 1`
- **Assembly**: `LDFMINNML  <Ss>, <St>, [<Xn|SP>]`
- **Fixed bits**: `size`=`10`, `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10??????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  A   R   1   Rs  0   111 00  Rn  Rt  |
```

### Variant: `Floating-point (LDFMINNM_64)` (Double-precision no memory ordering)
- **Condition**: `size == 11 && A == 0 && R == 0`
- **Assembly**: `LDFMINNM  <Ds>, <Dt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`11`, `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00??????11`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  A   R   1   Rs  0   111 00  Rn  Rt  |
```

### Variant: `Floating-point (LDFMINNMA_64)` (Double-precision acquire)
- **Condition**: `size == 11 && A == 1 && R == 0`
- **Assembly**: `LDFMINNMA  <Ds>, <Dt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`11`, `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01??????11`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  A   R   1   Rs  0   111 00  Rn  Rt  |
```

### Variant: `Floating-point (LDFMINNMAL_64)` (Double-precision acquire-release)
- **Condition**: `size == 11 && A == 1 && R == 1`
- **Assembly**: `LDFMINNMAL  <Ds>, <Dt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`11`, `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11??????11`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  A   R   1   Rs  0   111 00  Rn  Rt  |
```

### Variant: `Floating-point (LDFMINNML_64)` (Double-precision release)
- **Condition**: `size == 11 && A == 0 && R == 1`
- **Assembly**: `LDFMINNML  <Ds>, <Dt>, [<Xn|SP>]`
- **Fixed bits**: `size`=`11`, `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10??????11`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  A   R   1   Rs  0   111 00  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hs>` | `register (16-bit)` | `Rs` | Is the 16-bit name of the SIMD&FP register holding the data value to be operated on with the contents of the memory location, encoded in the "Rs" fiel |
| `<Ht>` | `register (16-bit)` | `Rt` | Is the 16-bit name of the SIMD&FP register to be loaded, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Ss>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the SIMD&FP register holding the data value to be operated on with the contents of the memory location, encoded in the "Rs" fiel |
| `<St>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the SIMD&FP register to be loaded, encoded in the "Rt" field. |
| `<Ds>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the SIMD&FP register holding the data value to be operated on with the contents of the memory location, encoded in the "Rs" fiel |
| `<Dt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the SIMD&FP register to be loaded, encoded in the "Rt" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ldfminnm.xml`
</details>