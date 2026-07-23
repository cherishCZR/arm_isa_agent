## STFMAXNM
_ARM A64 Instruction_

**Title**: STFMAXNM, STFMAXNML -- A64 | **Class**: `advsimd` | **XML ID**: `STFMAXNM`

**Architecture**: `FEAT_LSFE` (ARMv9.6)

**Summary**: Floating-point atomic maximum number in memory, without return

**Description**:
This instruction atomically loads a 16-bit, 32-bit, or 64-bit value from memory,
computes the floating-point maximum number with the value held in a register,
and stores the result back to memory.

This instruction:

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Floating-point (STFMAXNM_16)` (Half-precision no memory ordering)
- **Condition**: `size == 01 && R == 0`
- **Assembly**: `STFMAXNM  <Hs>, [<Xn|SP>]`
- **Fixed bits**: `size`=`01`, `R`=`0`
- **Bit Pattern**: `??????????????????????0???????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  0   R   1   Rs  1   110 00  Rn  11111 |
```

#### Decode (A64.ldst.memop.STFMAXNM_16)

```
if !IsFeatureImplemented(FEAT_LSFE) then EndOfDecode(Decode_UNDEF);

constant integer s = UInt(Rs);
constant integer n = UInt(Rn);

constant integer datasize = 8 << UInt(size);
constant boolean acquire = FALSE;
constant boolean release = R == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.memop.STFMAXNM_16)

```
CheckFPEnabled64();
bits(64) address;
bits(datasize) value;
bits(datasize) data;
constant AccessDescriptor accdesc = CreateAccDescFPAtomicOp(MemAtomicOp_FPMAXNM, acquire,
                                                            release, tagchecked);

value = V[s, datasize];
if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant bits(datasize) comparevalue = bits(datasize) UNKNOWN; // Irrelevant when not executing CAS
data = MemAtomic(address, comparevalue, value, accdesc);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSFE)` |

### Variant: `Floating-point (STFMAXNML_16)` (Half-precision release)
- **Condition**: `size == 01 && R == 1`
- **Assembly**: `STFMAXNML  <Hs>, [<Xn|SP>]`
- **Fixed bits**: `size`=`01`, `R`=`1`
- **Bit Pattern**: `??????????????????????1???????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  0   R   1   Rs  1   110 00  Rn  11111 |
```

### Variant: `Floating-point (STFMAXNM_32)` (Single-precision no memory ordering)
- **Condition**: `size == 10 && R == 0`
- **Assembly**: `STFMAXNM  <Ss>, [<Xn|SP>]`
- **Fixed bits**: `size`=`10`, `R`=`0`
- **Bit Pattern**: `??????????????????????0???????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  0   R   1   Rs  1   110 00  Rn  11111 |
```

### Variant: `Floating-point (STFMAXNML_32)` (Single-precision release)
- **Condition**: `size == 10 && R == 1`
- **Assembly**: `STFMAXNML  <Ss>, [<Xn|SP>]`
- **Fixed bits**: `size`=`10`, `R`=`1`
- **Bit Pattern**: `??????????????????????1???????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  0   R   1   Rs  1   110 00  Rn  11111 |
```

### Variant: `Floating-point (STFMAXNM_64)` (Double-precision no memory ordering)
- **Condition**: `size == 11 && R == 0`
- **Assembly**: `STFMAXNM  <Ds>, [<Xn|SP>]`
- **Fixed bits**: `size`=`11`, `R`=`0`
- **Bit Pattern**: `??????????????????????0???????11`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  0   R   1   Rs  1   110 00  Rn  11111 |
```

### Variant: `Floating-point (STFMAXNML_64)` (Double-precision release)
- **Condition**: `size == 11 && R == 1`
- **Assembly**: `STFMAXNML  <Ds>, [<Xn|SP>]`
- **Fixed bits**: `size`=`11`, `R`=`1`
- **Bit Pattern**: `??????????????????????1???????11`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| size 111 1   00  0   R   1   Rs  1   110 00  Rn  11111 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hs>` | `register (16-bit)` | `Rs` | Is the 16-bit name of the SIMD&FP register holding the data value to be operated on with the contents of the memory location, encoded in the "Rs" fiel |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Ss>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the SIMD&FP register holding the data value to be operated on with the contents of the memory location, encoded in the "Rs" fiel |
| `<Ds>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the SIMD&FP register holding the data value to be operated on with the contents of the memory location, encoded in the "Rs" fiel |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `stfmaxnm.xml`
</details>