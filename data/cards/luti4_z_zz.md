## LUTI4
_ARM A64 Instruction_

**Title**: LUTI4 (8-bit and 16-bit) -- A64 | **Class**: `sve2` | **XML ID**: `luti4_z_zz`

**Architecture**: `(FEAT_SVE2 || FEAT_SME2) && FEAT_LUT` ((FEAT_SVE2 || FEAT_SME2) && FEAT_LUT)

**Summary**: Lookup table read with 4-bit indicess (8-bit and 16-bit)

**Description**:
This instruction copies indexed 8-bit or 16-bit elements from the low 128 or 256 bits of the table vector,
      or from the low 128 bits of the two table vectors to
the destination vector using packed 4-bit indices from a
segment of the source vector. A segment corresponds to a portion of the
source vector that is consumed in order to fill the destination vector.
The segment is selected by the vector segment index.
This instruction is unpredicated.

### Variant: `Byte, single register table`
- **Assembly**: `LUTI4  <Zd>.B, { <Zn>.B }, <Zm>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  15  12   9   4  |
|-----------------------------------|
| 010 0010 1   i1  1   1   Zm  101 001 Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_histseg_lut.sve_intx_lut4_8.luti4_z_zz_8)

```
if ((!IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME2)) ||
      !IsFeatureImplemented(FEAT_LUT)) then EndOfDecode(Decode_UNDEF);
constant integer isize = 4;
constant integer esize = 8;
constant integer ntblr = 1;
constant integer m = UInt(Zm);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer part = UInt(i1);
```

#### Execute (A64.sve.sve_intx_histseg_lut.sve_intx_lut4_8.luti4_z_zz_8)

```
if IsFeatureImplemented(FEAT_SME2) then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
if ntblr == 1 && esize == 16 && VL < 256 then EndOfDecode(Decode_UNDEF);
constant integer elements = VL DIV esize;
constant integer tablesize = if ntblr == 1 && esize == 16 then 256 else 128;
constant integer eltspertable = tablesize DIV esize;
constant integer ibase = elements * part;
constant bits(VL) indices = Z[m, VL];
constant bits(VL) table1  = Z[n+0, VL];
constant bits(VL) table2  = if ntblr == 2 then Z[(n+1) MOD 32, VL] else Zeros(VL);
bits(VL) result;
bits(esize) res;

for e = 0 to elements-1
    constant integer index = UInt(Elem[indices, ibase + e, isize]);
    if index < eltspertable then
        res = Elem[table1, index, esize];
    else
        assert ntblr == 2;
        res = Elem[table2, index - eltspertable, esize];
    Elem[result, e, esize] = res;

Z[d, VL] = result;
```

### Variant: `Halfword, two register table`
- **Assembly**: `LUTI4  <Zd>.H, { <Zn1>.H, <Zn2>.H }, <Zm>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12 11 10  9   4  |
|--------------------------------------|
| 010 0010 1   i2  1   Zm  101 1   0   1   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_histseg_lut.sve_intx_lut4_16.luti4_z_zz_2x16)

```
if ((!IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME2)) ||
      !IsFeatureImplemented(FEAT_LUT)) then EndOfDecode(Decode_UNDEF);
constant integer isize = 4;
constant integer esize = 16;
constant integer ntblr = 2;
constant integer m = UInt(Zm);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer part = UInt(i2);
```

### Variant: `Halfword, single register table`
- **Assembly**: `LUTI4  <Zd>.H, { <Zn>.H }, <Zm>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12 11 10  9   4  |
|--------------------------------------|
| 010 0010 1   i2  1   Zm  101 1   1   1   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_histseg_lut.sve_intx_lut4_16.luti4_z_zz_1x16)

```
if ((!IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME2)) ||
      !IsFeatureImplemented(FEAT_LUT)) then EndOfDecode(Decode_UNDEF);
if MaxImplementedAnyVL() < 256 then EndOfDecode(Decode_UNDEF);
constant integer isize = 4;
constant integer esize = 16;
constant integer ntblr = 1;
constant integer m = UInt(Zm);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer part = UInt(i2);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `MaxImplementedAnyVL() < 256` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the table vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the source scalable vector register, encoded in the "Zm" field. |
| `<index>` | `unknown` | `i1` | For the "Byte, single register table" variant: is the vector segment index, in the range 0 to 1, encoded in the "i1" field. |
| `<index>` | `unknown` | `i2` | For the "Halfword, single register table" and "Halfword, two register table" variants: is the vector segment index, in the range 0 to 3, encoded in th |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first table vector register, encoded as "Zn". |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second table vector register, encoded as "Zn" plus 1 modulo 32. |

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
- source: `luti4_z_zz.xml`
</details>