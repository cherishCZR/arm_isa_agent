## SQDMULLT
_ARM A64 Instruction_

**Title**: SQDMULLT (indexed) -- A64 | **Class**: `sve2` | **XML ID**: `sqdmullt_z_zzi`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Signed saturating doubling multiply long (top, indexed)

**Description**:
Multiply then double the odd-numbered signed elements within each 128-bit segment of
the first source vector and the specified element in the corresponding
second source vector segment, and place the results
in overlapping double-width elements of the destination vector register.
Each result element is saturated to the
double-width N-bit element's
signed integer range -2(N-1)  to (2(N-1))-1.

The elements within the second source vector are specified using
an immediate index which selects the same element position within
each 128-bit vector segment.  The index range is from 0 to
one less than the number of elements per 128-bit segment.

### Variant: `32-bit`
- **Assembly**: `SQDMULLT  <Zd>.S, <Zn>.H, <Zm>.H[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  11 10  9   4  |
|--------------------------------------|
| 010 0010 0   10  1   i3h Zm  1110 i3l 1   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_qdmul_long_by_indexed_elem.sqdmullt_z_zzi_s)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer index = UInt(i3h:i3l);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant integer sel = 1;
```

#### Execute (A64.sve.sve_intx_by_indexed_elem.sve_intx_qdmul_long_by_indexed_elem.sqdmullt_z_zzi_s)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV (2 * esize);
constant integer eltspersegment = 128 DIV (2 * esize);
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer s = e - (e MOD eltspersegment);
    constant integer element1 = SInt(Elem[operand1, 2 * e + sel,   esize]);
    constant integer element2 = SInt(Elem[operand2, 2 * s + index, esize]);
    constant integer res = 2 * element1 * element2;
    Elem[result, e, 2*esize] = SignedSat(res, 2*esize);

Z[d, VL] = result;
```

### Variant: `64-bit`
- **Assembly**: `SQDMULLT  <Zd>.D, <Zn>.S, <Zm>.S[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  11 10  9   4  |
|--------------------------------------|
| 010 0010 0   11  1   i2h Zm  1110 i2l 1   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_qdmul_long_by_indexed_elem.sqdmullt_z_zzi_d)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer index = UInt(i2h:i2l);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant integer sel = 1;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "32-bit" variant: is the name of the second source scalable vector register Z0-Z7, encoded in the "Zm" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "64-bit" variant: is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<imm>` | `immediate` | `i3h:i3l` | For the "32-bit" variant: is the element index, in the range 0 to 7, encoded in the "i3h:i3l" fields. |
| `<imm>` | `immediate` | `i2h:i2l` | For the "64-bit" variant: is the element index, in the range 0 to 3, encoded in the "i2h:i2l" fields. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqdmullt_z_zzi.xml`
</details>