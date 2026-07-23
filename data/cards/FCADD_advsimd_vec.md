## FCADD
_ARM A64 Instruction_

**Title**: FCADD -- A64 | **Class**: `advsimd` | **XML ID**: `FCADD_advsimd_vec`

**Architecture**: `FEAT_FCMA` (ARMv8.3)

**Summary**: Floating-point complex add

**Description**:
This instruction operates on complex numbers that are represented in SIMD&FP registers as pairs of
elements, with the more significant element holding the imaginary part of the number and the less
significant element holding the real part of the number. Each element holds a floating-point
value. It performs the following computation on the corresponding complex number element pairs
from the two source registers:

This instruction can generate a floating-point exception.
  Depending on the settings in FPCR,
  the exception results in either a flag being set in FPSR
  or a synchronous exception being generated.
  For more information, see
  Floating-point exceptions and exception traps.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Vector`
- **Assembly**: `FCADD  <Vd>.<T>, <Vn>.<T>, <Vm>.<T>, #<rotate>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15 14  12 11 10  9   4  |
|--------------------------------------------------|
| 0   Q   1   0   111 0   size 0   Rm  1   11  rot 0   1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame2.FCADD_asimdsame2_C)

```
if !IsFeatureImplemented(FEAT_FCMA) then EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
if size == '01' && !IsFeatureImplemented(FEAT_FP16) then EndOfDecode(Decode_UNDEF);
if Q == '0' && size == '11' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 8 << UInt(size);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
```

#### Execute (A64.simd_dp.asimdsame2.FCADD_asimdsame2_C)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(datasize) operand2 = V[m, datasize];
bits(datasize) result;
bits(esize) element1;
bits(esize) element3;

for e = 0 to (elements DIV 2)-1
    case rot of
        when '0'
            element1 = FPNeg(Elem[operand2, e*2+1, esize], FPCR);
            element3 = Elem[operand2, e*2, esize];
        when '1'
            element1 = Elem[operand2, e*2+1, esize];
            element3 = FPNeg(Elem[operand2, e*2, esize], FPCR);
    Elem[result, e*2,   esize] = FPAdd(Elem[operand1, e*2, esize], element1, FPCR);
    Elem[result, e*2+1, esize] = FPAdd(Elem[operand1, e*2+1, esize], element3, FPCR);

V[d, datasize] = result;
```

#### Constraints
_2× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FCMA)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |
| 🔒 FEATURE_GATE | `size != '01' \|\| IsFeatureImplemented(FEAT_FP16)` |
| 🚫 ENCODING_UNDEF | `Q != '0' \|\| size != '11'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `arrangement` | `size:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<rotate>` | `unknown` | `rot` | Is the rotation, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| x | RESERVED |
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| 0 | RESERVED |
| 1 | 2D |

**<rotate> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 90 |
| 1 | 270 |

---
<details><summary>Metadata</summary>

- advsimd-type: `simd`
- isa: `A64`
- source: `fcadd_advsimd_vec.xml`
</details>