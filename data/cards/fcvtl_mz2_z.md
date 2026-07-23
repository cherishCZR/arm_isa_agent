## FCVTL
_ARM A64 Instruction_

**Title**: FCVTL -- A64 | **Class**: `mortlach2` | **XML ID**: `fcvtl_mz2_z`

**Architecture**: `FEAT_SME_F16F16` (ARMv9.4)

**Summary**: Multi-vector convert from half-precision to deinterleaved single-precision

**Description**:
This instruction converts each element of the
source vector from half-precision to single-precision floating-point, and places the two-way deinterleaved results
in the double-width destination elements of the destination vectors.

This instruction follows SME2 floating-point numerical behaviors
corresponding to instructions that place their results in one or more
SVE Z vectors.

This instruction is unpredicated.

ID_AA64SMFR0_EL1.F16F16 indicates whether this instruction is implemented.

**Attributes**: SM Policy: `SM_1_only`

### Variant: `SME2`
- **Assembly**: `FCVTL  { <Zd1>.S-<Zd2>.S }, <Zn>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   4   0 |
|--------------------------------------|
| 1   10  0000 1   10  1   000 00  111000 Zn  Zd  1   |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi2_wide_fp_cvrt.fcvtl_mz2_z_)

```
if !IsFeatureImplemented(FEAT_SME_F16F16) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd:'0');
```

#### Execute (A64.sme.mortlach_multi_sve_4.mortlach_multi2_wide_fp_cvrt.fcvtl_mz2_z_)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer pairs = VL DIV 32;
constant bits(VL) operand = Z[n, VL];
bits(VL) result0;
bits(VL) result1;

for p = 0 to pairs-1
    constant bits(16) element1 = Elem[operand, 2*p+0, 16];
    constant bits(16) element2 = Elem[operand, 2*p+1, 16];
    constant bits(32) res1 = FPConvertSVE(element1, FPCR, 32);
    constant bits(32) res2 = FPConvertSVE(element2, FPCR, 32);
    Elem[result0, p, 32] = res1;
    Elem[result1, p, 32] = res2;

Z[d+0, VL] = result0;
Z[d+1, VL] = result1;
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
- source: `fcvtl_mz2_z.xml`
</details>