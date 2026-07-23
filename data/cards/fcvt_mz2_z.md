## FCVT
_ARM A64 Instruction_

**Title**: FCVT (widening) -- A64 | **Class**: `mortlach2` | **XML ID**: `fcvt_mz2_z`

**Architecture**: `FEAT_SME_F16F16` (ARMv9.4)

**Summary**: Multi-vector convert from half-precision to single-precision (in-order)

**Description**:
This instruction converts each element of the
source vector from half-precision to single-precision floating-point, and places the  results
in the double-width destination elements of the destination vectors.

This instruction follows SME2 floating-point numerical behaviors
corresponding to instructions that place their results in one or more
SVE Z vectors.

This instruction is unpredicated.

ID_AA64SMFR0_EL1.F16F16 indicates whether this instruction is implemented.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `FCVT  { <Zd1>.S-<Zd2>.S }, <Zn>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   4   0 |
|--------------------------------------|
| 1   10  0000 1   10  1   000 00  111000 Zn  Zd  0   |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi2_wide_fp_cvrt.fcvt_mz2_z_)

```
if !IsFeatureImplemented(FEAT_SME_F16F16) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd:'0');
```

#### Execute (A64.sme.mortlach_multi_sve_4.mortlach_multi2_wide_fp_cvrt.fcvt_mz2_z_)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 16;
constant bits(VL) operand = Z[n, VL];
bits(2*VL) result;

for e = 0 to elements-1
    constant bits(16) element = Elem[operand, e, 16];
    constant bits(32) res = FPConvertSVE(element, FPCR, 32);
    Elem[result, e, 32] = res;

Z[d+0, VL] = result<VL-1:0>;
Z[d+1, VL] = result<2*VL-1:VL>;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_F16F16)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | Is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 2. |
| `<Zd2>` | `register (128-bit)` | `Zd` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zd" times 2 plus 1. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcvt_mz2_z.xml`
</details>