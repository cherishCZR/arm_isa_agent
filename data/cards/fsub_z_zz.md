## FSUB
_ARM A64 Instruction_

**Title**: FSUB (vectors, unpredicated) -- A64 | **Class**: `sve` | **XML ID**: `fsub_z_zz`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Floating-point subtract vectors (unpredicated)

**Description**:
Subtract all floating-point elements of the second source vector from
corresponding elements of the first source vector
and place the results in the corresponding elements of the destination vector. This instruction is unpredicated.

### Variant: `SVE`
- **Assembly**: `FSUB  <Zd>.<T>, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12   9   4  |
|--------------------------------|
| 011 0010 1   ?   0   Zm  000 001 Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_unpred.sve_fp_3op_u_zd.fsub_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_fp_unpred.sve_fp_3op_u_zd.fsub_z_zz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(esize) element1 = Elem[operand1, e, esize];
    constant bits(esize) element2 = Elem[operand2, e, esize];
    Elem[result, e, esize] = FPSub(element1, element2, FPCR);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

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
| 01 | H |
| 10 | S |
| 11 | D |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fsub_z_zz.xml`
</details>