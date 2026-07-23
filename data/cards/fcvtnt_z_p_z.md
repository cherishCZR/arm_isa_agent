## FCVTNT
_ARM A64 Instruction_

**Title**: FCVTNT (predicated) -- A64 | **Class**: `sve2` | **XML ID**: `fcvtnt_z_p_z`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME), `FEAT_SVE2p2 || FEAT_SME2p2` (FEAT_SVE2p2 || FEAT_SME2p2)

**Summary**: Floating-point down convert and narrow (top, predicated)

**Description**:
Convert active floating-point elements from the source vector to the
next lower precision, and place the results in the
odd-numbered half-width elements of the destination vector,
leaving the even-numbered elements unchanged. 
Inactive elements in the destination vector register remain unmodified or
are set to zero, depending on whether merging or zeroing
predication is selected.

**Attributes**: Predicated

### Variant: `Single-precision to half-precision, merging`
- **Assembly**: `FCVTNT  <Zd>.H, <Pg>/M, <Zn>.S`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  17  15  12   9   4  |
|--------------------------------|
| 011 0010 0   10  0010 00  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fcvt2.sve_fp_fcvt2.fcvtnt_z_p_z_s2h)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean merging = TRUE;
```

#### Execute (A64.sve.sve_fp_fcvt2.sve_fp_fcvt2.fcvtnt_z_p_z_s2h)

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
        Elem[result, 2*e + 1, halfesize] = FPConvertSVE(element, FPCR, halfesize);

    elsif !merging then
        Elem[result, 2*e + 1, halfesize] = Zeros(halfesize);

Z[d, VL] = result;
```

### Variant: `Single-precision to half-precision, zeroing`
- **Assembly**: `FCVTNT  <Zd>.H, <Pg>/Z, <Zn>.S`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  17  15  12   9   4  |
|--------------------------------|
| 011 0010 0   10  0000 00  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fcvt2z.sve_fp_fcvt2z.fcvtnt_z_p_z_s2hz)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean merging = FALSE;
```

### Variant: `Double-precision to single-precision, merging`
- **Assembly**: `FCVTNT  <Zd>.S, <Pg>/M, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  17  15  12   9   4  |
|--------------------------------|
| 011 0010 0   11  0010 10  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fcvt2.sve_fp_fcvt2.fcvtnt_z_p_z_d2s)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean merging = TRUE;
```

### Variant: `Double-precision to single-precision, zeroing`
- **Assembly**: `FCVTNT  <Zd>.S, <Pg>/Z, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  17  15  12   9   4  |
|--------------------------------|
| 011 0010 0   11  0000 10  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fcvt2z.sve_fp_fcvt2z.fcvtnt_z_p_z_d2sz)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean merging = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

### Encoding Constraints
_2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p2) \|\| IsFeatureImplemented(FEAT_SME2p2)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvtnt_z_p_z.xml`
</details>