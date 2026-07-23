## SQRSHRUN
_ARM A64 Instruction_

**Title**: SQRSHRUN, SQRSHRUN2 -- A64 | **Class**: `advsimd` | **XML ID**: `SQRSHRUN_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Signed saturating rounded shift right unsigned narrow (immediate)

**Description**:
This instruction reads each signed integer value in
the vector of the source SIMD&FP register,
right shifts each value by an immediate value,
saturates the result to an unsigned integer value that is
half the original width,
places the final result into a vector,
and writes the vector to the
destination SIMD&FP register.
The results are rounded. For truncated results, see
SQSHRUN.

The SQRSHRUN instruction writes the vector
to the lower half of the
destination register and clears the upper half.
The SQRSHRUN2 instruction writes the vector
to the upper half of the
destination register without affecting the other bits of the register.

If saturation occurs, the cumulative saturation bit
FPSR.QC is set.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Scalar`
- **Assembly**: `SQRSHRUN  <Vb><d>, <Va><n>, #<shift>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24  22  18  15  11 10  9   4  |
|--------------------------------------|
| 01  1   1   111 10  ?   immb 1000 1   1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdshf.SQRSHRUN_asisdshf_N)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if immh == '0000' then EndOfDecode(Decode_UNDEF);
if immh<3> == '1' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 8 << HighestSetBitNZ(immh<2:0>);
constant integer datasize = esize;
constant integer elements = 1;
constant integer part = 0;

constant integer shift = (2 * esize) - UInt(immh:immb);
constant boolean round = TRUE;
```

#### Execute (A64.simd_dp.asisdshf.SQRSHRUN_asisdshf_N)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize*2) operand = V[n, datasize*2];
bits(datasize) result;
integer element;
boolean sat;

for e = 0 to elements-1
    element = RShr(SInt(Elem[operand, e, 2*esize]), shift, round);
    (Elem[result, e, esize], sat) = UnsignedSatQ(element, esize);
    if sat then FPSR.QC = '1';

Vpart[d, part, datasize] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `immh != '0000'` |

### Variant: `Vector`
- **Assembly**: `SQRSHRUN{2}  <Vd>.<Tb>, <Vn>.<Ta>, #<shift>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  22  18  15  11 10  9   4  |
|-----------------------------------------|
| 0   Q   1   0   111 10  ?   immb 1000 1   1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdshf.SQRSHRUN_asimdshf_N)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if immh == '0000' then SEE(asimdimm);
if immh<3> == '1' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 8 << HighestSetBitNZ(immh<2:0>);
constant integer datasize = 64;
constant integer part = UInt(Q);
constant integer elements = datasize DIV esize;

constant integer shift = (2 * esize) - UInt(immh:immb);
constant boolean round = TRUE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vb>` | `register (128-bit)` | `immh` | Is the destination width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Va>` | `register (128-bit)` | `immh` | Is the source width specifier, |
| `<n>` | `unknown` | `Rn` | Is the number of the SIMD&FP source register, encoded in the "Rn" field. |
| `<shift>` | `shift` | `immh:immb` | For the "Scalar" variant: is the right shift amount, in the range 1 to the destination operand width in bits, |
| `<shift>` | `shift` | `immh:immb` | For the "Vector" variant: is the right shift amount, in the range 1 to the destination element width in bits, |
| `2` | `unknown` | `Q` | Is the second and upper half specifier. If present it causes the operation to be performed on the upper 64 bits of the registers holding the narrower  |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Tb>` | `unknown` | `immh:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Ta>` | `unknown` | `immh` | Is an arrangement specifier, |

**<Vb> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | B |
| 001x | H |
| 01xx | S |
| 1xxx | RESERVED |

**<Va> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | H |
| 001x | S |
| 01xx | D |
| 1xxx | RESERVED |

**<shift> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | 16 - UInt(immh:immb) |
| 001x | 32 - UInt(immh:immb) |
| 01xx | 64 - UInt(immh:immb) |
| 1xxx | RESERVED |

**<shift> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | 16 - UInt(immh:immb) |
| 001x | 32 - UInt(immh:immb) |
| 01xx | 64 - UInt(immh:immb) |
| 1xxx | RESERVED |

**2 Value Table**:

| bitfield | symbol |
|---|---|
| 0 | [absent] |
| 1 | [present] |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| x | RESERVED |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | 8H |
| 001x | 4S |
| 01xx | 2D |
| 1xxx | RESERVED |

### Encoding Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `immh<3> != '1'` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqrshrun_advsimd.xml`
</details>