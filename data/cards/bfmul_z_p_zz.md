## BFMUL
_ARM A64 Instruction_

**Title**: BFMUL (vectors, predicated) -- A64 | **Class**: `sve2` | **XML ID**: `bfmul_z_p_zz`

**Architecture**: `FEAT_SVE_B16B16` (ARMv9.4)

**Summary**: BFloat16 multiply vectors (predicated)

**Description**:
Multiply active BFloat16 elements of the second source vector to
corresponding elements of the first source vector and destructively
place the results in the corresponding elements of the first source
vector. Inactive elements in the destination vector register remain
unmodified.

This instruction follows SVE2 non-widening BFloat16 numerical behaviors.

ID_AA64ZFR0_EL1.B16B16 indicates whether this instruction is implemented.

**Attributes**: Predicated

### Variant: `SVE2`
- **Assembly**: `BFMUL  <Zdn>.H, <Pg>/M, <Zdn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  12   9   4  |
|-----------------------------------|
| 011 0010 1   00  0   0   0010 100 Pg  Zm  Zdn |
```

#### Decode (A64.sve.sve_fp_pred.sve_fp_2op_p_zds.bfmul_z_p_zz_)

```
if !IsFeatureImplemented(FEAT_SVE_B16B16) then EndOfDecode(Decode_UNDEF);

constant integer g = UInt(Pg);
constant integer dn = UInt(Zdn);
constant integer m = UInt(Zm);
```

#### Execute (A64.sve.sve_fp_pred.sve_fp_2op_p_zds.bfmul_z_p_zz_)

```
if IsFeatureImplemented(FEAT_SME2) then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV 16;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand1 = Z[dn, VL];
constant bits(VL) operand2 = if AnyActiveElement(mask, 16) then Z[m, VL] else Zeros(VL);
bits(VL) result;

for e = 0 to elements-1
    constant bits(16) element1 = Elem[operand1, e, 16];
    if ActivePredicateElement(mask, e, 16) then
        constant bits(16) element2 = Elem[operand2, e, 16];
        Elem[result, e, 16] = BFMul(element1, element2, FPCR);
    else
        Elem[result, e, 16] = element1;

Z[dn, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE_B16B16)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the first source and destination scalable vector register, encoded in the "Zdn" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
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
- source: `bfmul_z_p_zz.xml`
</details>