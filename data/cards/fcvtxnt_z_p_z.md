## FCVTXNT
_ARM A64 Instruction_

**Title**: FCVTXNT -- A64 | **Class**: `sve2` | **XML ID**: `fcvtxnt_z_p_z`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME), `FEAT_SVE2p2 || FEAT_SME2p2` (FEAT_SVE2p2 || FEAT_SME2p2)

**Summary**: Double-precision down convert to single-precision, rounding to odd (top, predicated)

**Description**:
Convert active double-precision elements from the
source vector to single-precision, rounding to Odd, and
place the results in the odd-numbered 32-bit elements of the
destination vector, leaving the even-numbered elements
unchanged. 
Inactive elements in the destination vector register remain unmodified or
are set to zero, depending on whether merging or zeroing
predication is selected.

Rounding to Odd (aka Von Neumann rounding) permits a two-step
conversion from double-precision to half-precision without
incurring intermediate rounding errors.

**Attributes**: Predicated

### Variant: `Double-precision to single-precision, merging`
- **Assembly**: `FCVTXNT  <Zd>.S, <Pg>/M, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  17  15  12   9   4  |
|--------------------------------|
| 011 0010 0   00  0010 10  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fcvt2.sve_fp_fcvt2.fcvtxnt_z_p_z_d2s)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean merging = TRUE;
```

#### Execute (A64.sve.sve_fp_fcvt2.sve_fp_fcvt2.fcvtxnt_z_p_z_d2s)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant integer halfesize = esize DIV 2;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
bits(VL) result = Z[d, VL];

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        constant bits(esize) element = Elem[operand, e, esize];
        Elem[result, 2*e + 1, halfesize] = FPConvertSVE(element, FPCR, FPRounding_ODD, halfesize);

    elsif !merging then
        Elem[result, 2*e + 1, halfesize] = Zeros(halfesize);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Variant: `Double-precision to single-precision, zeroing`
- **Assembly**: `FCVTXNT  <Zd>.S, <Pg>/Z, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  17  15  12   9   4  |
|--------------------------------|
| 011 0010 0   00  0000 10  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fcvt2z.sve_fp_fcvt2z.fcvtxnt_z_p_z_d2sz)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean merging = FALSE;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p2) \|\| IsFeatureImplemented(FEAT_SME2p2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvtxnt_z_p_z.xml`
</details>