## MOVA
_ARM A64 Instruction_

**Title**: MOVA (vector to tile, single) -- A64 | **Class**: `mortlach` | **XML ID**: `mova_za_p_rz`

**Architecture**: `FEAT_SME` (PROFILE_A)

**Summary**: Move vector register to ZA tile slice

**Description**:
This instruction operates on individual horizontal or vertical slices
within a named ZA tile of the specified element size.
The slice number within the tile is selected by
the sum of the slice index register and immediate offset,
modulo the number of such elements in a vector.
The immediate offset is in the range 0 to the number of elements in a 128-bit vector segment minus 1.

Inactive elements in the destination slice remain unmodified.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `8-bit`
- **Assembly**: `MOVA  ZA0<HV>.B[<Ws>, <offs>], <Pg>/M, <Zn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   4  3  |
|-----------------------------------------------|
| 1   10  0000 0   00  000 0   0   0   V   Rs  Pg  Zn  0   off4 |
```

#### Decode (A64.sme.mortlach_ins.mortlach_insert_pred.mova_za_p_rz_b)

```
if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
constant integer g = UInt(Pg);
constant integer s = UInt('011':Rs);
constant integer n = UInt(Zn);
constant integer d = 0;
constant integer offset = UInt(off4);
constant integer esize = 8;
constant boolean vertical = V == '1';
```

#### Execute (A64.sme.mortlach_ins.mortlach_insert_pred.mova_za_p_rz_b)

```
CheckStreamingSVEAndZAEnabled();
constant integer  VL = CurrentVL;
constant integer  PL = VL DIV 8;
constant integer  dim = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = Z[n, VL];
constant bits(32) index = X[s, 32];
constant integer  slice = (UInt(index) + offset) MOD dim;
bits(VL) result = ZAslice[d, esize, vertical, slice, VL];

for e = 0 to dim-1
    constant bits(esize) element = Elem[operand, e, esize];
    if ActivePredicateElement(mask, e, esize) then
        Elem[result, e, esize] = element;

ZAslice[d, esize, vertical, slice, VL] = result;
```

### Variant: `16-bit`
- **Assembly**: `MOVA  <ZAd><HV>.H[<Ws>, <offs>], <Pg>/M, <Zn>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   4  3  2  |
|--------------------------------------------------|
| 1   10  0000 0   01  000 0   0   0   V   Rs  Pg  Zn  0   ZAd off3 |
```

#### Decode (A64.sme.mortlach_ins.mortlach_insert_pred.mova_za_p_rz_h)

```
if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
constant integer g = UInt(Pg);
constant integer s = UInt('011':Rs);
constant integer n = UInt(Zn);
constant integer d = UInt(ZAd);
constant integer offset = UInt(off3);
constant integer esize = 16;
constant boolean vertical = V == '1';
```

### Variant: `32-bit`
- **Assembly**: `MOVA  <ZAd><HV>.S[<Ws>, <offs>], <Pg>/M, <Zn>.S`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   4  3   1  |
|--------------------------------------------------|
| 1   10  0000 0   10  000 0   0   0   V   Rs  Pg  Zn  0   ZAd off2 |
```

#### Decode (A64.sme.mortlach_ins.mortlach_insert_pred.mova_za_p_rz_w)

```
if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
constant integer g = UInt(Pg);
constant integer s = UInt('011':Rs);
constant integer n = UInt(Zn);
constant integer d = UInt(ZAd);
constant integer offset = UInt(off2);
constant integer esize = 32;
constant boolean vertical = V == '1';
```

### Variant: `64-bit`
- **Assembly**: `MOVA  <ZAd><HV>.D[<Ws>, <offs>], <Pg>/M, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   4  3   0 |
|--------------------------------------------------|
| 1   10  0000 0   11  000 0   0   0   V   Rs  Pg  Zn  0   ZAd o1  |
```

#### Decode (A64.sme.mortlach_ins.mortlach_insert_pred.mova_za_p_rz_d)

```
if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
constant integer g = UInt(Pg);
constant integer s = UInt('011':Rs);
constant integer n = UInt(Zn);
constant integer d = UInt(ZAd);
constant integer offset = UInt(o1);
constant integer esize = 64;
constant boolean vertical = V == '1';
```

### Variant: `128-bit`
- **Assembly**: `MOVA  <ZAd><HV>.Q[<Ws>, <offs>], <Pg>/M, <Zn>.Q`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21  18 17 16 15 14  12   9   4  3  |
|-----------------------------------------------|
| 1   10  0000 0   11  000 0   0   1   V   Rs  Pg  Zn  0   ZAd |
```

#### Decode (A64.sme.mortlach_ins.mortlach_insert_pred.mova_za_p_rz_q)

```
if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
constant integer g = UInt(Pg);
constant integer s = UInt('011':Rs);
constant integer n = UInt(Zn);
constant integer d = UInt(ZAd);
constant integer offset = 0;
constant integer esize = 128;
constant boolean vertical = V == '1';
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<HV>` | `register (16-bit)` | `V` | Is the horizontal or vertical slice indicator, |
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the slice index register W12-W15, encoded in the "Rs" field. |
| `<offs>` | `unknown` | `off4` | For the "8-bit" variant: is the slice index offset, in the range 0 to 15, encoded in the "off4" field. |
| `<offs>` | `unknown` | `off3` | For the "16-bit" variant: is the slice index offset, in the range 0 to 7, encoded in the "off3" field. |
| `<offs>` | `unknown` | `off2` | For the "32-bit" variant: is the slice index offset, in the range 0 to 3, encoded in the "off2" field. |
| `<offs>` | `unknown` | `o1` | For the "64-bit" variant: is the slice index offset, in the range 0 to 1, encoded in the "o1" field. |
| `<offs>` | `unknown` | `` | For the "128-bit" variant: is the slice index offset, with implicit value 0. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<ZAd>` | `register (128-bit)` | `ZAd` | For the "16-bit" variant: is the name of the ZA tile ZA0-ZA1 to be accessed, encoded in the "ZAd" field. |
| `<ZAd>` | `register (128-bit)` | `ZAd` | For the "32-bit" variant: is the name of the ZA tile ZA0-ZA3 to be accessed, encoded in the "ZAd" field. |
| `<ZAd>` | `register (128-bit)` | `ZAd` | For the "64-bit" variant: is the name of the ZA tile ZA0-ZA7 to be accessed, encoded in the "ZAd" field. |
| `<ZAd>` | `register (128-bit)` | `ZAd` | For the "128-bit" variant: is the name of the ZA tile ZA0-ZA15 to be accessed, encoded in the "ZAd" field. |

**<HV> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | H |
| 1 | V |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME)` |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `mova_za_p_rz.xml`
</details>