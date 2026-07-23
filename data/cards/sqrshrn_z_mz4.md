## SQRSHRN
_ARM A64 Instruction_

**Title**: SQRSHRN -- A64 | **Class**: `mortlach2` | **XML ID**: `sqrshrn_z_mz4`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector signed saturating rounding shift right narrow by immediate and interleave

**Description**:
This instruction shifts right by an immediate value the signed integer value in each element of the
four source vectors, and places the four-way
interleaved rounded results in the quarter-width destination
elements. Each result element is saturated to the quarter-width
N-bit element's signed integer range -2(N-1)
to (2(N-1))-1. The immediate shift amount is an unsigned value in the
range 1 to number of bits per source element.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `SQRSHRN  <Zd>.<T>, { <Zn1>.<Tb>-<Zn4>.<Tb> }, #<const>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12  10  9   6  5  4  |
|--------------------------------------------|
| 1   10  0000 1   tsize 1   imm5 110 11  1   Zn  0   0   Zd  |
```

#### Decode (A64.sme.mortlach_multi_sve_3.mortlach_multi4_qrshr.sqrshrn_z_mz4_)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if tsize == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << HighestSetBit(tsize);
constant integer n = UInt(Zn:'00');
constant integer d = UInt(Zd);
constant integer shift = (8 * esize) - UInt(tsize:imm5);
```

#### Execute (A64.sme.mortlach_multi_sve_3.mortlach_multi4_qrshr.sqrshrn_z_mz4_)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV (4 * esize);
bits(VL) result;

for e = 0 to elements-1
    for i = 0 to 3
        constant bits(VL) operand = Z[n+i, VL];
        constant bits(4 * esize) element = Elem[operand, e, 4 * esize];
        constant integer res = (SInt(element) + (1 << (shift-1))) >> shift;
        Elem[result, 4*e + i, esize] = SignedSat(res, esize);

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |
| 🚫 ENCODING_UNDEF | `tsize != '00'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `tsize` | Is the size specifier, |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 4. |
| `<Tb>` | `unknown` | `tsize` | Is the size specifier, |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the source multi-vector group, encoded as "Zn" times 4 plus 3. |
| `<const>` | `unknown` | `tsize:imm5` | Is the immediate shift amount, in the range 1 to number of bits per source element, encoded in "tsize:imm5". |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | B |
| 1x | H |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | S |
| 1x | D |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqrshrn_z_mz4.xml`
</details>