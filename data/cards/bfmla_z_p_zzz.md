## BFMLA
_ARM A64 Instruction_

**Title**: BFMLA (vectors) -- A64 | **Class**: `sve2` | **XML ID**: `bfmla_z_p_zzz`

**Architecture**: `FEAT_SVE_B16B16` (ARMv9.4)

**Summary**: BFloat16 fused multiply-add vectors

**Description**:
Multiply the corresponding active BFloat16 elements of the first and
second source vectors and add to elements of the third source (addend)
vector without intermediate rounding. Destructively place the results
in the destination and third source (addend) vector. Inactive elements
in the destination vector register remain unmodified.

This instruction follows SVE2 non-widening BFloat16 numerical behaviors.

ID_AA64ZFR0_EL1.B16B16 indicates whether this instruction is implemented.

**Attributes**: Predicated

### Variant: `SVE2`
- **Assembly**: `BFMLA  <Zda>.H, <Pg>/M, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  |
|--------------------------------------|
| 011 0010 1   00  1   Zm  0   0   0   Pg  Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fma.sve_fp_3op_p_zds_a.bfmla_z_p_zzz_)

```
if !IsFeatureImplemented(FEAT_SVE_B16B16) then EndOfDecode(Decode_UNDEF);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant boolean op1_neg = FALSE;
constant boolean op3_neg = FALSE;
```

#### Execute (A64.sve.sve_fp_fma.sve_fp_3op_p_zds_a.bfmla_z_p_zzz_)

```
if IsFeatureImplemented(FEAT_SME2) then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV 16;
constant bits(PL) mask = P[g, PL];
constant bits(VL) op1 = if AnyActiveElement(mask, 16) then Z[n, VL] else Zeros(VL);
constant bits(VL) op2 = if AnyActiveElement(mask, 16) then Z[m, VL] else Zeros(VL);
constant bits(VL) op3 = Z[da, VL];
bits(VL) result;

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, 16) then
        constant bits(16) elem1 = if op1_neg then BFNeg(Elem[op1, e, 16]) else Elem[op1, e, 16];
        constant bits(16) elem2 = Elem[op2, e, 16];
        constant bits(16) elem3 = if op3_neg then BFNeg(Elem[op3, e, 16]) else Elem[op3, e, 16];

        Elem[result, e, 16] = BFMulAdd(elem3, elem1, elem2, FPCR);
    else
        Elem[result, e, 16] = Elem[op3, e, 16];

Z[da, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE_B16B16)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX can be predicated or unpredicated.
          
          
            A predicated MOVPRFX must use the same governing predicate register as this instruction.
          
          
            A predicated MOVPRFX must use the larger of the destination element size and first source element size in the preferred disassembly of this instruction.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bfmla_z_p_zzz.xml`
</details>