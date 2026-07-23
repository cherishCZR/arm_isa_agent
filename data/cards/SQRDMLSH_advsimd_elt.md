## SQRDMLSH
_ARM A64 Instruction_

**Title**: SQRDMLSH (by element) -- A64 | **Class**: `advsimd` | **XML ID**: `SQRDMLSH_advsimd_elt`

**Architecture**: `FEAT_RDM` (ARMv8.1)

**Summary**: Signed saturating rounding doubling multiply subtract returning high half (by element)

**Description**:
This instruction
multiplies the vector elements of the first source SIMD&FP register
with the value of a vector element of the second source SIMD&FP register
without saturating the multiply results,
doubles the results, and
subtracts the most significant half of the final results
from the vector elements of the destination SIMD&FP register.
The results are rounded.

If any of the results overflow, they are saturated. The cumulative
saturation bit, FPSR.QC, is set if
saturation occurs.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Scalar`
- **Assembly**: `SQRDMLSH  <V><d>, <V><n>, <Vm>.<Ts>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23  21 20 19  15  13 12 11 10  9   4  |
|--------------------------------------------------|
| 01  1   1   111 1   size L   M   Rm  11  1   1   H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdelem.SQRDMLSH_asisdelem_R)

```
if !IsFeatureImplemented(FEAT_RDM) then EndOfDecode(Decode_UNDEF);
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

constant boolean rounding = TRUE;
```

#### Execute (A64.simd_dp.asisdelem.SQRDMLSH_asisdelem_R)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(idxdsize) operand2 = V[m, idxdsize];
constant bits(datasize) operand3 = V[d, datasize];
bits(datasize) result;
integer element1;
integer element2;
integer element3;
integer accum;
boolean sat;

element2 = SInt(Elem[operand2, index, esize]);
for e = 0 to elements-1
    element1 = SInt(Elem[operand1, e, esize]);
    element3 = SInt(Elem[operand3, e, esize]);
    accum = (element3 << esize) - 2 * (element1 * element2);
    accum = RShr(accum, esize, rounding);
    (Elem[result, e, esize], sat) = SignedSatQ(accum, esize);
    if sat then FPSR.QC = '1';

V[d, datasize] = result;
```

### Variant: `Vector`
- **Assembly**: `SQRDMLSH  <Vd>.<T>, <Vn>.<T>, <Vm>.<Ts>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20 19  15  13 12 11 10  9   4  |
|-----------------------------------------------------|
| 0   Q   1   0   111 1   size L   M   Rm  11  1   1   H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdelem.SQRDMLSH_asimdelem_R)

```
if !IsFeatureImplemented(FEAT_RDM) then EndOfDecode(Decode_UNDEF);
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
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;

constant boolean rounding = TRUE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<V>` | `register (128-bit)` | `size` | Is a width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<n>` | `unknown` | `Rn` | Is the number of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `size:M:Rm` | Is the name of the second SIMD&FP source register, |
| `<Ts>` | `unknown` | `size` | Is an element size specifier, |
| `<index>` | `unknown` | `size:H:L:M` | Is the element index, |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `arrangement` | `size:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |

**<V> Value Table**:

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

**<T> Value Table**:

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
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_RDM)` |
| ↩ DECODE_FALLBACK | `matching encodings` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqrdmlsh_advsimd_elt.xml`
</details>