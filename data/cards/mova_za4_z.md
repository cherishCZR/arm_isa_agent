## MOVA
_ARM A64 Instruction_

**Title**: MOVA (vector to tile, four registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `mova_za4_z`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Move four vector registers to four ZA tile slices

**Description**:
This instruction operates on four consecutive horizontal or
vertical slices within a named ZA tile of the specified element size.

The consecutive slice numbers within the tile are selected starting from the
sum of the slice index register and immediate offset, modulo the number of
such elements in a vector.
The immediate offset is a multiple of 4 in the range 0 to the number
of elements in a 128-bit vector segment minus 4.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `8-bit`
- **Assembly**: `MOVA  ZA0<HV>.B[<Ws>, <offs1>:<offs4>], { <Zn1>.B-<Zn4>.B }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   6   4  3  2  1  |
|--------------------------------------------------------|
| 1   10  0000 0   00  000 1   0   0   V   Rs  001 Zn  00  0   0   0   off2 |
```

#### Decode (A64.sme.mortlach_ins.mortlach_multi4_insert_ctg.mova_za4_z_b1)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt('011':Rs);
constant integer nreg = 4;
constant integer esize = 8;
constant integer n = UInt(Zn:'00');
constant integer d = 0;
constant integer offset = UInt(off2:'00');
constant boolean vertical = V == '1';
```

#### Execute (A64.sme.mortlach_ins.mortlach_multi4_insert_ctg.mova_za4_z_b1)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
if nreg == 4 && esize == 64 && VL < 256 then EndOfDecode(Decode_UNDEF);
constant integer slices = VL DIV esize;
constant bits(32) index = X[s, 32];
constant integer slice = ((UInt(index) - (UInt(index) MOD nreg)) + offset) MOD slices;

for r = 0 to nreg-1
    constant bits(VL) result = Z[n + r, VL];
    ZAslice[d, esize, vertical, slice + r, VL] = result;
```

### Variant: `16-bit`
- **Assembly**: `MOVA  <ZAd><HV>.H[<Ws>, <offs1>:<offs4>], { <Zn1>.H-<Zn4>.H }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   6   4  3  2  1  0 |
|-----------------------------------------------------------|
| 1   10  0000 0   01  000 1   0   0   V   Rs  001 Zn  00  0   0   0   ZAd o1  |
```

#### Decode (A64.sme.mortlach_ins.mortlach_multi4_insert_ctg.mova_za4_z_h1)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt('011':Rs);
constant integer nreg = 4;
constant integer esize = 16;
constant integer n = UInt(Zn:'00');
constant integer d = UInt(ZAd);
constant integer offset = UInt(o1:'00');
constant boolean vertical = V == '1';
```

### Variant: `32-bit`
- **Assembly**: `MOVA  <ZAd><HV>.S[<Ws>, <offs1>:<offs4>], { <Zn1>.S-<Zn4>.S }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   6   4  3  2  1  |
|--------------------------------------------------------|
| 1   10  0000 0   10  000 1   0   0   V   Rs  001 Zn  00  0   0   0   ZAd |
```

#### Decode (A64.sme.mortlach_ins.mortlach_multi4_insert_ctg.mova_za4_z_w1)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt('011':Rs);
constant integer nreg = 4;
constant integer esize = 32;
constant integer n = UInt(Zn:'00');
constant integer d = UInt(ZAd);
constant integer offset = 0;
constant boolean vertical = V == '1';
```

### Variant: `64-bit`
- **Assembly**: `MOVA  <ZAd><HV>.D[<Ws>, <offs1>:<offs4>], { <Zn1>.D-<Zn4>.D }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   6   4  3  2  |
|-----------------------------------------------------|
| 1   10  0000 0   11  000 1   0   0   V   Rs  001 Zn  00  0   0   ZAd |
```

#### Decode (A64.sme.mortlach_ins.mortlach_multi4_insert_ctg.mova_za4_z_d1)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if MaxImplementedSVL() < 256 then EndOfDecode(Decode_UNDEF);
constant integer s = UInt('011':Rs);
constant integer nreg = 4;
constant integer esize = 64;
constant integer n = UInt(Zn:'00');
constant integer d = UInt(ZAd);
constant integer offset = 0;
constant boolean vertical = V == '1';
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `MaxImplementedSVL() < 256` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<HV>` | `register (16-bit)` | `V` | Is the horizontal or vertical slice indicator, |
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the slice index register W12-W15, encoded in the "Rs" field. |
| `<offs1>` | `unknown` | `off2` | For the "8-bit" variant: is the first slice index offset, encoded as "off2" field times 4. |
| `<offs1>` | `unknown` | `o1` | For the "16-bit" variant: is the first slice index offset, encoded as "o1" field times 4. |
| `<offs1>` | `unknown` | `` | For the "32-bit" and "64-bit" variants: is the first slice index offset, with implicit value 0. |
| `<offs4>` | `unknown` | `off2` | For the "8-bit" variant: is the fourth slice index offset, encoded as "off2" field times 4 plus 3. |
| `<offs4>` | `unknown` | `o1` | For the "16-bit" variant: is the fourth slice index offset, encoded as "o1" field times 4 plus 3. |
| `<offs4>` | `unknown` | `` | For the "32-bit" and "64-bit" variants: is the fourth slice index offset, with implicit value 3. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 4. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the source multi-vector group, encoded as "Zn" times 4 plus 3. |
| `<ZAd>` | `register (128-bit)` | `ZAd` | For the "16-bit" variant: is the name of the ZA tile ZA0-ZA1 to be accessed, encoded in the "ZAd" field. |
| `<ZAd>` | `register (128-bit)` | `ZAd` | For the "32-bit" variant: is the name of the ZA tile ZA0-ZA3 to be accessed, encoded in the "ZAd" field. |
| `<ZAd>` | `register (128-bit)` | `ZAd` | For the "64-bit" variant: is the name of the ZA tile ZA0-ZA7 to be accessed, encoded in the "ZAd" field. |

**<HV> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | H |
| 1 | V |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

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
- source: `mova_za4_z.xml`
</details>