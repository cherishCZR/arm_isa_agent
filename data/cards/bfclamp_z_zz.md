## BFCLAMP
_ARM A64 Instruction_

**Title**: BFCLAMP -- A64 | **Class**: `sve2` | **XML ID**: `bfclamp_z_zz`

**Architecture**: `FEAT_SVE_B16B16` (ARMv9.4)

**Summary**: BFloat16 clamp to minimum/maximum number

**Description**:
Clamp each BFloat16 element in the destination vector
to between the BFloat16 minimum value in the corresponding element of the
first source vector and the BFloat16 maximum value in the corresponding element
of the second source vector and destructively place the clamped results
in the corresponding elements of the destination vector.

Regardless of the value of FPCR.AH, the behavior is as follows for each minimum number and maximum number operation:

This instruction follows SVE2 non-widening BFloat16 numerical behaviors.

This instruction is unpredicated.

ID_AA64ZFR0_EL1.B16B16 indicates whether this instruction is implemented.

### Variant: `SVE2`
- **Assembly**: `BFCLAMP  <Zd>.H, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15   9   4  |
|-----------------------------|
| 011 0010 0   00  1   Zm  001001 Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_clamp.sve_fp_clamp.bfclamp_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE_B16B16) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_fp_clamp.sve_fp_clamp.bfclamp_z_zz_)

```
if IsFeatureImplemented(FEAT_SME2) then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 16;
bits(VL) result;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[d, VL];

for e = 0 to elements-1
    constant bits(16) element1 = Elem[operand1, e, 16];
    constant bits(16) element2 = Elem[operand2, e, 16];
    constant bits(16) element3 = Elem[operand3, e, 16];
    constant bits(16) maxelement = BFMaxNum(element1, element3, FPCR);
    Elem[result, e, 16] = BFMinNum(maxelement, element2, FPCR);
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

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bfclamp_z_zz.xml`
</details>