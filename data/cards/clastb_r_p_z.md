## CLASTB
_ARM A64 Instruction_

**Title**: CLASTB (scalar) -- A64 | **Class**: `sve` | **XML ID**: `clastb_r_p_z`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Conditionally extract last element to general-purpose register

**Description**:
From the source vector register extract the
   last active element,
   and then zero-extend that element to destructively
   place in the destination and first source general-purpose
   register.
   If there are no active elements then destructively
   zero-extend the least significant element-size bits
   of the destination and first source general-purpose register.

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `CLASTB  <R><dn>, <Pg>, <R><dn>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  16 15  13 12   9   4  |
|-----------------------------------------|
| 000 0010 1   size 1   1   000 1   10  1   Pg  Zm  Rdn |
```

#### Decode (A64.sve.sve_perm_pred.sve_int_perm_clast_rz.clastb_r_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer dn = UInt(Rdn);
constant integer m = UInt(Zm);
constant integer csize = if esize < 64 then 32 else 64;
constant boolean isBefore = TRUE;
```

#### Execute (A64.sve.sve_perm_pred.sve_int_perm_clast_rz.clastb_r_p_z_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(esize) operand1 = X[dn, esize];
constant bits(VL) operand2 = Z[m, VL];
bits(csize) result;
integer last = LastActiveElement(mask, esize);

if last < 0 then
    result = ZeroExtend(operand1, csize);
else
    if !isBefore then
        last = last + 1;
        if last >= elements then last = 0;
    result = ZeroExtend(Elem[operand2, last, esize], csize);

X[dn, csize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<R>` | `unknown` | `size` | Is a width specifier, |
| `<dn>` | `unknown` | `Rdn` | Is the number [0-30] of the source and destination general-purpose register or the name ZR (31), encoded in the "Rdn" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the source scalable vector register, encoded in the "Zm" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |

**<R> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | W |
| 01 | W |
| 10 | W |
| 11 | X |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

### Operational Notes

If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the general-purpose register written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `clastb_r_p_z.xml`
</details>