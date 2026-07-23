## FCMLA
_ARM A64 Instruction_

**Title**: FCMLA (by element) -- A64 | **Class**: `advsimd` | **XML ID**: `FCMLA_advsimd_elt`

**Architecture**: `FEAT_FCMA` (ARMv8.3)

**Summary**: Floating-point complex multiply accumulate (by element)

**Description**:
This instruction operates on complex numbers that are represented in SIMD&FP registers as pairs of elements,
with the more significant element holding the imaginary part of the number and the less significant element
holding the real part of the number. Each element holds a floating-point value. It performs the following computation
on complex numbers from the first source register and the destination register with the specified complex number from the second source register:

The multiplication and addition operations are performed as a fused multiply-add, without any intermediate rounding.

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
- **Assembly**: `FCMLA  <Vd>.<T>, <Vn>.<T>, <Vm>.<Ts>[<index>], #<rotate>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20 19  15 14  12 11 10  9   4  |
|-----------------------------------------------------|
| 0   Q   1   0   111 1   size L   M   Rm  0   rot 1   H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdelem.FCMLA_advsimd_elt)

```
if !IsFeatureImplemented(FEAT_FCMA) then EndOfDecode(Decode_UNDEF);
if size == '00' || size == '11' then EndOfDecode(Decode_UNDEF);
if !IsFeatureImplemented(FEAT_FP16) && size == '10' then EndOfDecode(Decode_UNDEF);
if size == '10' && (L == '1' || Q == '0') then EndOfDecode(Decode_UNDEF);
if size == '01' && H == '1' && Q == '0' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(M:Rm);
integer index;
if size == '01' then index = UInt(H:L);
if size == '10' then index = UInt(H);
constant integer esize = 8 << UInt(size);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
```

#### Execute (A64.simd_dp.asimdelem.FCMLA_advsimd_elt)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(datasize) operand2 = V[m, datasize];
constant bits(datasize) operand3 = V[d, datasize];
bits(datasize) result;

for e = 0 to (elements DIV 2)-1
    bits(esize) element1;
    bits(esize) element2;
    bits(esize) element3;
    bits(esize) element4;
    case rot of
        when '00'
            element1 = Elem[operand2, index*2, esize];
            element2 = Elem[operand1, e*2, esize];
            element3 = Elem[operand2, index*2+1, esize];
            element4 = Elem[operand1, e*2, esize];
        when '01'
            element1 = FPNeg(Elem[operand2, index*2+1, esize], FPCR);
            element2 = Elem[operand1, e*2+1, esize];
            element3 = Elem[operand2, index*2, esize];
            element4 = Elem[operand1, e*2+1, esize];
        when '10'
            element1 = FPNeg(Elem[operand2, index*2, esize], FPCR);
            element2 = Elem[operand1, e*2, esize];
            element3 = FPNeg(Elem[operand2, index*2+1, esize], FPCR);
            element4 = Elem[operand1, e*2, esize];
        when '11'
            element1 = Elem[operand2, index*2+1, esize];
            element2 = Elem[operand1, e*2+1, esize];
            element3 = FPNeg(Elem[operand2, index*2, esize], FPCR);
            element4 = Elem[operand1, e*2+1, esize];

    Elem[result, e*2,   esize] = FPMulAdd(Elem[operand3, e*2, esize], element2, element1, FPCR);
    Elem[result, e*2+1, esize] = FPMulAdd(Elem[operand3, e*2+1, esize], element4, element3, FPCR);

V[d, datasize] = result;
```

#### Constraints
_3× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FCMA)` |
| 🚫 ENCODING_UNDEF | `size != '00' && size != '11'` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP16) \|\| size != '10'` |
| 🚫 ENCODING_UNDEF | `size != '10' \|\| (L != '1' && Q != '0')` |
| 🚫 ENCODING_UNDEF | `size != '01' \|\| H != '1' \|\| Q != '0'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `arrangement` | `size:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `M:Rm` | Is the name of the second SIMD&FP source register, encoded in the "M:Rm" fields. |
| `<Ts>` | `unknown` | `size` | Is an element size specifier, |
| `<index>` | `unknown` | `size:H:L` | Is the element index, |
| `<rotate>` | `unknown` | `rot` | Is the rotation, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| x | RESERVED |
| 0 | 4H |
| 1 | 8H |
| 0 | RESERVED |
| 1 | 4S |
| x | RESERVED |

**<Ts> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | RESERVED |

**<index> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | UInt(H:L) |
| 10 | UInt(H) |
| 11 | RESERVED |

**<rotate> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | 0 |
| 01 | 90 |
| 10 | 180 |
| 11 | 270 |

---
<details><summary>Metadata</summary>

- advsimd-reguse: `2reg-element`
- isa: `A64`
- source: `fcmla_advsimd_elt.xml`
</details>