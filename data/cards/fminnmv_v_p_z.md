## FMINNMV
_ARM A64 Instruction_

**Title**: FMINNMV -- A64 | **Class**: `sve` | **XML ID**: `fminnmv_v_p_z`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Floating-point minimum number recursive reduction to scalar

**Description**:
Floating-point minimum number horizontally over all lanes of a vector using a recursive pairwise reduction,
and place the result in the SIMD&FP scalar destination register.
Inactive elements in the source vector are treated as the default NaN.

Regardless of the value of FPCR.AH, the behavior is as follows:

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `FMINNMV  <V><d>, <Pg>, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  15  12   9   4  |
|--------------------------------|
| 011 0010 1   size 000 101 001 Pg  Zn  Vd  |
```

#### Decode (A64.sve.sve_fp_fastreduce.sve_fp_fast_red.fminnmv_v_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Vd);
```

#### Execute (A64.sve.sve_fp_fastreduce.sve_fp_fast_red.fminnmv_v_p_z_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
constant bits(esize) identity = FPDefaultNaN(FPCR, esize);

V[d, esize] = FPReducePredicated(ReduceOp_FMINNUM, operand, mask, identity, FPCR);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<V>` | `register (128-bit)` | `size` | Is a width specifier, |
| `<d>` | `unknown` | `Vd` | Is the number [0-31] of the destination SIMD&FP register, encoded in the "Vd" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

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
- source: `fminnmv_v_p_z.xml`
</details>