## FDUP
_ARM A64 Instruction_

**Title**: FDUP -- A64 | **Class**: `sve` | **XML ID**: `fdup_z_i`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Broadcast 8-bit floating-point immediate to vector elements (unpredicated)

**Description**:
Unconditionally broadcast the floating-point immediate into each element of the
destination vector. This instruction is unpredicated.

### Variant: `SVE`
- **Assembly**: `FDUP  <Zd>.<T>, #<const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  16 15  13 12   4  |
|--------------------------------------|
| 001 0010 1   size 1   11  00  1   11  0   imm8 Zd  |
```

#### Decode (A64.sve.sve_wideimm_unpred.sve_int_dup_fpimm.fdup_z_i_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer d = UInt(Zd);
constant bits(esize) imm = VFPExpandImm(imm8, esize);
```

#### Execute (A64.sve.sve_wideimm_unpred.sve_int_dup_fpimm.fdup_z_i_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
bits(VL) result;

for e = 0 to elements-1
    Elem[result, e, esize] = imm;

Z[d, VL] = result;
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
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<const>` | `unknown` | `imm8` | Is a floating-point immediate value expressible as ±n÷16×2^r, where n and r are integers such that 16 ≤ n ≤ 31 and -3 ≤ r ≤ 4, i.e. a normalized binar |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fdup_z_i.xml`
</details>