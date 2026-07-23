## UMULLB
_ARM A64 Instruction_

**Title**: UMULLB (indexed) -- A64 | **Class**: `sve2` | **XML ID**: `umullb_z_zzi`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Unsigned multiply long (bottom, indexed)

**Description**:
Multiply the even-numbered unsigned elements within each 128-bit segment
of the first source vector by the specified unsigned element in the corresponding
second source vector segment, and place the results in the overlapping
double-width elements of the destination vector register.

The elements within the second source vector are specified using
an immediate index which selects the same element position within
each 128-bit vector segment.  The index range is from 0 to
one less than the number of elements per 128-bit segment.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `32-bit`
- **Assembly**: `UMULLB  <Zd>.S, <Zn>.H, <Zm>.H[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  12 11 10  9   4  |
|-----------------------------------------|
| 010 0010 0   10  1   i3h Zm  110 1   i3l 0   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_mul_long_by_indexed_elem.umullb_z_zzi_s)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer index = UInt(i3h:i3l);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant integer sel = 0;
```

#### Execute (A64.sve.sve_intx_by_indexed_elem.sve_intx_mul_long_by_indexed_elem.umullb_z_zzi_s)

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
    constant integer element1 = UInt(Elem[operand1, 2 * e + sel,   esize]);
    constant integer element2 = UInt(Elem[operand2, 2 * s + index, esize]);
    constant integer res = element1 * element2;
    Elem[result, e, 2*esize] = res<2*esize-1:0>;

Z[d, VL] = result;
```

### Variant: `64-bit`
- **Assembly**: `UMULLB  <Zd>.D, <Zn>.S, <Zm>.S[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  12 11 10  9   4  |
|-----------------------------------------|
| 010 0010 0   11  1   i2h Zm  110 1   i2l 0   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_mul_long_by_indexed_elem.umullb_z_zzi_d)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer index = UInt(i2h:i2l);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant integer sel = 0;
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
- source: `umullb_z_zzi.xml`
</details>