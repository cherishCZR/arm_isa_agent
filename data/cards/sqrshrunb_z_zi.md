## SQRSHRUNB
_ARM A64 Instruction_

**Title**: SQRSHRUNB -- A64 | **Class**: `sve2` | **XML ID**: `sqrshrunb_z_zi`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Signed saturating rounding shift right unsigned narrow by immediate (bottom)

**Description**:
Shift each signed integer value in the source
vector elements right by an immediate value,
and place the rounded results in the even-numbered half-width destination
elements, while setting the odd-numbered elements to zero.
Each result element is saturated to the
half-width N-bit element's
unsigned integer range 0 to (2N)-1.
The immediate shift amount is an unsigned value in the range 1
to number of bits per element.
This instruction is unpredicated.

### Variant: `SVE2`
- **Assembly**: `SQRSHRUNB  <Zd>.<T>, <Zn>.<Tb>, #<const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  15 14 13 12 11 10  9   4  |
|--------------------------------------------------|
| 010 0010 1   0   tszh 1   tszl imm3 0   0   0   0   1   0   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_narrowing.sve_intx_shift_narrow.sqrshrunb_z_zi_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant bits(3) tsize = tszh:tszl;
if tsize == '000' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << HighestSetBit(tsize);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer shift = (2 * esize) - UInt(tsize:imm3);
```

#### Execute (A64.sve.sve_intx_narrowing.sve_intx_shift_narrow.sqrshrunb_z_zi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV (2 * esize);
constant bits(VL) operand = Z[n, VL];
bits(VL) result;
for e = 0 to elements-1
    constant bits(2*esize) element = Elem[operand, e, 2*esize];
    constant integer res = (SInt(element) + (1 << (shift-1))) >> shift;
    Elem[result, 2*e + 0, esize] = UnsignedSat(res, esize);
    Elem[result, 2*e + 1, esize] = Zeros(esize);

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `tszh:tszl != '000'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `arrangement` | `tszh:tszl` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<Tb>` | `unknown` | `tszh:tszl` | Is the size specifier, |
| `<const>` | `unknown` | `tszh:tszl:imm3` | Is the immediate shift amount, in the range 1 to number of bits per element, encoded in "tszh:tszl:imm3". |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | B |
| 1x | H |
| xx | S |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 1x | S |
| xx | D |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqrshrunb_z_zi.xml`
</details>