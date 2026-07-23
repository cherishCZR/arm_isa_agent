## LUTI2
_ARM A64 Instruction_

**Title**: LUTI2 -- A64 | **Class**: `advsimd` | **XML ID**: `LUTI2_advsimd`

**Architecture**: `FEAT_AdvSIMD && FEAT_LUT` (FEAT_AdvSIMD && FEAT_LUT)

**Summary**: Lookup table read with 2-bit indices

**Description**:
This instruction copies indexed 8-bit or 16-bit elements from the table vector
to the destination vector using packed 2-bit indices from a segment of the
source vector. A segment corresponds to a portion of the source vector
that is consumed in order to fill the destination vector. The segment is selected
by the vector segment index.

### Variant: `Advanced SIMD (LUTI2_asimdtbl_L5)` (Byte)
- **Condition**: `op2 == 10 && op == 1`
- **Assembly**: `LUTI2  <Vd>.16B, { <Vn>.16B }, <Vm>[<index>]`
- **Fixed bits**: `op2`=`0`, `op`=`1`
- **Bit Pattern**: `????????????1?????????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23  21 20  15 14  12 11   9   4  |
|--------------------------------------|
| 0   1   001110 1x  0   Rm  0   len op  00  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdtbl.LUTI2_asimdtbl_L5)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) || !IsFeatureImplemented(FEAT_LUT) then
    EndOfDecode(Decode_UNDEF);
if op2 == '10' && op == '0' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer isize = 2;
constant integer esize = if op2 == '10' then 8 else 16;
constant integer part = if op2 == '10' then UInt(len) else UInt(len:op);
```

#### Execute (A64.simd_dp.asimdtbl.LUTI2_asimdtbl_L5)

```
CheckFPAdvSIMDEnabled64();
constant integer elements = 128 DIV esize;
constant integer ibase = elements * part;
constant bits(128) indices = V[m, 128];
constant bits(128) table   = V[n, 128];
bits(128) result;

for e = 0 to elements-1
    constant integer index = UInt(Elem[indices, ibase + e, isize]);
    Elem[result, e, esize] = Elem[table, index, esize];

V[d, 128] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD) && IsFeatureImplemented(FEAT_LUT)` |
| 🚫 ENCODING_UNDEF | `op2 != '10' \|\| op != '0'` |

### Variant: `Advanced SIMD (LUTI2_asimdtbl_L6)` (Halfword)
- **Condition**: `op2 == 11`
- **Assembly**: `LUTI2  <Vd>.8H, { <Vn>.8H }, <Vm>[<index>]`
- **Fixed bits**: `op2`=`1`
- **Bit Pattern**: `??????????????????????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23  21 20  15 14  12 11   9   4  |
|--------------------------------------|
| 0   1   001110 1x  0   Rm  0   len op  00  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP table register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the SIMD&FP source register, encoded in the "Rm" field. |
| `<index>` | `unknown` | `len` | For the "Byte" variant: is the vector segment index, in the range 0 to 3, encoded in the "len" field. |
| `<index>` | `unknown` | `len:op` | For the "Halfword" variant: is the vector segment index, in the range 0 to 7, encoded in the "len:op" fields. |

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
- source: `luti2_advsimd.xml`
</details>