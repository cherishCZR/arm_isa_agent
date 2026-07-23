## CLASTB
_ARM A64 Instruction_

**Title**: CLASTB (SIMD&FP scalar) -- A64 | **Class**: `sve` | **XML ID**: `clastb_v_p_z`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Conditionally extract last element to SIMD&FP scalar register

**Description**:
From the source vector register extract the
   last active element,
   and then zero-extend that element to destructively
   place in the destination and first source SIMD & floating-point scalar
   register.
   If there are no active elements then destructively
   zero-extend the least significant element-size bits
   of the destination and first source SIMD & floating-point scalar register.

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `CLASTB  <V><dn>, <Pg>, <V><dn>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  16 15  13 12   9   4  |
|-----------------------------------------|
| 000 0010 1   size 1   0   101 1   10  0   Pg  Zm  Vdn |
```

#### Decode (A64.sve.sve_perm_pred.sve_int_perm_clast_vz.clastb_v_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer dn = UInt(Vdn);
constant integer m = UInt(Zm);
constant boolean isBefore = TRUE;
```

#### Execute (A64.sve.sve_perm_pred.sve_int_perm_clast_vz.clastb_v_p_z_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(esize) operand1 = V[dn, esize];
constant bits(VL) operand2 = Z[m, VL];
bits(esize) result;
integer last = LastActiveElement(mask, esize);

if last < 0 then
    result = ZeroExtend(operand1, esize);
else
    if !isBefore then
        last = last + 1;
        if last >= elements then last = 0;
    result = Elem[operand2, last, esize];

V[dn, esize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

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
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `clastb_v_p_z.xml`
</details>