## LUTI2
_ARM A64 Instruction_

**Title**: LUTI2 (single) -- A64 | **Class**: `mortlach2` | **XML ID**: `luti2_z_ztz`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Lookup table read with 2-bit indexes (single)

**Description**:
This instruction copies 8-bit, 16-bit or 32-bit elements from ZT0 to one destination
vector using packed 2-bit indices from a segment of the source vector register.
A segment corresponds to a portion of the source vector that is consumed in order
to fill the destination vector. The segment is selected by the vector
segment index modulo the total number of segments.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `LUTI2  <Zd>.<T>, ZT0, <Zn>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  18 17  13  11   9   4  |
|--------------------------------------|
| 1   10  0000 01  1   001 1   i4  size 00  Zn  Zd  |
```

#### Decode (A64.sme.mortlach_zt_expand_ctg.mortlach_expand_1dst.luti2_z_ztz_)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if size == '11' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer isize = 2;
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer imm = UInt(i4);
constant integer nreg = 1;
```

#### Execute (A64.sme.mortlach_zt_expand_ctg.mortlach_expand_1dst.luti2_z_ztz_)

```
CheckStreamingSVEEnabled();
CheckSMEZT0Enabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer segments = esize DIV (isize * nreg);
constant integer segment = imm MOD segments;
constant bits(VL) indexes = Z[n, VL];
constant integer dst = d;
constant bits(512) table = ZT0[512];

for r = 0 to nreg-1
    constant integer base = (segment * nreg + r) * elements;
    bits(VL) result;
    for e = 0 to elements-1
        constant integer index = UInt(Elem[indexes, base+e, isize]);
        Elem[result, e, esize] = Elem[table, index, 32]<esize-1:0>;
    Z[dst+r, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |
| 🚫 ENCODING_UNDEF | `size != '11'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<index>` | `unknown` | `i4` | Is the vector segment index, in the range 0 to 15, encoded in the "i4" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | RESERVED |

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
- source: `luti2_z_ztz.xml`
</details>