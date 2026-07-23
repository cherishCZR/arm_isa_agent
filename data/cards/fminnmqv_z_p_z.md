## FMINNMQV
_ARM A64 Instruction_

**Title**: FMINNMQV -- A64 | **Class**: `sve2` | **XML ID**: `fminnmqv_z_p_z`

**Architecture**: `FEAT_SVE2p1 || FEAT_SME2p1` (FEAT_SVE2p1 || FEAT_SME2p1)

**Summary**: Floating-point minimum number recursive reduction of quadword vector segments

**Description**:
Floating-point minimum number of the same element numbers from each 128-bit source vector segment
using a recursive pairwise reduction,
placing each result into the corresponding element number of the
128-bit SIMD&FP destination register.
Inactive elements in the source vector are treated as the default NaN.

Regardless of the value of FPCR.AH, the behavior is as follows:

**Attributes**: Predicated

### Variant: `SVE2`
- **Assembly**: `FMINNMQV  <Vd>.<T>, <Pg>, <Zn>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  15  12   9   4  |
|--------------------------------|
| 011 0010 0   size 010 101 101 Pg  Zn  Vd  |
```

#### Decode (A64.sve.sve_fp_fastreduceq.sve_fp_fast_redq.fminnmqv_z_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Vd);
```

#### Execute (A64.sve.sve_fp_fastreduceq.sve_fp_fast_redq.fminnmqv_z_p_z_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer segments = VL DIV 128;
constant integer elempersegment = 128 DIV esize;
constant integer segbits = segments*esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
constant bits(esize) identity = FPDefaultNaN(FPCR, esize);
bits(128) result = Zeros(128);

for e = 0 to elempersegment-1
    bits(segbits) stmp;
    for s = 0 to segments-1
        if ActivePredicateElement(mask, s * elempersegment + e, esize) then
            Elem[stmp, s, esize] = Elem[operand, s * elempersegment + e, esize];
        else
            Elem[stmp, s, esize] = identity;
    Elem[result, e, esize] = FPReduce(ReduceOp_FMINNUM, stmp, esize, FPCR);
V[d, 128] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p1) \|\| IsFeatureImplemented(FEAT_SME2p1)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Vd` | Is the name of the destination SIMD&FP register, encoded in the "Vd" field. |
| `<T>` | `unknown` | `size` | Is an arrangement specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<Tb>` | `unknown` | `size` | Is the size specifier, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | 8H |
| 10 | 4S |
| 11 | 2D |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fminnmqv_z_p_z.xml`
</details>