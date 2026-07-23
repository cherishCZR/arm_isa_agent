## LUTI2
_ARM A64 Instruction_

**Title**: LUTI2 (four registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `luti2_mz4_ztz`

**Architecture**: `FEAT_SME2` (ARMv9.3), `FEAT_SME2p1` (ARMv9.4)

**Summary**: Lookup table read with 2-bit indexes (four registers)

**Description**:
This instruction copies 8-bit, 16-bit or 32-bit elements from ZT0 to four destination
vectors using packed 2-bit indices from a segment of the source vector register.
A segment corresponds to a portion of the source vector that is consumed in order
to fill the destination vector. The segment is selected by the vector
segment index modulo the total number of segments.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `Consecutive`
- **Assembly**: `LUTI2  { <Zd1>.<T>-<Zd4>.<T> }, ZT0, <Zn>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  22 21  18 17  15  13  11   9   4   1  |
|--------------------------------------------|
| 1   10  0000 01  0   001 1   i2  10  size 00  Zn  Zd  00  |
```

#### Decode (A64.sme.mortlach_zt_expand_ctg.mortlach_expand_4dst_ctg.luti2_mz4_ztz_1)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if size == '11' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer isize = 2;
constant integer n = UInt(Zn);
constant integer dstride = 1;
constant integer d = UInt(Zd:'00');
constant integer imm = UInt(i2);
constant integer nreg = 4;
```

#### Execute (A64.sme.mortlach_zt_expand_ctg.mortlach_expand_4dst_ctg.luti2_mz4_ztz_1)

```
CheckStreamingSVEEnabled();
CheckSMEZT0Enabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer segments = esize DIV (isize * nreg);
constant integer segment = imm MOD segments;
constant bits(VL) indexes = Z[n, VL];
integer dst = d;
constant bits(512) table = ZT0[512];

for r = 0 to nreg-1
    constant integer base = (segment * nreg + r) * elements;
    bits(VL) result;
    for e = 0 to elements-1
        constant integer index = UInt(Elem[indexes, base+e, isize]);
        Elem[result, e, esize] = Elem[table, index, 32]<esize-1:0>;
    Z[dst, VL] = result;
    dst = dst + dstride;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |
| 🚫 ENCODING_UNDEF | `size != '11'` |

### Variant: `Strided`
- **Assembly**: `LUTI2  { <Zd1>.<T>, <Zd2>.<T>, <Zd3>.<T>, <Zd4>.<T> }, ZT0, <Zn>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24  18 17  15  13  11   9   4  3   1  |
|-----------------------------------------|
| 1   10  0000 010011 1   i2  10  size 00  Zn  D   00  Zd  |
```

#### Decode (A64.sme.mortlach_zt_expand_nctg.mortlach_expand_4dst_nctg.luti2_mz4_ztz_4)

```
if !IsFeatureImplemented(FEAT_SME2p1) then EndOfDecode(Decode_UNDEF);
if size == '10' || size == '11' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer isize = 2;
constant integer n = UInt(Zn);
constant integer dstride = 4;
constant integer d = UInt(D:'00':Zd);
constant integer imm = UInt(i2);
constant integer nreg = 4;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2p1)` |
| 🚫 ENCODING_UNDEF | `size != '10' && size != '11'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Consecutive" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 4. |
| `<Zd1>` | `register (128-bit)` | `D:Zd` | For the "Strided" variant: is the name of the first scalable vector register Z0-Z3 or Z16-Z19 of the destination multi-vector group, encoded as "D:'00 |
| `<T>` | `unknown` | `size` | For the "Consecutive" variant: is the size specifier, |
| `<T>` | `unknown` | `size<0>` | For the "Strided" variant: is the size specifier, |
| `<Zd4>` | `register (128-bit)` | `Zd` | For the "Consecutive" variant: is the name of the fourth scalable vector register of the destination multi-vector group, encoded as "Zd" times 4 plus  |
| `<Zd4>` | `register (128-bit)` | `D:Zd` | For the "Strided" variant: is the name of the fourth scalable vector register Z12-Z15 or Z28-Z31 of the destination multi-vector group, encoded as "D: |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<index>` | `unknown` | `i2` | Is the vector segment index, in the range 0 to 3, encoded in the "i2" field. |
| `<Zd2>` | `register (128-bit)` | `D:Zd` | Is the name of the second scalable vector register Z4-Z7 or Z20-Z23 of the destination multi-vector group, encoded as "D:'01':Zd". |
| `<Zd3>` | `register (128-bit)` | `D:Zd` | Is the name of the third scalable vector register Z8-Z11 or Z24-Z27 of the destination multi-vector group, encoded as "D:'10':Zd". |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | RESERVED |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | B |
| 1 | H |

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
- source: `luti2_mz4_ztz.xml`
</details>