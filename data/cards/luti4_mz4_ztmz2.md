## LUTI4
_ARM A64 Instruction_

**Title**: LUTI4 (four registers, 8-bit) -- A64 | **Class**: `mortlach2` | **XML ID**: `luti4_mz4_ztmz2`

**Architecture**: `FEAT_SME_LUTv2` (ARMv9.5), `FEAT_SME2p1 && FEAT_SME_LUTv2` (FEAT_SME2p1 && FEAT_SME_LUTv2)

**Summary**: Lookup table read with 4-bit indexes and 8-bit elements (four registers)

**Description**:
This instruction copies 8-bit elements from ZT0 to four destination
vectors using packed 4-bit indices in the two source vectors.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `Consecutive`
- **Assembly**: `LUTI4  { <Zd1>.B-<Zd4>.B }, ZT0, { <Zn1>-<Zn2> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  18  13  11   9   5  4   1  |
|-----------------------------------------|
| 1   10  0000 01  0   001 01100 size 00  Zn  0   Zd  00  |
```

#### Decode (A64.sme.mortlach_zt_expand_ctg.mortlach_expand_4dst2src_ctg.luti4_mz4_ztmz2_1)

```
if !IsFeatureImplemented(FEAT_SME_LUTv2) then EndOfDecode(Decode_UNDEF);
if size != '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer isize = 4;
constant integer n = UInt(Zn:'0');
constant integer dstride = 1;
constant integer d = UInt(Zd:'00');
constant integer nreg = 4;
```

#### Execute (A64.sme.mortlach_zt_expand_ctg.mortlach_expand_4dst2src_ctg.luti4_mz4_ztmz2_1)

```
CheckStreamingSVEEnabled();
CheckSMEZT0Enabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(2*VL) indexes = Z[n+1, VL] : Z[n+0, VL];
integer dst = d;
constant bits(512) table = ZT0[512];

for r = 0 to nreg-1
    constant integer base = r * elements;
    bits(VL) result;
    for e = 0 to elements-1
        constant integer index = UInt(Elem[indexes, base+e, isize]);
        Elem[result, e, esize] = Elem[table, index, 32]<esize-1:0>;
    Z[dst, VL] = result;
    dst = dst + dstride;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_LUTv2)` |

### Variant: `Strided`
- **Assembly**: `LUTI4  { <Zd1>.B, <Zd2>.B, <Zd3>.B, <Zd4>.B }, ZT0, { <Zn1>-<Zn2> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  18  15  13  11   9   5  4  3   1  |
|-----------------------------------------|
| 1   10  0000 010011 011 00  size 00  Zn  0   D   00  Zd  |
```

#### Decode (A64.sme.mortlach_zt_expand_nctg.mortlach_expand_4dst2src_nctg.luti4_mz4_ztmz2_4)

```
if !IsFeatureImplemented(FEAT_SME2p1) || !IsFeatureImplemented(FEAT_SME_LUTv2) then
    EndOfDecode(Decode_UNDEF);
if size != '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer isize = 4;
constant integer n = UInt(Zn:'0');
constant integer dstride = 4;
constant integer d = UInt(D:'00':Zd);
constant integer nreg = 4;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2p1) && IsFeatureImplemented(FEAT_SME_LUTv2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Consecutive" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 4. |
| `<Zd1>` | `register (128-bit)` | `D:Zd` | For the "Strided" variant: is the name of the first scalable vector register Z0-Z3 or Z16-Z19 of the destination multi-vector group, encoded as "D:'00 |
| `<Zd4>` | `register (128-bit)` | `Zd` | For the "Consecutive" variant: is the name of the fourth scalable vector register of the destination multi-vector group, encoded as "Zd" times 4 plus  |
| `<Zd4>` | `register (128-bit)` | `D:Zd` | For the "Strided" variant: is the name of the fourth scalable vector register Z12-Z15 or Z28-Z31 of the destination multi-vector group, encoded as "D: |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 2. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the source multi-vector group, encoded as "Zn" times 2 plus 1. |
| `<Zd2>` | `register (128-bit)` | `D:Zd` | Is the name of the second scalable vector register Z4-Z7 or Z20-Z23 of the destination multi-vector group, encoded as "D:'01':Zd". |
| `<Zd3>` | `register (128-bit)` | `D:Zd` | Is the name of the third scalable vector register Z8-Z11 or Z24-Z27 of the destination multi-vector group, encoded as "D:'10':Zd". |

### Encoding Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `size == '00'` |

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
- source: `luti4_mz4_ztmz2.xml`
</details>