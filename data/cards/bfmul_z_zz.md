## BFMUL
_ARM A64 Instruction_

**Title**: BFMUL (vectors, unpredicated) -- A64 | **Class**: `sve2` | **XML ID**: `bfmul_z_zz`

**Architecture**: `FEAT_SVE_B16B16` (ARMv9.4)

**Summary**: BFloat16 multiply vectors (unpredicated)

**Description**:
Multiply all BFloat16 elements of the second source vector to
corresponding elements of the first source vector and place the results
in the corresponding elements of the destination vector.

This instruction follows SVE2 non-widening BFloat16 numerical behaviors.

This instruction is unpredicated.

ID_AA64ZFR0_EL1.B16B16 indicates whether this instruction is implemented.

### Variant: `SVE2`
- **Assembly**: `BFMUL  <Zd>.H, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12   9   4  |
|--------------------------------|
| 011 0010 1   00  0   Zm  000 010 Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_unpred.sve_fp_3op_u_zd.bfmul_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE_B16B16) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_fp_unpred.sve_fp_3op_u_zd.bfmul_z_zz_)

```
if IsFeatureImplemented(FEAT_SME2) then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 16;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(16) element1 = Elem[operand1, e, 16];
    constant bits(16) element2 = Elem[operand2, e, 16];
    Elem[result, e, 16] = BFMul(element1, element2, FPCR);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE_B16B16)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bfmul_z_zz.xml`
</details>