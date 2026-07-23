## INCP
_ARM A64 Instruction_

**Title**: INCP (vector) -- A64 | **Class**: `sve` | **XML ID**: `incp_z_p_z`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Increment vector by count of true predicate elements

**Description**:
Counts the number of true elements in the source predicate and
then uses the result to increment all destination vector elements.

The predicate size specifier may be omitted in assembler
   source code, but this is deprecated and will be
   prohibited in a future release of the architecture.

### Variant: `SVE`
- **Assembly**: `INCP  <Zdn>.<T>, <Pm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18 17 16 15  11 10   8   4  |
|-----------------------------------------|
| 001 0010 1   size 101 1   0   0   1000 0   00  Pm  Zdn |
```

#### Decode (A64.sve.sve_pred_count_b.sve_int_count_v.incp_z_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer m = UInt(Pm);
constant integer dn = UInt(Zdn);
```

#### Execute (A64.sve.sve_pred_count_b.sve_int_count_v.incp_z_p_z_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[dn, VL];
constant bits(PL) operand2 = P[m, PL];
bits(VL) result;
integer count = 0;

for e = 0 to elements-1
    if ActivePredicateElement(operand2, e, esize) then
        count = count + 1;

for e = 0 to elements-1
    Elem[result, e, esize] = Elem[operand1, e, esize] + count;

Z[dn, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the source and destination scalable vector register, encoded in the "Zdn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pm>` | `unknown` | `Pm` | Is the name of the source scalable predicate register, encoded in the "Pm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `incp_z_p_z.xml`
</details>