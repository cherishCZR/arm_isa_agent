## FEXPA
_ARM A64 Instruction_

**Title**: FEXPA -- A64 | **Class**: `sve` | **XML ID**: `fexpa_z_z`

**Architecture**: `FEAT_SVE || FEAT_SSVE_FEXPA` (FEAT_SVE || FEAT_SSVE_FEXPA)

**Summary**: Floating-point exponential accelerator

**Description**:
The FEXPA instruction computes an exponentiation acceleration
operation on each floating-point element in the source vector, where
the result sign is zero, the result exponent field is copied from a
set of significant bits of the input fraction, and the result fraction
is inserted from a lookup table indexed by the least-significant
input fraction bits, and returns each result in the corresponding
element of the destination vector.

This instruction is fully defined by its bit-manipulation
semantics, does not generate floating-point exceptions,
and does not guarantee NaN propagation.

For double-precision variants, the result element exponent
is copied from the source element bits<16:6>, and the
result fraction is set based on the source element to the
rounded value of 252 × (2bits<5:0>/64 - 1).

For single-precision variants, the result element exponent
is copied from the source element bits<13:6>, and the
result fraction is set based on the source element to the
rounded value of 223 × (2bits<5:0>/64 - 1).

For half-precision variants, the result element exponent
is copied from the source element bits<9:5>, and the
result fraction is set based on the source element to the
rounded value of 210 × (2bits<4:0>/32 - 1).

This instruction is unpredicated.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is
implemented and enabled, or FEAT_SME2p2 is implemented.

**Attributes**: SM Policy: `SM_0_or_SME2p2`

### Variant: `SVE`
- **Assembly**: `FEXPA  <Zd>.<T>, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  11   9   4  |
|--------------------------------|
| 000 0010 0   size 1   00000 1011 10  Zn  Zd  |
```

#### Decode (A64.sve.sve_int_unpred_misc.sve_int_bin_cons_misc_0_c.fexpa_z_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SSVE_FEXPA) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_int_unpred_misc.sve_int_bin_cons_misc_0_c.fexpa_z_z_)

```
if IsFeatureImplemented(FEAT_SSVE_FEXPA) then
    CheckSVEEnabled();
else
    CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand = Z[n, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(esize) element = Elem[operand, e, esize];
    Elem[result, e, esize] = FPExpA(element);

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SSVE_FEXPA)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

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
- source: `fexpa_z_z.xml`
</details>