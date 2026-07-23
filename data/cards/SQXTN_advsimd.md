## SQXTN
_ARM A64 Instruction_

**Title**: SQXTN, SQXTN2 -- A64 | **Class**: `advsimd` | **XML ID**: `SQXTN_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Signed saturating extract narrow

**Description**:
This instruction reads each vector element
from the source SIMD&FP register,
saturates the value to half the original width,
places the result into a vector,
and writes
the vector to the
lower or upper half of the destination SIMD&FP
register.
The destination vector elements are half as long as the source vector elements.
All the values in this instruction are signed integer values.

If overflow occurs with any of the results, those results are saturated.
If saturation occurs, the cumulative saturation bit
FPSR.QC is set.

The SQXTN instruction writes the vector
to the lower half of the
destination register and clears the upper half.
The SQXTN2 instruction writes the vector
to the upper half of the
destination register without affecting the other bits of the register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Scalar`
- **Assembly**: `SQXTN  <Vb><d>, <Va><n>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23  21  16  11   9   4  |
|-----------------------------------|
| 01  0   1   111 0   size 10000 10100 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdmisc.SQXTN_asisdmisc_N)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if size == '11' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer esize = 8 << UInt(size);
constant integer datasize = esize;
constant integer part = 0;
constant integer elements = 1;
constant boolean unsigned = FALSE;
```

#### Execute (A64.simd_dp.asisdmisc.SQXTN_asisdmisc_N)

```
CheckFPAdvSIMDEnabled64();
constant bits(2*datasize) operand = V[n, 2*datasize];
bits(datasize) result;
bits(2*esize) element;
boolean sat;

for e = 0 to elements-1
    element = Elem[operand, e, 2*esize];
    (Elem[result, e, esize], sat) = SatQ(SInt(element), esize, unsigned);
    if sat then FPSR.QC = '1';

Vpart[d, part, datasize] = result;
```

### Variant: `Vector`
- **Assembly**: `SQXTN{2}  <Vd>.<Tb>, <Vn>.<Ta>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21  16  11   9   4  |
|--------------------------------------|
| 0   Q   0   0   111 0   size 10000 10100 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.SQXTN_asimdmisc_N)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if size == '11' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer esize = 8 << UInt(size);
constant integer datasize = 64;
constant integer part = UInt(Q);
constant integer elements = datasize DIV esize;
constant boolean unsigned = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vb>` | `register (128-bit)` | `size` | Is the destination width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Va>` | `register (128-bit)` | `size` | Is the source width specifier, |
| `<n>` | `unknown` | `Rn` | Is the number of the SIMD&FP source register, encoded in the "Rn" field. |
| `2` | `unknown` | `Q` | Is the second and upper half specifier. If present it causes the operation to be performed on the upper 64 bits of the registers holding the narrower  |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Tb>` | `unknown` | `size:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Ta>` | `unknown` | `size` | Is an arrangement specifier, |

**<Vb> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | RESERVED |

**<Va> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | H |
| 01 | S |
| 10 | D |
| 11 | RESERVED |

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
| 00 | 8H |
| 01 | 4S |
| 10 | 2D |
| 11 | RESERVED |

### Encoding Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `size != '11'` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqxtn_advsimd.xml`
</details>