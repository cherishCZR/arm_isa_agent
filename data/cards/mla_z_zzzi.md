## MLA
_ARM A64 Instruction_

**Title**: MLA (indexed) -- A64 | **Class**: `sve2` | **XML ID**: `mla_z_zzzi`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Multiply-add to accumulator (indexed)

**Description**:
Multiply all integer elements within each 128-bit
segment of the first source vector by the specified element in
the corresponding second source vector segment.  The products are then destructively added to the corresponding
elements of the addend and destination vector.

The elements within the second source vector are specified using
an immediate index which selects the same element position within
each 128-bit vector segment.  The index range is from 0 to
one less than the number of elements per 128-bit segment.
This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `16-bit`
- **Assembly**: `MLA  <Zda>.H, <Zn>.H, <Zm>.H[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  15  10  9   4  |
|--------------------------------------|
| 010 0010 0   0   i3h 1   i3l Zm  00001 0   Zn  Zda |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_mla_by_indexed_elem.mla_z_zzzi_h)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer index = UInt(i3h:i3l);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

#### Execute (A64.sve.sve_intx_by_indexed_elem.sve_intx_mla_by_indexed_elem.mla_z_zzzi_h)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer eltspersegment = 128 DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result = Z[da, VL];

for e = 0 to elements-1
    constant integer segmentbase = e - (e MOD eltspersegment);
    constant integer s = segmentbase + index;
    constant integer element1 = UInt(Elem[operand1, e, esize]);
    constant integer element2 = UInt(Elem[operand2, s, esize]);
    constant bits(esize) product = (element1 * element2)<esize-1:0>;
    Elem[result, e, esize] = Elem[result, e, esize] + product;

Z[da, VL] = result;
```

### Variant: `32-bit`
- **Assembly**: `MLA  <Zda>.S, <Zn>.S, <Zm>.S[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  10  9   4  |
|-----------------------------------|
| 010 0010 0   10  1   i2  Zm  00001 0   Zn  Zda |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_mla_by_indexed_elem.mla_z_zzzi_s)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer index = UInt(i2);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

### Variant: `64-bit`
- **Assembly**: `MLA  <Zda>.D, <Zn>.D, <Zm>.D[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  10  9   4  |
|-----------------------------------|
| 010 0010 0   11  1   i1  Zm  00001 0   Zn  Zda |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_mla_by_indexed_elem.mla_z_zzzi_d)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer index = UInt(i1);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
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
                
              
            
          
        
        This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `mla_z_zzzi.xml`
</details>