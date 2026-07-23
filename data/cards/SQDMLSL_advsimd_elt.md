## SQDMLSL
_ARM A64 Instruction_

**Title**: SQDMLSL, SQDMLSL2 (by element) -- A64 | **Class**: `advsimd` | **XML ID**: `SQDMLSL_advsimd_elt`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Signed saturating doubling multiply-subtract long (by element)

**Description**:
This instruction
multiplies each vector element in the
lower or upper half of the
first source SIMD&FP register
by the specified vector element of the
second source SIMD&FP register, doubles the results,
and subtracts the final results
from the vector elements of the destination SIMD&FP register.
The destination vector elements are twice
as long as the elements that are multiplied.
All the values in this instruction are signed integer values.

If overflow occurs with any of the results, those results are saturated.
If saturation occurs, the cumulative saturation bit
FPSR.QC is set.

The SQDMLSL instruction extracts
vector elements from the lower half
of the first source register. The SQDMLSL2 instruction extracts
vector elements from the upper half
of the first source register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Scalar`
- **Assembly**: `SQDMLSL  <Va><d>, <Vb><n>, <Vm>.<Ts>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23  21 20 19  15 14 13  11 10  9   4  |
|--------------------------------------------------|
| 01  0   1   111 1   size L   M   Rm  0   1   11  H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdelem.SQDMLSL_asisdelem_L)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer idxdsize = 64 << UInt(H);
integer index;
bit Rmhi;
case size of
    when '01' index = UInt(H:L:M); Rmhi = '0';
    when '10' index = UInt(H:L); Rmhi = M;
    otherwise EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rmhi:Rm);

constant integer esize = 8 << UInt(size);
constant integer datasize = esize;
constant integer elements = 1;
constant integer part = 0;
```

#### Execute (A64.simd_dp.asisdelem.SQDMLSL_asisdelem_L)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize)   operand1 = Vpart[n, part, datasize];
constant bits(idxdsize)   operand2 = V[m, idxdsize];
constant bits(2*datasize) operand3 = V[d, 2*datasize];
bits(2*datasize) result;
integer element1;
integer element2;
bits(2*esize) product;
integer accum;
boolean sat1;
boolean sat2;

element2 = SInt(Elem[operand2, index, esize]);
for e = 0 to elements-1
    element1 = SInt(Elem[operand1, e, esize]);
    (product, sat1) = SignedSatQ(2 * element1 * element2, 2 * esize);
    accum = SInt(Elem[operand3, e, 2*esize]) - SInt(product);
    (Elem[result, e, 2*esize], sat2) = SignedSatQ(accum, 2 * esize);
    if sat1 || sat2 then FPSR.QC = '1';

V[d, 2*datasize] = result;
```

### Variant: `Vector`
- **Assembly**: `SQDMLSL{2}  <Vd>.<Ta>, <Vn>.<Tb>, <Vm>.<Ts>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20 19  15 14 13  11 10  9   4  |
|-----------------------------------------------------|
| 0   Q   0   0   111 1   size L   M   Rm  0   1   11  H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdelem.SQDMLSL_asimdelem_L)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer idxdsize = 64 << UInt(H);
integer index;
bit Rmhi;
case size of
    when '01' index = UInt(H:L:M); Rmhi = '0';
    when '10' index = UInt(H:L); Rmhi = M;
    otherwise EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rmhi:Rm);

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
| `<Vm>` | `register (128-bit)` | `size:M:Rm` | Is the name of the second SIMD&FP source register, |
| `<Ts>` | `unknown` | `size` | Is an element size specifier, |
| `<index>` | `unknown` | `size:H:L:M` | Is the element index, |
| `2` | `unknown` | `Q` | Is the second and upper half specifier. If present it causes the operation to be performed on the upper 64 bits of the registers holding the narrower  |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `size` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Tb>` | `unknown` | `size:Q` | Is an arrangement specifier, |

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

**<Vm> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | UInt('0':Rm) |
| 10 | UInt(M:Rm) |
| 11 | RESERVED |

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
| 01 | UInt(H:L:M) |
| 10 | UInt(H:L) |
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
_1× ↩ DECODE_FALLBACK / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| ↩ DECODE_FALLBACK | `matching encodings` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqdmlsl_advsimd_elt.xml`
</details>