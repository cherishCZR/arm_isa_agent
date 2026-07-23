## LUTI4
_ARM A64 Instruction_

**Title**: LUTI4 -- A64 | **Class**: `advsimd` | **XML ID**: `LUTI4_advsimd`

**Architecture**: `FEAT_AdvSIMD && FEAT_LUT` (FEAT_AdvSIMD && FEAT_LUT)

**Summary**: Lookup table read with 4-bit indices

**Description**:
This instruction copies indexed 8-bit or 16-bit elements from the one or two
table vectors to the destination vector using packed 4-bit indices from
a segment of the source vector. A segment corresponds to a portion
of the source vector that is consumed in order to fill the destination
vector. The segment is selected by the vector segment index.

### Variant: `Advanced SIMD (LUTI4_asimdtbl_L5)` (Byte)
- **Condition**: `len == x1 && op == 0`
- **Assembly**: `LUTI4  <Vd>.16B, { <Vn>.16B }, <Vm>[<index>]`
- **Fixed bits**: `len`=`1`, `op`=`0`
- **Bit Pattern**: `????????????01??????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23  21 20  15 14  12 11   9   4  |
|--------------------------------------|
| 0   1   001110 01  0   Rm  0   len op  00  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdtbl.LUTI4_asimdtbl_L5)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_LUT) then
    EndOfDecode(Decode_UNDEF);
if len<0> == '0' && op == '0' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer isize = 4;
constant integer esize = 8 << UInt(op);
constant integer ntblr = 1 << UInt(op);
constant integer part = if op == '0' then UInt(len<1>) else UInt(len);
```

#### Execute (A64.simd_dp.asimdtbl.LUTI4_asimdtbl_L5)

```
CheckFPAdvSIMDEnabled64();
constant integer elements = 128 DIV esize;
constant integer ibase = elements * part;
constant bits(128) indices = V[m, 128];
constant bits(128) table1  = V[n+0, 128];
constant bits(128) table2  = if ntblr == 2 then V[(n+1) MOD 32, 128] else Zeros(128);
bits(128) result;
bits(esize) res;

for e = 0 to elements-1
    constant integer index = UInt(Elem[indices, ibase + e, isize]);
    if index < elements then
        res = Elem[table1, index, esize];
    else
        assert ntblr == 2;
        res = Elem[table2, index - elements, esize];
    Elem[result, e, esize] = res;

V[d, 128] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD) && IsFeatureImplemented(FEAT_LUT)` |
| 🚫 ENCODING_UNDEF | `len<0> != '0' \|\| op != '0'` |

### Variant: `Advanced SIMD (LUTI4_asimdtbl_L7)` (Halfword)
- **Condition**: `op == 1`
- **Assembly**: `LUTI4  <Vd>.8H, { <Vn1>.8H, <Vn2>.8H }, <Vm>[<index>]`
- **Fixed bits**: `op`=`1`
- **Bit Pattern**: `????????????1???????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23  21 20  15 14  12 11   9   4  |
|--------------------------------------|
| 0   1   001110 01  0   Rm  0   len op  00  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP table register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the SIMD&FP source register, encoded in the "Rm" field. |
| `<index>` | `unknown` | `len` | For the "Byte" variant: is the vector segment index, in the range 0 to 1, encoded in the "len<1>" field. |
| `<index>` | `unknown` | `len` | For the "Halfword" variant: is the vector segment index, in the range 0 to 3, encoded in the "len" field. |
| `<Vn1>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP table register, encoded in the "Rn" field. |
| `<Vn2>` | `register (128-bit)` | `Rn` | Is the name of the second SIMD&FP table register, encoded as "Rn" plus 1 modulo 32. |

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
- source: `luti4_advsimd.xml`
</details>