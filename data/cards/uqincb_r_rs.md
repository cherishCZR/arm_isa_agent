## UQINCB
_ARM A64 Instruction_

**Title**: UQINCB -- A64 | **Class**: `sve` | **XML ID**: `uqincb_r_rs`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Unsigned saturating increment scalar by multiple of 8-bit predicate constraint element count

**Description**:
Determines the number of active 8-bit
elements implied by the named predicate constraint, multiplies
that by an immediate in the range 1 to 16 inclusive, and
then uses the result to increment the
  scalar destination.
The
  result is
  saturated to the
      general-purpose register's
  unsigned integer range.

The named predicate constraint limits the number of active
elements in a single predicate to:

Unspecified or out of range constraint encodings generate an
empty predicate or zero element count rather than Undefined
Instruction exception.

### Variant: `32-bit`
- **Assembly**: `UQINCB  <Wdn>{, <pattern>{, MUL #<imm>}}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  13  11 10  9   4  |
|-----------------------------------------|
| 000 0010 0   00  1   0   imm4 11  11  0   1   pattern Rdn |
```

#### Decode (A64.sve.sve_countelt.sve_int_pred_pattern_b.uqincb_r_rs_uw)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8;
constant integer dn = UInt(Rdn);
constant bits(5) pat = pattern;
constant integer imm = UInt(imm4) + 1;

constant boolean unsigned = TRUE;
constant integer ssize = 32;
```

#### Execute (A64.sve.sve_countelt.sve_int_pred_pattern_b.uqincb_r_rs_uw)

```
CheckSVEEnabled();
constant integer count = DecodePredCount(pat, esize);
constant bits(ssize) operand1 = X[dn, ssize];
bits(ssize) result;
constant integer element1 = Int(operand1, unsigned);
(result, -) = SatQ(element1 + (count * imm), ssize, unsigned);
X[dn, 64] = Extend(result, 64, unsigned);
```

### Variant: `64-bit`
- **Assembly**: `UQINCB  <Xdn>{, <pattern>{, MUL #<imm>}}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  13  11 10  9   4  |
|-----------------------------------------|
| 000 0010 0   00  1   1   imm4 11  11  0   1   pattern Rdn |
```

#### Decode (A64.sve.sve_countelt.sve_int_pred_pattern_b.uqincb_r_rs_x)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8;
constant integer dn = UInt(Rdn);
constant bits(5) pat = pattern;
constant integer imm = UInt(imm4) + 1;

constant boolean unsigned = TRUE;
constant integer ssize = 64;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wdn>` | `register (32-bit)` | `Rdn` | Is the 32-bit name of the source and destination general-purpose register, encoded in the "Rdn" field. |
| `<pattern>` | `unknown` | `pattern` | Is the optional pattern specifier, defaulting to ALL, |
| `<imm>` | `immediate` | `imm4` | Is the immediate multiplier, in the range 1 to 16, defaulting to 1, encoded in the "imm4" field. |
| `<Xdn>` | `register (64-bit)` | `Rdn` | Is the 64-bit name of the source and destination general-purpose register, encoded in the "Rdn" field. |

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

---
<details><summary>Metadata</summary>

- isa: `A64`
- sve-esize: `esize-byte`
- source: `uqincb_r_rs.xml`
</details>