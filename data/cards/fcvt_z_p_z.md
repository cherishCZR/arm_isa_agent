## FCVT
_ARM A64 Instruction_

**Title**: FCVT -- A64 | **Class**: `sve` | **XML ID**: `fcvt_z_p_z`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME), `FEAT_SVE2p2 || FEAT_SME2p2` (FEAT_SVE2p2 || FEAT_SME2p2)

**Summary**: Floating-point convert precision (predicated)

**Description**:
Convert the size and precision of each active floating-point element of the source vector,
and place the results in the corresponding elements of the destination vector. 
Inactive elements in the destination vector register remain unmodified or
are set to zero, depending on whether merging or zeroing
predication is selected.

Since the input and result types have a different size
the smaller type is held unpacked in the least
significant bits of elements of the larger size. When the
input is the smaller type the upper bits of each source
element are ignored. When the result is the smaller type
the results are
zero-extended
to fill each destination element.

**Attributes**: Predicated

### Variant: `Half-precision to single-precision, merging`
- **Assembly**: `FCVT  <Zd>.S, <Pg>/M, <Zn>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  17  15  12   9   4  |
|-----------------------------------|
| 011 0010 1   10  0   010 01  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_unary.sve_fp_2op_p_zd_b_0.fcvt_z_p_z_h2s)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 16;
constant integer d_esize = 32;
constant boolean merging = TRUE;
```

#### Execute (A64.sve.sve_fp_unary.sve_fp_2op_p_zd_b_0.fcvt_z_p_z_h2s)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
bits(VL) result = if merging then Z[d, VL] else Zeros(VL);

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        constant bits(esize) element = Elem[operand, e, esize];
        constant bits(d_esize) res = FPConvertSVE(element<s_esize-1:0>, FPCR, d_esize);
        Elem[result, e, esize] = ZeroExtend(res, esize);

Z[d, VL] = result;
```

### Variant: `Half-precision to single-precision, zeroing`
- **Assembly**: `FCVT  <Zd>.S, <Pg>/Z, <Zn>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  15 14  12   9   4  |
|-----------------------------------|
| 011 0010 0   10  011 010 1   01  Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_zeroing_unary.sve_fp_z2op_p_zd_b_0.fcvt_z_p_z_h2sz)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 16;
constant integer d_esize = 32;
constant boolean merging = FALSE;
```

### Variant: `Half-precision to double-precision, merging`
- **Assembly**: `FCVT  <Zd>.D, <Pg>/M, <Zn>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  17  15  12   9   4  |
|-----------------------------------|
| 011 0010 1   11  0   010 01  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_unary.sve_fp_2op_p_zd_b_0.fcvt_z_p_z_h2d)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 16;
constant integer d_esize = 64;
constant boolean merging = TRUE;
```

### Variant: `Half-precision to double-precision, zeroing`
- **Assembly**: `FCVT  <Zd>.D, <Pg>/Z, <Zn>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  15 14  12   9   4  |
|-----------------------------------|
| 011 0010 0   11  011 010 1   01  Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_zeroing_unary.sve_fp_z2op_p_zd_b_0.fcvt_z_p_z_h2dz)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 16;
constant integer d_esize = 64;
constant boolean merging = FALSE;
```

### Variant: `Single-precision to half-precision, merging`
- **Assembly**: `FCVT  <Zd>.H, <Pg>/M, <Zn>.S`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  17  15  12   9   4  |
|-----------------------------------|
| 011 0010 1   10  0   010 00  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_unary.sve_fp_2op_p_zd_b_0.fcvt_z_p_z_s2h)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 32;
constant integer d_esize = 16;
constant boolean merging = TRUE;
```

### Variant: `Single-precision to half-precision, zeroing`
- **Assembly**: `FCVT  <Zd>.H, <Pg>/Z, <Zn>.S`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  15 14  12   9   4  |
|-----------------------------------|
| 011 0010 0   10  011 010 1   00  Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_zeroing_unary.sve_fp_z2op_p_zd_b_0.fcvt_z_p_z_s2hz)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 32;
constant integer d_esize = 16;
constant boolean merging = FALSE;
```

### Variant: `Single-precision to double-precision, merging`
- **Assembly**: `FCVT  <Zd>.D, <Pg>/M, <Zn>.S`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  17  15  12   9   4  |
|-----------------------------------|
| 011 0010 1   11  0   010 11  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_unary.sve_fp_2op_p_zd_b_0.fcvt_z_p_z_s2d)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 32;
constant integer d_esize = 64;
constant boolean merging = TRUE;
```

### Variant: `Single-precision to double-precision, zeroing`
- **Assembly**: `FCVT  <Zd>.D, <Pg>/Z, <Zn>.S`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  15 14  12   9   4  |
|-----------------------------------|
| 011 0010 0   11  011 010 1   11  Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_zeroing_unary.sve_fp_z2op_p_zd_b_0.fcvt_z_p_z_s2dz)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 32;
constant integer d_esize = 64;
constant boolean merging = FALSE;
```

### Variant: `Double-precision to half-precision, merging`
- **Assembly**: `FCVT  <Zd>.H, <Pg>/M, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  17  15  12   9   4  |
|-----------------------------------|
| 011 0010 1   11  0   010 00  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_unary.sve_fp_2op_p_zd_b_0.fcvt_z_p_z_d2h)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 64;
constant integer d_esize = 16;
constant boolean merging = TRUE;
```

### Variant: `Double-precision to half-precision, zeroing`
- **Assembly**: `FCVT  <Zd>.H, <Pg>/Z, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  15 14  12   9   4  |
|-----------------------------------|
| 011 0010 0   11  011 010 1   00  Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_zeroing_unary.sve_fp_z2op_p_zd_b_0.fcvt_z_p_z_d2hz)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 64;
constant integer d_esize = 16;
constant boolean merging = FALSE;
```

### Variant: `Double-precision to single-precision, merging`
- **Assembly**: `FCVT  <Zd>.S, <Pg>/M, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  17  15  12   9   4  |
|-----------------------------------|
| 011 0010 1   11  0   010 10  101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_unary.sve_fp_2op_p_zd_b_0.fcvt_z_p_z_d2s)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 64;
constant integer d_esize = 32;
constant boolean merging = TRUE;
```

### Variant: `Double-precision to single-precision, zeroing`
- **Assembly**: `FCVT  <Zd>.S, <Pg>/Z, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  15 14  12   9   4  |
|-----------------------------------|
| 011 0010 0   11  011 010 1   10  Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_zeroing_unary.sve_fp_z2op_p_zd_b_0.fcvt_z_p_z_d2sz)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer s_esize = 64;
constant integer d_esize = 32;
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
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p2) \|\| IsFeatureImplemented(FEAT_SME2p2)` |

### Operational Notes

The merging variant of this instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and the merging variant of this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX can be predicated or unpredicated.
          
          
            A predicated MOVPRFX must use the same governing predicate register as the merging variant this instruction.
          
          
            A predicated MOVPRFX must use the larger of the destination element size and first source element size in the preferred disassembly of the merging variant of this instruction.
          
          
            The MOVPRFX must specify the same destination register as the merging variant of this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of the merging variant of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvt_z_p_z.xml`
</details>