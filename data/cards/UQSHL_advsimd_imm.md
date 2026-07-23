## UQSHL
_ARM A64 Instruction_

**Title**: UQSHL (immediate) -- A64 | **Class**: `advsimd` | **XML ID**: `UQSHL_advsimd_imm`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Unsigned saturating shift left (immediate)

**Description**:
This instruction takes each vector element in the
source SIMD&FP register, shifts it by an immediate value,
places the results in a vector,
and writes the vector to the destination
SIMD&FP register.
The results are
truncated. For rounded results, see UQRSHL.

If overflow occurs with any of the results, those results are saturated.
If saturation occurs, the cumulative saturation bit
FPSR.QC is set.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Scalar`
- **Assembly**: `UQSHL  <V><d>, <V><n>, #<shift>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24  22  18  15  12 11 10  9   4  |
|-----------------------------------------|
| 01  1   1   111 10  ?   immb 011 1   0   1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdshf.UQSHL_asisdshf_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if immh == '0000' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 8 << HighestSetBitNZ(immh);
constant integer datasize = esize;
constant integer elements = 1;
constant integer shift = UInt(immh:immb) - esize;

constant boolean src_unsigned = TRUE;
constant boolean dst_unsigned = TRUE;
```

#### Execute (A64.simd_dp.asisdshf.UQSHL_asisdshf_R)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand  = V[n, datasize];
bits(datasize) result;
integer element;
boolean sat;

for e = 0 to elements-1
    element = Int(Elem[operand, e, esize], src_unsigned) << shift;
    (Elem[result, e, esize], sat) = SatQ(element, esize, dst_unsigned);
    if sat then FPSR.QC = '1';

V[d, datasize] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `immh != '0000'` |

### Variant: `Vector`
- **Assembly**: `UQSHL  <Vd>.<T>, <Vn>.<T>, #<shift>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  22  18  15  12 11 10  9   4  |
|--------------------------------------------|
| 0   Q   1   0   111 10  ?   immb 011 1   0   1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdshf.UQSHL_asimdshf_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if immh == '0000' then SEE(asimdimm);
if immh<3>:Q == '10' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 8 << HighestSetBitNZ(immh);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
constant integer shift = UInt(immh:immb) - esize;

constant boolean src_unsigned = TRUE;
constant boolean dst_unsigned = TRUE;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `immh<3>:Q != '10'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<V>` | `register (128-bit)` | `immh` | Is a width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<n>` | `unknown` | `Rn` | Is the number of the SIMD&FP source register, encoded in the "Rn" field. |
| `<shift>` | `shift` | `immh:immb` | For the "Scalar" variant: is the left shift amount, in the range 0 to the operand width in bits minus 1, |
| `<shift>` | `shift` | `immh:immb` | For the "Vector" variant: is the left shift amount, in the range 0 to the element width in bits minus 1, |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `arrangement` | `immh:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | B |
| 001x | H |
| 01xx | S |
| 1xxx | D |

**<shift> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | UInt(immh:immb) - 8 |
| 001x | UInt(immh:immb) - 16 |
| 01xx | UInt(immh:immb) - 32 |
| 1xxx | UInt(immh:immb) - 64 |

**<shift> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | UInt(immh:immb) - 8 |
| 001x | UInt(immh:immb) - 16 |
| 01xx | UInt(immh:immb) - 32 |
| 1xxx | UInt(immh:immb) - 64 |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| 0 | RESERVED |
| 1 | 2D |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `uqshl_advsimd_imm.xml`
</details>