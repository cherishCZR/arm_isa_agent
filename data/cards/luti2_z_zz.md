## LUTI2
_ARM A64 Instruction_

**Title**: LUTI2 (8-bit and 16-bit) -- A64 | **Class**: `sve2` | **XML ID**: `luti2_z_zz`

**Architecture**: `(FEAT_SVE2 || FEAT_SME2) && FEAT_LUT` ((FEAT_SVE2 || FEAT_SME2) && FEAT_LUT)

**Summary**: Lookup table read with 2-bit indices (8-bit and 16-bit)

**Description**:
This instruction copies indexed 8-bit or 16-bit elements from the low 128 bits of the table vector to
the destination vector using packed 2-bit indices from a
segment of the source vector. A segment corresponds to a portion of the
source vector that is consumed in order to fill the destination vector.
The segment is selected by the vector segment index.
This instruction is unpredicated.

### Variant: `Byte`
- **Assembly**: `LUTI2  <Zd>.B, { <Zn>.B }, <Zm>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12   9   4  |
|--------------------------------|
| 010 0010 1   i2  1   Zm  101 100 Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_histseg_lut.sve_intx_lut2_8.luti2_z_zz_8)

```
if ((!IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME2)) ||
      !IsFeatureImplemented(FEAT_LUT)) then EndOfDecode(Decode_UNDEF);
constant integer isize = 2;
constant integer esize = 8;
constant integer m = UInt(Zm);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer part = UInt(i2);
```

#### Execute (A64.sve.sve_intx_histseg_lut.sve_intx_lut2_8.luti2_z_zz_8)

```
if IsFeatureImplemented(FEAT_SME2) then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer ibase = elements * part;
constant bits(VL) indices = Z[m, VL];
constant bits(VL) table   = Z[n, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer index = UInt(Elem[indices, ibase + e, isize]);
    Elem[result, e, esize] = Elem[table, index, esize];

Z[d, VL] = result;
```

### Variant: `Halfword`
- **Assembly**: `LUTI2  <Zd>.H, { <Zn>.H }, <Zm>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12 11   9   4  |
|-----------------------------------|
| 010 0010 1   i3h 1   Zm  101 i3l 10  Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_histseg_lut.sve_intx_lut2_16.luti2_z_zz_16)

```
if ((!IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME2)) ||
      !IsFeatureImplemented(FEAT_LUT)) then EndOfDecode(Decode_UNDEF);
constant integer isize = 2;
constant integer esize = 16;
constant integer m = UInt(Zm);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer part = UInt(i3h:i3l);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the table vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the source scalable vector register, encoded in the "Zm" field. |
| `<index>` | `unknown` | `i2` | For the "Byte" variant: is the vector segment index, in the range 0 to 3, encoded in the "i2" field. |
| `<index>` | `unknown` | `i3h:i3l` | For the "Halfword" variant: is the vector segment index, in the range 0 to 7, encoded in the "i3h:i3l" fields. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `((IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME2)) && IsFeatureImplemented(FEAT_LUT))` |

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
- source: `luti2_z_zz.xml`
</details>