## BFCVTNT
_ARM A64 Instruction_

**Title**: BFCVTNT -- A64 | **Class**: `sve` | **XML ID**: `bfcvtnt_z_p_z`

**Architecture**: `(FEAT_SVE || FEAT_SME) && FEAT_BF16` ((FEAT_SVE || FEAT_SME) && FEAT_BF16), `FEAT_SVE2p2 || FEAT_SME2p2` (FEAT_SVE2p2 || FEAT_SME2p2)

**Summary**: Single-precision down convert and narrow to BFloat16 (top, predicated)

**Description**:
Convert to BFloat16 from single-precision in each active floating-point
element of the source vector, and place the results in the
odd-numbered 16-bit elements of the destination vector,
leaving the even-numbered elements unchanged. 
Inactive elements in the destination vector register remain unmodified or
are set to zero, depending on whether merging or zeroing
predication is selected.

ID_AA64ZFR0_EL1.BF16 indicates whether this instruction is implemented.

**Attributes**: Predicated

### Variant: `Merging`
- **Assembly**: `BFCVTNT  <Zd>.H, <Pg>/M, <Zn>.S`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  17  15  12   9   4  |
|--------------------------------|
| 011 0010 0   10  0010 10  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fcvt2.sve_fp_fcvt2.bfcvtnt_z_p_z_s2bf)

```
if ((!IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME)) ||
    !IsFeatureImplemented(FEAT_BF16)) then EndOfDecode(Decode_UNDEF);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean merging = TRUE;
```

#### Execute (A64.sve.sve_fp_fcvt2.sve_fp_fcvt2.bfcvtnt_z_p_z_s2bf)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV 32;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = if AnyActiveElement(mask, 32) then Z[n, VL] else Zeros(VL);
bits(VL) result = Z[d, VL];

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, 32) then
        constant bits(32) element = Elem[operand, e, 32];
        Elem[result, 2*e+1, 16] = FPConvertBF(element, FPCR);
    elsif !merging then
        Elem[result, 2*e+1, 16] = Zeros(16);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `((IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)) && IsFeatureImplemented(FEAT_BF16))` |

### Variant: `Zeroing`
- **Assembly**: `BFCVTNT  <Zd>.H, <Pg>/Z, <Zn>.S`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  17  15  12   9   4  |
|--------------------------------|
| 011 0010 0   10  0000 10  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fcvt2z.sve_fp_fcvt2z.bfcvtnt_z_p_z_s2bfz)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
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
- source: `bfcvtnt_z_p_z.xml`
</details>