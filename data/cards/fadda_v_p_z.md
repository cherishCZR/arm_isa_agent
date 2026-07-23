## FADDA
_ARM A64 Instruction_

**Title**: FADDA -- A64 | **Class**: `sve` | **XML ID**: `fadda_v_p_z`

**Architecture**: `FEAT_SVE` (PROFILE_A)

**Summary**: Floating-point add strictly-ordered reduction, accumulating in scalar

**Description**:
Floating-point add a SIMD&FP scalar source and all active lanes of the vector source
and place the result destructively in the SIMD&FP scalar source register.
Vector elements are processed strictly in order from low to high,
with the scalar source providing the initial value.
Inactive elements in the source vector are ignored.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: Predicated; SM Policy: `SM_0_only`

### Variant: `SVE`
- **Assembly**: `FADDA  <V><dn>, <Pg>, <V><dn>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18 17  15  12   9   4  |
|-----------------------------------|
| 011 0010 1   size 011 0   00  001 Pg  Zm  Vdn |
```

#### Decode (A64.sve.sve_fp_slowreduce.sve_fp_2op_p_vd.fadda_v_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE) then EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer dn = UInt(Vdn);
constant integer m = UInt(Zm);
```

#### Execute (A64.sve.sve_fp_slowreduce.sve_fp_2op_p_vd.fadda_v_p_z_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(esize) operand1 = V[dn, esize];
constant bits(VL) operand2 = if AnyActiveElement(mask, esize) then Z[m, VL] else Zeros(VL);
bits(esize) result = operand1;

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        constant bits(esize) element = Elem[operand2, e, esize];
        result = FPAdd(result, element, FPCR);

V[dn, esize] = result;
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
| `<V>` | `register (128-bit)` | `size` | Is a width specifier, |
| `<dn>` | `unknown` | `Vdn` | Is the number [0-31] of the source and destination SIMD&FP register, encoded in the "Vdn" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the source scalable vector register, encoded in the "Zm" field. |
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
- source: `fadda_v_p_z.xml`
</details>