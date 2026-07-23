## SQCVT
_ARM A64 Instruction_

**Title**: SQCVT (four registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `sqcvt_z_mz4`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Multi-vector signed saturating extract narrow

**Description**:
This instruction saturates the signed integer value in each element of the four source
vectors to  quarter the original source element width, and places the   results in the quarter-width
destination elements.

This instruction is unpredicated.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `SQCVT  <Zd>.<T>, { <Zn1>.<Tb>-<Zn4>.<Tb> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23 22 21 20  17  15   9   6  5  4  |
|--------------------------------------------|
| 1   10  0000 1   sz  0   1   100 11  111000 Zn  0   0   Zd  |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi4_narrow_int_cvrt.sqcvt_z_mz4_)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(sz);
constant integer n = UInt(Zn:'00');
constant integer d = UInt(Zd);
```

#### Execute (A64.sme.mortlach_multi_sve_4.mortlach_multi4_narrow_int_cvrt.sqcvt_z_mz4_)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV (4 * esize);
bits(VL) result;

for r = 0 to 3
    constant bits(VL) operand = Z[n+r, VL];
    for e = 0 to elements-1
        constant integer element = SInt(Elem[operand, e, 4 * esize]);
        Elem[result, r*elements + e, esize] = SignedSat(element, esize);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `sz` | Is the size specifier, |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 4. |
| `<Tb>` | `unknown` | `sz` | Is the size specifier, |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the source multi-vector group, encoded as "Zn" times 4 plus 3. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | B |
| 1 | H |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | S |
| 1 | D |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqcvt_z_mz4.xml`
</details>