## FMUL
_ARM A64 Instruction_

**Title**: FMUL (indexed) -- A64 | **Class**: `sve` | **XML ID**: `fmul_z_zzi`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Floating-point multiply by indexed elements

**Description**:
Multiply all floating-point elements within each 128-bit
segment of the first source vector by the specified element in
the corresponding second source vector segment.  The results
are placed in the corresponding elements of the destination
vector.

The elements within the second source vector are specified using
an immediate index which selects the same element position within
each 128-bit vector segment.  The index range is from 0 to
one less than the number of elements per 128-bit segment.
This instruction is unpredicated.

### Variant: `Half-precision`
- **Assembly**: `FMUL  <Zd>.H, <Zn>.H, <Zm>.H[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  15  11 10  9   4  |
|-----------------------------------------|
| 011 0010 0   0   i3h 1   i3l Zm  0010 0   0   Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fmul_by_indexed_elem.sve_fp_fmul_by_indexed_elem.fmul_z_zzi_h)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer index = UInt(i3h:i3l);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_fp_fmul_by_indexed_elem.sve_fp_fmul_by_indexed_elem.fmul_z_zzi_h)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer eltspersegment = 128 DIV esize;
constant bits(VL) op1 = Z[n, VL];
constant bits(VL) op2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer segmentbase = e - (e MOD eltspersegment);
    constant integer s = segmentbase + index;
    constant bits(esize) elem2 = Elem[op2, s, esize];
    constant bits(esize) elem1 = Elem[op1, e, esize];
    Elem[result, e, esize] = FPMul(elem1, elem2, FPCR);

Z[d, VL] = result;
```

### Variant: `Single-precision`
- **Assembly**: `FMUL  <Zd>.S, <Zn>.S, <Zm>.S[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  11 10  9   4  |
|--------------------------------------|
| 011 0010 0   10  1   i2  Zm  0010 0   0   Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fmul_by_indexed_elem.sve_fp_fmul_by_indexed_elem.fmul_z_zzi_s)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer index = UInt(i2);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

### Variant: `Double-precision`
- **Assembly**: `FMUL  <Zd>.D, <Zn>.D, <Zm>.D[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  11 10  9   4  |
|--------------------------------------|
| 011 0010 0   11  1   i1  Zm  0010 0   0   Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fmul_by_indexed_elem.sve_fp_fmul_by_indexed_elem.fmul_z_zzi_d)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer index = UInt(i1);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "Half-precision" and "Single-precision" variants: is the name of the second source scalable vector register Z0-Z7, encoded in the "Zm" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "Double-precision" variant: is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<imm>` | `immediate` | `i3h:i3l` | For the "Half-precision" variant: is the immediate index, in the range 0 to 7, encoded in the "i3h:i3l" fields. |
| `<imm>` | `immediate` | `i2` | For the "Single-precision" variant: is the immediate index, in the range 0 to 3, encoded in the "i2" field. |
| `<imm>` | `immediate` | `i1` | For the "Double-precision" variant: is the immediate index, in the range 0 to 1, encoded in the "i1" field. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmul_z_zzi.xml`
</details>