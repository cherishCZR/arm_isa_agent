## LDBFMAX
_ARM A64 Instruction_

**Title**: LDBFMAX, LDBFMAXA, LDBFMAXAL, LDBFMAXL -- A64 | **Class**: `advsimd` | **XML ID**: `LDBFMAX`

**Architecture**: `FEAT_LSFE` (ARMv9.6)

**Summary**: BFloat16 floating-point atomic maximum in memory

**Description**:
This instruction atomically loads a 16-bit value from memory,
computes the BFloat16 maximum with the value held in a register,
and stores the result back to memory.
The value initially loaded from memory is returned in the destination register.

This instruction:

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Floating-point (LDBFMAX_16)` (No memory ordering)
- **Condition**: `A == 0 && R == 0`
- **Assembly**: `LDBFMAX  <Hs>, <Ht>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 1   00  A   R   1   Rs  0   100 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop.LDBFMAX_16)

```
if !IsFeatureImplemented(FEAT_LSFE) then EndOfDecode(Decode_UNDEF);

constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer s = UInt(Rs);

constant integer datasize = 16;
constant boolean acquire = A == '1';
constant boolean release = R == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.memop.LDBFMAX_16)

```
CheckFPEnabled64();
bits(64) address;
bits(datasize) value;
bits(datasize) data;
constant AccessDescriptor accdesc = CreateAccDescFPAtomicOp(MemAtomicOp_BFMAX, acquire,
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

### Variant: `Floating-point (LDBFMAXA_16)` (Acquire)
- **Condition**: `A == 1 && R == 0`
- **Assembly**: `LDBFMAXA  <Hs>, <Ht>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 1   00  A   R   1   Rs  0   100 00  Rn  Rt  |
```

### Variant: `Floating-point (LDBFMAXAL_16)` (Acquire-release)
- **Condition**: `A == 1 && R == 1`
- **Assembly**: `LDBFMAXAL  <Hs>, <Ht>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 1   00  A   R   1   Rs  0   100 00  Rn  Rt  |
```

### Variant: `Floating-point (LDBFMAXL_16)` (Release)
- **Condition**: `A == 0 && R == 1`
- **Assembly**: `LDBFMAXL  <Hs>, <Ht>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 1   00  A   R   1   Rs  0   100 00  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hs>` | `register (16-bit)` | `Rs` | Is the 16-bit name of the SIMD&FP register holding the data value to be operated on with the contents of the memory location, encoded in the "Rs" fiel |
| `<Ht>` | `register (16-bit)` | `Rt` | Is the 16-bit name of the SIMD&FP register to be loaded, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- reg-type: `16-reg`
- source: `ldbfmax.xml`
</details>