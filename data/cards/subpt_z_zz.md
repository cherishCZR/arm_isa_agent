## SUBPT
_ARM A64 Instruction_

**Title**: SUBPT (unpredicated) -- A64 | **Class**: `sve2` | **XML ID**: `subpt_z_zz`

**Architecture**: `FEAT_SVE && FEAT_CPA` (FEAT_SVE && FEAT_CPA)

**Summary**: Subtract checked pointer vectors (unpredicated)

**Description**:
Subtract with pointer check all elements of the second source vector
from corresponding elements of the first source vector and place the
results in the corresponding elements of the destination vector. This
instruction is unpredicated.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: SM Policy: `SM_0_only`

### Variant: `SVE2`
- **Assembly**: `SUBPT  <Zd>.D, <Zn>.D, <Zm>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12   9   4  |
|--------------------------------|
| 000 0010 0   11  1   Zm  000 011 Zn  Zd  |
```

#### Decode (A64.sve.sve_int_unpred_arit.sve_int_bin_cons_arit_0.subpt_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) || !IsFeatureImplemented(FEAT_CPA) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_int_unpred_arit.sve_int_bin_cons_arit_0.subpt_z_zz_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 64;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(64) element1 = Elem[operand1, e, 64];
    constant bits(64) element2 = Elem[operand2, e, 64];
    constant bits(64) res = element1 - element2;
    Elem[result, e, 64] = PointerAddCheck(res, element1);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) && IsFeatureImplemented(FEAT_CPA)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `subpt_z_zz.xml`
</details>