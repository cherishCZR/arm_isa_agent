## FMLA
_ARM A64 Instruction_

**Title**: FMLA (vectors) -- A64 | **Class**: `sve` | **XML ID**: `fmla_z_p_zzz`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Floating-point fused multiply-add vectors (predicated), writing addend [Zda = Zda + Zn * Zm]

**Description**:
Multiply the corresponding active floating-point elements of the first and second source
vectors and add to elements of the third source
(addend) vector without intermediate
rounding.  Destructively place the  results in
the destination and third source (addend) vector.  Inactive elements in the destination vector register remain unmodified.

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `FMLA  <Zda>.<T>, <Pg>/M, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  |
|--------------------------------------|
| 011 0010 1   ?   1   Zm  0   0   0   Pg  Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fma.sve_fp_3op_p_zds_a.fmla_z_p_zzz_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant boolean op1_neg = FALSE;
constant boolean op3_neg = FALSE;
```

#### Execute (A64.sve.sve_fp_fma.sve_fp_3op_p_zds_a.fmla_z_p_zzz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) op1 = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
constant bits(VL) op2 = if AnyActiveElement(mask, esize) then Z[m, VL] else Zeros(VL);
constant bits(VL) op3 = Z[da, VL];
bits(VL) result;

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        constant bits(esize) elem1 = (if op1_neg then FPNeg(Elem[op1, e, esize], FPCR)
                                      else Elem[op1, e, esize]);
        constant bits(esize) elem2 = Elem[op2, e, esize];
        constant bits(esize) elem3 = (if op3_neg then FPNeg(Elem[op3, e, esize], FPCR)
                                      else Elem[op3, e, esize]);

        Elem[result, e, esize] = FPMulAdd(elem3, elem1, elem2, FPCR);
    else
        Elem[result, e, esize] = Elem[op3, e, esize];

Z[da, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 01 | H |
| 10 | S |
| 11 | D |

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
- source: `fmla_z_p_zzz.xml`
</details>