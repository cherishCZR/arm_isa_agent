## FCVTLT
_ARM A64 Instruction_

**Title**: FCVTLT -- A64 | **Class**: `sve2` | **XML ID**: `fcvtlt_z_p_z`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME), `FEAT_SVE2p2 || FEAT_SME2p2` (FEAT_SVE2p2 || FEAT_SME2p2)

**Summary**: Floating-point up convert long (top, predicated)

**Description**:
Convert odd-numbered floating-point elements from the source
vector to the next higher precision, and place the results
in the active overlapping double-width elements of the destination
vector. 
Inactive elements in the destination vector register remain unmodified or
are set to zero, depending on whether merging or zeroing
predication is selected.

**Attributes**: Predicated

### Variant: `Half-precision to single-precision, merging`
- **Assembly**: `FCVTLT  <Zd>.S, <Pg>/M, <Zn>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  17  15  12   9   4  |
|--------------------------------|
| 011 0010 0   10  0010 01  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fcvt2.sve_fp_fcvt2.fcvtlt_z_p_z_h2s)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean merging = TRUE;
```

#### Execute (A64.sve.sve_fp_fcvt2.sve_fp_fcvt2.fcvtlt_z_p_z_h2s)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant integer halfesize = esize DIV 2;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
bits(VL) result = if merging then Z[d, VL] else Zeros(VL);

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        constant bits(halfesize) element = Elem[operand, 2*e + 1, halfesize];
        Elem[result, e, esize] = FPConvertSVE(element, FPCR, esize);
Z[d, VL] = result;
```

### Variant: `Half-precision to single-precision, zeroing`
- **Assembly**: `FCVTLT  <Zd>.S, <Pg>/Z, <Zn>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  17  15  12   9   4  |
|--------------------------------|
| 011 0010 0   10  0000 01  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fcvt2z.sve_fp_fcvt2z.fcvtlt_z_p_z_h2sz)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean merging = FALSE;
```

### Variant: `Single-precision to double-precision, merging`
- **Assembly**: `FCVTLT  <Zd>.D, <Pg>/M, <Zn>.S`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  17  15  12   9   4  |
|--------------------------------|
| 011 0010 0   11  0010 11  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fcvt2.sve_fp_fcvt2.fcvtlt_z_p_z_s2d)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean merging = TRUE;
```

### Variant: `Single-precision to double-precision, zeroing`
- **Assembly**: `FCVTLT  <Zd>.D, <Pg>/Z, <Zn>.S`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  17  15  12   9   4  |
|--------------------------------|
| 011 0010 0   11  0000 11  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fcvt2z.sve_fp_fcvt2z.fcvtlt_z_p_z_s2dz)

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
- source: `fcvtlt_z_p_z.xml`
</details>