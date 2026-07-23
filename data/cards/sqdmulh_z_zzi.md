## SQDMULH
_ARM A64 Instruction_

**Title**: SQDMULH (indexed) -- A64 | **Class**: `sve2` | **XML ID**: `sqdmulh_z_zzi`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Signed saturating doubling multiply high (indexed)

**Description**:
Multiply all signed elements within each 128-bit segment of the first
source vector by the specified signed element in the corresponding
second source vector segment, double and place the most
significant half of the result in the corresponding elements of the
destination vector register.
Each result element is saturated to the
 N-bit element's
signed integer range -2(N-1)  to (2(N-1))-1.

The elements within the second source vector are specified using
an immediate index which selects the same element position within
each 128-bit vector segment.  The index range is from 0 to
one less than the number of elements per 128-bit segment.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `16-bit`
- **Assembly**: `SQDMULH  <Zd>.H, <Zn>.H, <Zm>.H[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  15  10  9   4  |
|--------------------------------------|
| 010 0010 0   0   i3h 1   i3l Zm  11110 0   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_qdmulh_by_indexed_elem.sqdmulh_z_zzi_h)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer index = UInt(i3h:i3l);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_intx_by_indexed_elem.sve_intx_qdmulh_by_indexed_elem.sqdmulh_z_zzi_h)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer eltspersegment = 128 DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer segmentbase = e - (e MOD eltspersegment);
    constant integer s = segmentbase + index;
    constant integer element1 = SInt(Elem[operand1, e, esize]);
    constant integer element2 = SInt(Elem[operand2, s, esize]);
    constant integer res = 2 * element1 * element2;
    Elem[result, e, esize] = SignedSat(res >> esize, esize);

Z[d, VL] = result;
```

### Variant: `32-bit`
- **Assembly**: `SQDMULH  <Zd>.S, <Zn>.S, <Zm>.S[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  10  9   4  |
|-----------------------------------|
| 010 0010 0   10  1   i2  Zm  11110 0   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_qdmulh_by_indexed_elem.sqdmulh_z_zzi_s)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer index = UInt(i2);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

### Variant: `64-bit`
- **Assembly**: `SQDMULH  <Zd>.D, <Zn>.D, <Zm>.D[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  10  9   4  |
|-----------------------------------|
| 010 0010 0   11  1   i1  Zm  11110 0   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_qdmulh_by_indexed_elem.sqdmulh_z_zzi_d)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
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
| `<Zm>` | `register (128-bit)` | `Zm` | For the "16-bit" and "32-bit" variants: is the name of the second source scalable vector register Z0-Z7, encoded in the "Zm" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "64-bit" variant: is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<imm>` | `immediate` | `i3h:i3l` | For the "16-bit" variant: is the element index, in the range 0 to 7, encoded in the "i3h:i3l" fields. |
| `<imm>` | `immediate` | `i2` | For the "32-bit" variant: is the element index, in the range 0 to 3, encoded in the "i2" field. |
| `<imm>` | `immediate` | `i1` | For the "64-bit" variant: is the element index, in the range 0 to 1, encoded in the "i1" field. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqdmulh_z_zzi.xml`
</details>