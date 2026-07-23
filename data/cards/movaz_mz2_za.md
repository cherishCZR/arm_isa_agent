## MOVAZ
_ARM A64 Instruction_

**Title**: MOVAZ (tile to vector, two registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `movaz_mz2_za`

**Architecture**: `FEAT_SME2p1` (ARMv9.4)

**Summary**: Move and zero two ZA tile slices to vector registers

**Description**:
This instruction operates on two consecutive horizontal or
vertical slices within a named ZA tile of the specified element size. The tile slices are zeroed after moving their
contents to the destination vectors.

The consecutive slice numbers within the tile are selected starting from the
sum of the slice index register and immediate offset, modulo the number of
such elements in a vector.
The immediate offset is a multiple of 2 in the range 0 to the number
of elements in a 128-bit vector segment minus 2.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `8-bit`
- **Assembly**: `MOVAZ  { <Zd1>.B-<Zd2>.B }, ZA0<HV>.B[<Ws>, <offs1>:<offs2>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   7   4   0 |
|--------------------------------------------------|
| 1   10  0000 0   00  000 1   1   0   V   Rs  000 10  off3 Zd  0   |
```

#### Decode (A64.sme.mortlach_ext.mortlach_multi2_extract_zero.movaz_mz2_za_b1)

```
if !IsFeatureImplemented(FEAT_SME2p1) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt('011':Rs);
constant integer nreg = 2;
constant integer esize = 8;
constant integer d = UInt(Zd:'0');
constant integer n = 0;
constant integer offset = UInt(off3:'0');
constant boolean vertical = V == '1';
```

#### Execute (A64.sme.mortlach_ext.mortlach_multi2_extract_zero.movaz_mz2_za_b1)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
if nreg == 4 && esize == 64 && VL < 256 then EndOfDecode(Decode_UNDEF);
constant integer slices = VL DIV esize;
constant bits(32) index = X[s, 32];
constant integer slice = ((UInt(index) - (UInt(index) MOD nreg)) + offset) MOD slices;

for r = 0 to nreg-1
    constant bits(VL) result = ZAslice[n, esize, vertical, slice + r, VL];
    ZAslice[n, esize, vertical, slice + r, VL] = Zeros(VL);
    Z[d + r, VL] = result;
```

### Variant: `16-bit`
- **Assembly**: `MOVAZ  { <Zd1>.H-<Zd2>.H }, <ZAn><HV>.H[<Ws>, <offs1>:<offs2>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   7  6   4   0 |
|-----------------------------------------------------|
| 1   10  0000 0   01  000 1   1   0   V   Rs  000 10  ZAn off2 Zd  0   |
```

#### Decode (A64.sme.mortlach_ext.mortlach_multi2_extract_zero.movaz_mz2_za_h1)

```
if !IsFeatureImplemented(FEAT_SME2p1) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt('011':Rs);
constant integer nreg = 2;
constant integer esize = 16;
constant integer d = UInt(Zd:'0');
constant integer n = UInt(ZAn);
constant integer offset = UInt(off2:'0');
constant boolean vertical = V == '1';
```

### Variant: `32-bit`
- **Assembly**: `MOVAZ  { <Zd1>.S-<Zd2>.S }, <ZAn><HV>.S[<Ws>, <offs1>:<offs2>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   7   5  4   0 |
|-----------------------------------------------------|
| 1   10  0000 0   10  000 1   1   0   V   Rs  000 10  ZAn o1  Zd  0   |
```

#### Decode (A64.sme.mortlach_ext.mortlach_multi2_extract_zero.movaz_mz2_za_w1)

```
if !IsFeatureImplemented(FEAT_SME2p1) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt('011':Rs);
constant integer nreg = 2;
constant integer esize = 32;
constant integer d = UInt(Zd:'0');
constant integer n = UInt(ZAn);
constant integer offset = UInt(o1:'0');
constant boolean vertical = V == '1';
```

### Variant: `64-bit`
- **Assembly**: `MOVAZ  { <Zd1>.D-<Zd2>.D }, <ZAn><HV>.D[<Ws>, <offs1>:<offs2>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   7   4   0 |
|--------------------------------------------------|
| 1   10  0000 0   11  000 1   1   0   V   Rs  000 10  ZAn Zd  0   |
```

#### Decode (A64.sme.mortlach_ext.mortlach_multi2_extract_zero.movaz_mz2_za_d1)

```
if !IsFeatureImplemented(FEAT_SME2p1) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt('011':Rs);
constant integer nreg = 2;
constant integer esize = 64;
constant integer d = UInt(Zd:'0');
constant integer n = UInt(ZAn);
constant integer offset = 0;
constant boolean vertical = V == '1';
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | Is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 2. |
| `<Zd2>` | `register (128-bit)` | `Zd` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zd" times 2 plus 1. |
| `<HV>` | `register (16-bit)` | `V` | Is the horizontal or vertical slice indicator, |
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the slice index register W12-W15, encoded in the "Rs" field. |
| `<offs1>` | `unknown` | `off3` | For the "8-bit" variant: is the first slice index offset, encoded as "off3" field times 2. |
| `<offs1>` | `unknown` | `off2` | For the "16-bit" variant: is the first slice index offset, encoded as "off2" field times 2. |
| `<offs1>` | `unknown` | `o1` | For the "32-bit" variant: is the first slice index offset, encoded as "o1" field times 2. |
| `<offs1>` | `unknown` | `` | For the "64-bit" variant: is the first slice index offset, with implicit value 0. |
| `<offs2>` | `unknown` | `off3` | For the "8-bit" variant: is the second slice index offset, encoded as "off3" field times 2 plus 1. |
| `<offs2>` | `unknown` | `off2` | For the "16-bit" variant: is the second slice index offset, encoded as "off2" field times 2 plus 1. |
| `<offs2>` | `unknown` | `o1` | For the "32-bit" variant: is the second slice index offset, encoded as "o1" field times 2 plus 1. |
| `<offs2>` | `unknown` | `` | For the "64-bit" variant: is the second slice index offset, with implicit value 1. |
| `<ZAn>` | `register (128-bit)` | `ZAn` | For the "16-bit" variant: is the name of the ZA tile ZA0-ZA1 to be accessed, encoded in the "ZAn" field. |
| `<ZAn>` | `register (128-bit)` | `ZAn` | For the "32-bit" variant: is the name of the ZA tile ZA0-ZA3 to be accessed, encoded in the "ZAn" field. |
| `<ZAn>` | `register (128-bit)` | `ZAn` | For the "64-bit" variant: is the name of the ZA tile ZA0-ZA7 to be accessed, encoded in the "ZAn" field. |

**<HV> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | H |
| 1 | V |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2p1)` |

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
- source: `movaz_mz2_za.xml`
</details>