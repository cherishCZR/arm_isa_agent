## STBFMAX
_ARM A64 Instruction_

**Title**: STBFMAX, STBFMAXL -- A64 | **Class**: `advsimd` | **XML ID**: `STBFMAX`

**Architecture**: `FEAT_LSFE` (ARMv9.6)

**Summary**: BFloat16 floating-point atomic maximum in memory, without return

**Description**:
This instruction atomically loads a 16-bit value from memory,
computes the BFloat16 maximum with the value held in a register,
and stores the result back to memory.

This instruction:

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Floating-point (STBFMAX_16)` (No memory ordering)
- **Condition**: `R == 0`
- **Assembly**: `STBFMAX  <Hs>, [<Xn|SP>]`
- **Fixed bits**: `R`=`0`
- **Bit Pattern**: `??????????????????????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 1   00  0   R   1   Rs  1   100 00  Rn  11111 |
```

#### Decode (A64.ldst.memop.STBFMAX_16)

```
if !IsFeatureImplemented(FEAT_LSFE) then EndOfDecode(Decode_UNDEF);

constant integer s = UInt(Rs);
constant integer n = UInt(Rn);

constant integer datasize = 16;
constant boolean acquire = FALSE;
constant boolean release = R == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.memop.STBFMAX_16)

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
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSFE)` |

### Variant: `Floating-point (STBFMAXL_16)` (Release)
- **Condition**: `R == 1`
- **Assembly**: `STBFMAXL  <Hs>, [<Xn|SP>]`
- **Fixed bits**: `R`=`1`
- **Bit Pattern**: `??????????????????????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 1   00  0   R   1   Rs  1   100 00  Rn  11111 |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hs>` | `register (16-bit)` | `Rs` | Is the 16-bit name of the SIMD&FP register holding the data value to be operated on with the contents of the memory location, encoded in the "Rs" fiel |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- reg-type: `16-reg`
- source: `stbfmax.xml`
</details>