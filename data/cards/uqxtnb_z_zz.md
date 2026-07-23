## UQXTNB
_ARM A64 Instruction_

**Title**: UQXTNB -- A64 | **Class**: `sve2` | **XML ID**: `uqxtnb_z_zz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Unsigned saturating extract narrow (bottom)

**Description**:
Saturate the unsigned integer value in each source element to half the
original source element width, and place the results in the
even-numbered half-width destination elements, while setting the
odd-numbered elements to zero.

### Variant: `SVE2`
- **Assembly**: `UQXTNB  <Zd>.<T>, <Zn>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  16 15 14  12 11 10  9   4  |
|--------------------------------------------------|
| 010 0010 1   0   tszh 1   tszl 00  0   0   10  0   1   0   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_narrowing.sve_intx_extract_narrow.uqxtnb_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant bits(3) tsize = tszh:tszl;
if !(tsize IN {'001', '010', '100'}) then EndOfDecode(Decode_UNDEF);
constant integer esize = 16 << HighestSetBitNZ(tsize);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_intx_narrowing.sve_intx_extract_narrow.uqxtnb_z_zz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[n, VL];
bits(VL) result;
constant integer halfesize = esize DIV 2;

for e = 0 to elements-1
    constant integer element1 = UInt(Elem[operand1, e, esize]);
    constant bits(halfesize) res = UnsignedSat(element1, halfesize);
    Elem[result, 2*e + 0, halfesize] = res;
    Elem[result, 2*e + 1, halfesize] = Zeros(halfesize);

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `tszh:tszl IN{'001', '010', '100'}` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `arrangement` | `tszh:tszl` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<Tb>` | `unknown` | `tszh:tszl` | Is the size specifier, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | B |
| 10 | H |
| 11 | RESERVED |
| 00 | S |
| 01 | RESERVED |
| 1x | RESERVED |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | RESERVED |
| 00 | D |
| 01 | RESERVED |
| 1x | RESERVED |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `uqxtnb_z_zz.xml`
</details>