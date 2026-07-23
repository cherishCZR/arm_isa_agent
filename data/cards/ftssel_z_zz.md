## FTSSEL
_ARM A64 Instruction_

**Title**: FTSSEL -- A64 | **Class**: `sve` | **XML ID**: `ftssel_z_zz`

**Architecture**: `FEAT_SVE` (PROFILE_A)

**Summary**: Floating-point trigonometric select coefficient

**Description**:
The FTSSEL instruction selects either the element of the
first source vector or the value 1.0, based on bit<0> of the
corresponding element of the second source element, negates the
result if bit<1> of the corresponding element of the second
source element is set, and places the results in the destination
vector. This instruction is unpredicated.

FTSSEL can be combined with FTSMUL and FTMAD to
compute values for sin(k) and cos(k). For more
information, see FTSMUL. The use of the second operand is
consistent with it holding an integer corresponding to the
desired sine-wave quadrant.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: SM Policy: `SM_0_only`

### Variant: `SVE`
- **Assembly**: `FTSSEL  <Zd>.<T>, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  11 10  9   4  |
|-----------------------------------|
| 000 0010 0   size 1   Zm  1011 0   0   Zn  Zd  |
```

#### Decode (A64.sve.sve_int_unpred_misc.sve_int_bin_cons_misc_0_b.ftssel_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) then EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_int_unpred_misc.sve_int_bin_cons_misc_0_b.ftssel_z_zz_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(esize) element1 = Elem[operand1, e, esize];
    constant bits(esize) element2 = Elem[operand2, e, esize];
    Elem[result, e, esize] = FPTrigSSel(element1, element2);

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

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
- source: `ftssel_z_zz.xml`
</details>