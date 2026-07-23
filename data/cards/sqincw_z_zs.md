## SQINCW
_ARM A64 Instruction_

**Title**: SQINCW (vector) -- A64 | **Class**: `sve` | **XML ID**: `sqincw_z_zs`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Signed saturating increment vector by multiple of 32-bit predicate constraint element count

**Description**:
Determines the number of active 32-bit
elements implied by the named predicate constraint, multiplies
that by an immediate in the range 1 to 16 inclusive, and
then uses the result to increment all destination vector elements.
The
  results are
  saturated to the
  32-bit 
  signed integer range.

The named predicate constraint limits the number of active
elements in a single predicate to:

Unspecified or out of range constraint encodings generate an
empty predicate or zero element count rather than Undefined
Instruction exception.

### Variant: `SVE`
- **Assembly**: `SQINCW  <Zdn>.S{, <pattern>{, MUL #<imm>}}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  13  11 10  9   4  |
|-----------------------------------------|
| 000 0010 0   10  1   0   imm4 11  00  0   0   pattern Zdn |
```

#### Decode (A64.sve.sve_countelt.sve_int_countvlv0.sqincw_z_zs_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer dn = UInt(Zdn);
constant bits(5) pat = pattern;
constant integer imm = UInt(imm4) + 1;

constant boolean unsigned = FALSE;
```

#### Execute (A64.sve.sve_countelt.sve_int_countvlv0.sqincw_z_zs_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer count = DecodePredCount(pat, esize);
constant bits(VL) operand1 = Z[dn, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer element1 = Int(Elem[operand1, e, esize], unsigned);
    (Elem[result, e, esize], -) = SatQ(element1 + (count * imm), esize, unsigned);

Z[dn, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the source and destination scalable vector register, encoded in the "Zdn" field. |
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

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- sve-esize: `esize-word`
- source: `sqincw_z_zs.xml`
</details>