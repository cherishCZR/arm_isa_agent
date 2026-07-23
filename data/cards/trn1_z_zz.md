## trn1_z_zz
_ARM A64 Instruction_

**Title**: TRN1, TRN2 (vectors) -- A64 | **Class**: `sve` | **XML ID**: `trn1_z_zz`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME), `FEAT_F64MM` (PROFILE_A)

**Summary**: Interleave even or odd elements from two vectors

**Description**:
Interleave alternating even or odd-numbered elements
from the 
first and second source vectors and place in
elements of the destination vector.  This instruction is unpredicated.

The 128-bit element variant requires that the Effective SVE vector
length is at least 256 bits.
ID_AA64ZFR0_EL1.F64MM indicates whether the 128-bit element variant
is implemented.
The 128-bit element variant
is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64
is implemented and enabled.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_only`

### Variant: `Even`
- **Assembly**: `TRN1  <Zd>.<T>, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12  10  9   4  |
|-----------------------------------|
| 000 0010 1   size 1   Zm  011 10  0   Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_inter.sve_int_perm_bin_perm_zz.trn1_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant integer part = 0;
```

#### Execute (A64.sve.sve_perm_inter.sve_int_perm_bin_perm_zz.trn1_z_zz_)

```
if esize < 128 then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
if VL < esize * 2 then EndOfDecode(Decode_UNDEF);
constant integer pairs = VL DIV (esize * 2);
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result = Zeros(VL);

for p = 0 to pairs-1
    Elem[result, 2*p+0, esize] = Elem[operand1, 2*p+part, esize];
    Elem[result, 2*p+1, esize] = Elem[operand2, 2*p+part, esize];

Z[d, VL] = result;
```

### Variant: `Even (quadwords)`
- **Assembly**: `TRN1  <Zd>.Q, <Zn>.Q, <Zm>.Q`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24  22 21 20  15  12  10  9   4  |
|-----------------------------------|
| 000 0010 11  0   1   Zm  000 11  0   Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_inter_long.sve_int_perm_bin_long_perm_zz.trn1_z_zz_q)

```
if !IsFeatureImplemented(FEAT_F64MM) then EndOfDecode(Decode_UNDEF);
constant integer esize = 128;
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant integer part = 0;
```

### Variant: `Odd`
- **Assembly**: `TRN2  <Zd>.<T>, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12  10  9   4  |
|-----------------------------------|
| 000 0010 1   size 1   Zm  011 10  1   Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_inter.sve_int_perm_bin_perm_zz.trn2_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant integer part = 1;
```

### Variant: `Odd (quadwords)`
- **Assembly**: `TRN2  <Zd>.Q, <Zn>.Q, <Zm>.Q`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24  22 21 20  15  12  10  9   4  |
|-----------------------------------|
| 000 0010 11  0   1   Zm  000 11  1   Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_inter_long.sve_int_perm_bin_long_perm_zz.trn2_z_zz_q)

```
if !IsFeatureImplemented(FEAT_F64MM) then EndOfDecode(Decode_UNDEF);
constant integer esize = 128;
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant integer part = 1;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

### Encoding Constraints
_2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_F64MM)` |

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
- source: `trn1_z_zz.xml`
</details>