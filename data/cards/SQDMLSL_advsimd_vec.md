## SQDMLSL
_ARM A64 Instruction_

**Title**: SQDMLSL, SQDMLSL2 (vector) -- A64 | **Class**: `advsimd` | **XML ID**: `SQDMLSL_advsimd_vec`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Signed saturating doubling multiply-subtract long

**Description**:
This instruction multiplies corresponding signed integer values
in the lower or upper half of the vectors
of the two source SIMD&FP registers, doubles the results,
and subtracts the final results
from the vector elements of the destination SIMD&FP register.
The destination vector elements are twice
as long as the elements that are multiplied.

If overflow occurs with any of the results, those results are saturated.
If saturation occurs,
the cumulative saturation bit
FPSR.QC is set.

The SQDMLSL instruction extracts
each source vector from the lower half
of each source register. The SQDMLSL2 instruction extracts
each source vector from the upper half
of each source register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Scalar`
- **Assembly**: `SQDMLSL  <Va><d>, <Vb><n>, <Vb><m>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23  21 20  15  13 12 11   9   4  |
|--------------------------------------------|
| 01  0   1   111 0   size 1   Rm  10  1   1   00  Rn  Rd  |
```

#### Decode (A64.simd_dp.asisddiff.SQDMLSL_asisddiff_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if size == '00' || size == '11' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 8 << UInt(size);
constant integer datasize = esize;
constant integer elements = 1;
constant integer part = 0;
```

#### Execute (A64.simd_dp.asisddiff.SQDMLSL_asisddiff_only)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = Vpart[n, part, datasize];
constant bits(datasize) operand2 = Vpart[m, part, datasize];
constant bits(2*datasize) operand3 = V[d, 2*datasize];
bits(2*datasize) result;
integer element1;
integer element2;
bits(2*esize) product;
integer accum;
boolean sat1;
boolean sat2;

for e = 0 to elements-1
    element1 = SInt(Elem[operand1, e, esize]);
    element2 = SInt(Elem[operand2, e, esize]);
    (product, sat1) = SignedSatQ(2 * element1 * element2, 2 * esize);
    accum = SInt(Elem[operand3, e, 2*esize]) - SInt(product);
    (Elem[result, e, 2*esize], sat2) = SignedSatQ(accum, 2 * esize);
    if sat1 || sat2 then FPSR.QC = '1';

V[d, 2*datasize] = result;
```

### Variant: `Vector`
- **Assembly**: `SQDMLSL{2}  <Vd>.<Ta>, <Vn>.<Tb>, <Vm>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15  13 12 11   9   4  |
|-----------------------------------------------|
| 0   Q   0   0   111 0   size 1   Rm  10  1   1   00  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimddiff.SQDMLSL_asimddiff_L)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if size == '00' || size == '11' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 8 << UInt(size);
constant integer datasize = 64;
constant integer part = UInt(Q);
constant integer elements = datasize DIV esize;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Va>` | `register (128-bit)` | `size` | Is the destination width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vb>` | `register (128-bit)` | `size` | Is the source width specifier, |
| `<n>` | `unknown` | `Rn` | Is the number of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<m>` | `unknown` | `Rm` | Is the number of the second SIMD&FP source register, encoded in the "Rm" field. |
| `2` | `unknown` | `Q` | Is the second and upper half specifier. If present it causes the operation to be performed on the upper 64 bits of the registers holding the narrower  |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `size` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Tb>` | `unknown` | `size:Q` | Is an arrangement specifier, |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

**<Va> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | S |
| 10 | D |
| 11 | RESERVED |

**<Vb> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | RESERVED |

**2 Value Table**:

| bitfield | symbol |
|---|---|
| 0 | [absent] |
| 1 | [present] |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | 4S |
| 10 | 2D |
| 11 | RESERVED |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| x | RESERVED |
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| x | RESERVED |

### Encoding Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `size != '00' && size != '11'` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqdmlsl_advsimd_vec.xml`
</details>