## cntb_r_s
_ARM A64 Instruction_

**Title**: CNTB, CNTD, CNTH, CNTW -- A64 | **Class**: `sve` | **XML ID**: `cntb_r_s`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Set scalar to multiple of predicate constraint element count

**Description**:
Determines the number of active 
elements implied by the named predicate constraint, multiplies
that by an immediate in the range 1 to 16 inclusive, and
then places the result in the
  scalar destination.

The named predicate constraint limits the number of active
elements in a single predicate to:

Unspecified or out of range constraint encodings generate an
empty predicate or zero element count rather than Undefined
Instruction exception.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `Byte`
- **Assembly**: `CNTB  <Xd>{, <pattern>{, MUL #<imm>}}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  13  10  9   4  |
|--------------------------------------|
| 000 0010 0   00  1   0   imm4 11  100 0   pattern Rd  |
```

#### Decode (A64.sve.sve_countelt.sve_int_count.cntb_r_s_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8;
constant integer d = UInt(Rd);
constant bits(5) pat = pattern;
constant integer imm = UInt(imm4) + 1;
```

#### Execute (A64.sve.sve_countelt.sve_int_count.cntb_r_s_)

```
CheckSVEEnabled();
constant integer count = DecodePredCount(pat, esize);
X[d, 64] = (count * imm)<63:0>;
```

### Variant: `Doubleword`
- **Assembly**: `CNTD  <Xd>{, <pattern>{, MUL #<imm>}}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  13  10  9   4  |
|--------------------------------------|
| 000 0010 0   11  1   0   imm4 11  100 0   pattern Rd  |
```

#### Decode (A64.sve.sve_countelt.sve_int_count.cntd_r_s_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer d = UInt(Rd);
constant bits(5) pat = pattern;
constant integer imm = UInt(imm4) + 1;
```

### Variant: `Halfword`
- **Assembly**: `CNTH  <Xd>{, <pattern>{, MUL #<imm>}}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  13  10  9   4  |
|--------------------------------------|
| 000 0010 0   01  1   0   imm4 11  100 0   pattern Rd  |
```

#### Decode (A64.sve.sve_countelt.sve_int_count.cnth_r_s_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer d = UInt(Rd);
constant bits(5) pat = pattern;
constant integer imm = UInt(imm4) + 1;
```

### Variant: `Word`
- **Assembly**: `CNTW  <Xd>{, <pattern>{, MUL #<imm>}}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  13  10  9   4  |
|--------------------------------------|
| 000 0010 0   10  1   0   imm4 11  100 0   pattern Rd  |
```

#### Decode (A64.sve.sve_countelt.sve_int_count.cntw_r_s_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer d = UInt(Rd);
constant bits(5) pat = pattern;
constant integer imm = UInt(imm4) + 1;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the destination general-purpose register, encoded in the "Rd" field. |
| `<pattern>` | `unknown` | `pattern` | Is the optional pattern specifier, defaulting to ALL, |
| `<imm>` | `immediate` | `imm4` | Is the immediate multiplier, in the range 1 to 16, defaulting to 1, encoded in the "imm4" field. |

**<pattern> Value Table**:

| bitfield | symbol |
|---|---|
| 00000 | POW2 |
| 00001 | VL1 |
| 00010 | VL2 |
| 00011 | VL3 |
| 00100 | VL4 |
| 00101 | VL5 |
| 00110 | VL6 |
| 00111 | VL7 |
| 01000 | VL8 |
| 01001 | VL16 |
| 01010 | VL32 |
| 01011 | VL64 |
| 01100 | VL128 |
| 01101 | VL256 |
| 0111x | #uimm5 |
| 1xx00 | #uimm5 |
| 1x0x1 | #uimm5 |
| 1x010 | #uimm5 |
| 101x1 | #uimm5 |
| 10110 | #uimm5 |
| 11101 | MUL4 |
| 11110 | MUL3 |
| 11111 | ALL |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

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
- source: `cntb_r_s.xml`
</details>