## UQRSHL
_ARM A64 Instruction_

**Title**: UQRSHL -- A64 | **Class**: `advsimd` | **XML ID**: `UQRSHL_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Unsigned saturating rounding shift left (register)

**Description**:
This instruction takes each vector element of the first
source SIMD&FP register, shifts the vector element by a value from the least
significant byte of the corresponding vector element of the second
source SIMD&FP register, places the results into a vector,
and writes the vector to the destination
SIMD&FP register.

If the shift value is positive, the operation is a left shift. Otherwise, it is a right shift.
The results are
rounded. For truncated results, see UQSHL.

If overflow occurs with any of the results, those results are saturated.
If saturation occurs, the cumulative saturation bit
FPSR.QC is set.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Scalar`
- **Assembly**: `UQRSHL  <V><d>, <V><n>, <V><m>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23  21 20  15  12 11 10  9   4  |
|--------------------------------------------|
| 01  1   1   111 0   size 1   Rm  010 1   1   1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdsame.UQRSHL_asisdsame_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if S == '0' && size != '11' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);

constant boolean unsigned = TRUE;
constant boolean rounding = TRUE;
constant integer esize = 8 << UInt(size);
constant integer datasize = esize;
constant integer elements = 1;
```

#### Execute (A64.simd_dp.asisdsame.UQRSHL_asisdsame_only)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(datasize) operand2 = V[m, datasize];
bits(datasize) result;
boolean sat;

for e = 0 to elements-1
    integer element = UInt(Elem[operand1, e, esize]);
    integer shift = ShiftSat(SInt(Elem[operand2, e, esize]<7:0>), esize);
    if shift >= 0 then // left shift
        element = element << shift;
    else               // right shift
        shift = -shift;
        element = RShr(element, shift, rounding);

    (Elem[result, e, esize], sat) = SatQ(element, esize, unsigned);
    if sat then FPSR.QC = '1';

V[d, datasize] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `S != '0' \|\| size == '11'` |

### Variant: `Vector`
- **Assembly**: `UQRSHL  <Vd>.<T>, <Vn>.<T>, <Vm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15  12 11 10  9   4  |
|-----------------------------------------------|
| 0   Q   1   0   111 0   size 1   Rm  010 1   1   1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame.UQRSHL_asimdsame_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if size:Q == '110' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);

constant boolean unsigned = TRUE;
constant boolean rounding = TRUE;
constant integer esize = 8 << UInt(size);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `size:Q != '110'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<V>` | `register (128-bit)` | `size` | Is a width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<n>` | `unknown` | `Rn` | Is the number of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<m>` | `unknown` | `Rm` | Is the number of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `arrangement` | `size:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

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
- source: `uqrshl_advsimd.xml`
</details>