## UQCVTN
_ARM A64 Instruction_

**Title**: UQCVTN -- A64 | **Class**: `sve2` | **XML ID**: `uqcvtn_z_mz2`

**Architecture**: `FEAT_SME2 || FEAT_SVE2p1` (FEAT_SME2 || FEAT_SVE2p1)

**Summary**: Unsigned 32-bit integer saturating extract narrow and interleave to 16-bit integer

**Description**:
Saturate the unsigned integer value in each element of the group of
two source vectors to half the original source element width,
and place the two-way interleaved results in the half-width destination elements.

This instruction is unpredicated.

### Variant: `SVE2`
- **Assembly**: `UQCVTN  <Zd>.H, { <Zn1>.S-<Zn2>.S }`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  16 15 14  12 11 10  9   5  4  |
|-----------------------------------------------------|
| 010 0010 1   0   0   1   10  00  1   0   10  0   1   0   Zn  0   Zd  |
```

#### Decode (A64.sve.sve_intx_narrowing.sve_intx_multi_extract_narrow.uqcvtn_z_mz2_)

```
if !IsFeatureImplemented(FEAT_SME2) && !IsFeatureImplemented(FEAT_SVE2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer n = UInt(Zn:'0');
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_intx_narrowing.sve_intx_multi_extract_narrow.uqcvtn_z_mz2_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV (2 * esize);
bits(VL) result;

for e = 0 to elements-1
    for i = 0 to 1
        constant bits(VL) operand = Z[n+i, VL];
        constant integer element = UInt(Elem[operand, e, 2 * esize]);
        Elem[result, 2*e + i, esize] = UnsignedSat(element, esize);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) \|\| IsFeatureImplemented(FEAT_SVE2p1)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 2. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the source multi-vector group, encoded as "Zn" times 2 plus 1. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `uqcvtn_z_mz2.xml`
</details>