## FTSMUL
_ARM A64 Instruction_

**Title**: FTSMUL -- A64 | **Class**: `sve` | **XML ID**: `ftsmul_z_zz`

**Architecture**: `FEAT_SVE` (PROFILE_A)

**Summary**: Floating-point trigonometric starting value

**Description**:
The FTSMUL instruction multiplies each element of the first
source vector by itself, replaces the sign-bit of each product
with the least-significant bit of the corresponding element of
the second source vector, and places the results in the
destination vector. This instruction is unpredicated.

FTSMUL can be combined with FTMAD and FTSSEL to
compute values for sin(x) and cos(x). The use of
the second operand is consistent with it holding an integer
corresponding to the desired sine-wave quadrant when used in
conjunction with FTMAD.

Note: FTSMUL, FTMAD, and FTSSEL can be used to
compute values for sin(k) and correspondingly
cos(k-π/2) via an intermediate value x, in the
range -π/4 < x ≤ π/4, and a quadrant q
where k = qπ/2 + x, using a Taylor Series
approximation. FTSMUL can be used to compute x2,
and to insert q<0> into the most-significant bit,
indicating the desired odd versus even Taylor Series to be used
in FTMAD. Repeated uses of FTMAD can be performed on
this value with decreasing immediate index operands, to produce a
single accumulated value approximating the Taylor Series result
with a single outstanding factor. FTSSEL can be used to
apply the final factor of x, 1.0, -x, or -1.0,
dependent on the corresponding sine-wave quadrant q<1:0>,
to produce a final sin() or cos() value.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: SM Policy: `SM_0_only`

### Variant: `SVE`
- **Assembly**: `FTSMUL  <Zd>.<T>, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12   9   4  |
|--------------------------------|
| 011 0010 1   size 0   Zm  000 011 Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_unpred.sve_fp_3op_u_zd.ftsmul_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) then EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_fp_unpred.sve_fp_3op_u_zd.ftsmul_z_zz_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(esize) element1 = Elem[operand1, e, esize];
    constant bits(esize) element2 = Elem[operand2, e, esize];
    Elem[result, e, esize] = FPTrigSMul(element1, element2, FPCR);

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ftsmul_z_zz.xml`
</details>