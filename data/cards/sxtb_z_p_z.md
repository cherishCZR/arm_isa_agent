## sxtb_z_p_z
_ARM A64 Instruction_

**Title**: SXTB, SXTH, SXTW -- A64 | **Class**: `sve` | **XML ID**: `sxtb_z_p_z`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME), `FEAT_SVE2p2 || FEAT_SME2p2` (FEAT_SVE2p2 || FEAT_SME2p2)

**Summary**: Signed byte / halfword / word extend (predicated)

**Description**:
Sign-extend the least-significant sub-element  of
each active element of the source vector,
and place the results in the corresponding elements of the destination vector. 
Inactive elements in the destination vector register remain unmodified or
are set to zero, depending on whether merging or zeroing
predication is selected.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `Byte, merging`
- **Assembly**: `SXTB  <Zd>.<T>, <Pg>/M, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19 18  16 15  12   9   4  |
|-----------------------------------------|
| 000 0010 0   size 0   1   0   00  0   101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_int_pred_un.sve_int_un_pred_arit_0.sxtb_z_p_z_m)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer s_esize = 8;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean unsigned = FALSE;
constant boolean merging = TRUE;
```

#### Execute (A64.sve.sve_int_pred_un.sve_int_un_pred_arit_0.sxtb_z_p_z_m)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
bits(VL) result = if merging then Z[d, VL] else Zeros(VL);

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        constant bits(esize) element = Elem[operand, e, esize];
        Elem[result, e, esize] = Extend(element<s_esize-1:0>, esize, unsigned);

Z[d, VL] = result;
```

### Variant: `Byte, zeroing`
- **Assembly**: `SXTB  <Zd>.<T>, <Pg>/Z, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19 18  16 15  12   9   4  |
|-----------------------------------------|
| 000 0010 0   size 0   0   0   00  0   101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_int_pred_un.sve_int_un_pred_arit_0.sxtb_z_p_z_z)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer s_esize = 8;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean unsigned = FALSE;
constant boolean merging = FALSE;
```

### Variant: `Halfword, merging`
- **Assembly**: `SXTH  <Zd>.<T>, <Pg>/M, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19 18  16 15  12   9   4  |
|-----------------------------------------|
| 000 0010 0   size 0   1   0   01  0   101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_int_pred_un.sve_int_un_pred_arit_0.sxth_z_p_z_m)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size IN {'0x'} then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer s_esize = 16;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean unsigned = FALSE;
constant boolean merging = TRUE;
```

### Variant: `Halfword, zeroing`
- **Assembly**: `SXTH  <Zd>.<T>, <Pg>/Z, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19 18  16 15  12   9   4  |
|-----------------------------------------|
| 000 0010 0   size 0   0   0   01  0   101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_int_pred_un.sve_int_un_pred_arit_0.sxth_z_p_z_z)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
if size IN {'0x'} then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer s_esize = 16;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean unsigned = FALSE;
constant boolean merging = FALSE;
```

### Variant: `Word, merging`
- **Assembly**: `SXTW  <Zd>.D, <Pg>/M, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19 18  16 15  12   9   4  |
|-----------------------------------------|
| 000 0010 0   size 0   1   0   10  0   101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_int_pred_un.sve_int_un_pred_arit_0.sxtw_z_p_z_m)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size != '11' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer s_esize = 32;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean unsigned = FALSE;
constant boolean merging = TRUE;
```

### Variant: `Word, zeroing`
- **Assembly**: `SXTW  <Zd>.D, <Pg>/Z, <Zn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19 18  16 15  12   9   4  |
|-----------------------------------------|
| 000 0010 0   size 0   0   0   10  0   101 Pg  Zn  Zd  |
```

#### Decode (A64.sve.sve_int_pred_un.sve_int_un_pred_arit_0.sxtw_z_p_z_z)

```
if !IsFeatureImplemented(FEAT_SVE2p2) && !IsFeatureImplemented(FEAT_SME2p2) then
    EndOfDecode(Decode_UNDEF);
if size != '11' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer s_esize = 32;
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean unsigned = FALSE;
constant boolean merging = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | For the "Byte, merging" and "Byte, zeroing" variants: is the size specifier, |
| `<T>` | `unknown` | `size<0>` | For the "Halfword, merging" and "Halfword, zeroing" variants: is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | S |
| 1 | D |

### Encoding Constraints
_3× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p2) \|\| IsFeatureImplemented(FEAT_SME2p2)` |
| 🚫 ENCODING_UNDEF | `size IN{'0x'}` |
| 🚫 ENCODING_UNDEF | `size == '11'` |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
        
        The merging variant of this instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and the merging variant of this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX can be predicated or unpredicated.
          
          
            A predicated MOVPRFX must use the same governing predicate register as the merging variant this instruction.
          
          
            A predicated MOVPRFX must use the larger of the destination element size and first s
... (truncated)

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sxtb_z_p_z.xml`
</details>