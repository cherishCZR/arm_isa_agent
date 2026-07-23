## FMAD
_ARM A64 Instruction_

**Title**: FMAD -- A64 | **Class**: `sve` | **XML ID**: `fmad_z_p_zzz`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Floating-point fused multiply-add vectors (predicated), writing multiplicand [Zdn = Za + Zdn * Zm]

**Description**:
Multiply the corresponding active floating-point elements of the first and second source
vectors and add to elements of the third (addend)
vector without intermediate rounding.
Destructively place the  results in the destination
and first source (multiplicand) vector.  Inactive elements in the destination vector register remain unmodified.

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `FMAD  <Zdn>.<T>, <Pg>/M, <Zm>.<T>, <Za>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  |
|--------------------------------------|
| 011 0010 1   size 1   Za  1   0   0   Pg  Zm  Zdn |
```

#### Decode (A64.sve.sve_fp_fma.sve_fp_3op_p_zds_b.fmad_z_p_zzz_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer dn = UInt(Zdn);
constant integer m = UInt(Zm);
constant integer a = UInt(Za);
constant boolean op1_neg = FALSE;
constant boolean op3_neg = FALSE;
```

#### Execute (A64.sve.sve_fp_fma.sve_fp_3op_p_zds_b.fmad_z_p_zzz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) op1 = Z[dn, VL];
constant bits(VL) op2 = if AnyActiveElement(mask, esize) then Z[m, VL] else Zeros(VL);
constant bits(VL) op3 = if AnyActiveElement(mask, esize) then Z[a, VL] else Zeros(VL);
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
        Elem[result, e, esize] = Elem[op1, e, esize];

Z[dn, VL] = result;
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
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the first source and destination scalable vector register, encoded in the "Zdn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<Za>` | `register (128-bit)` | `Za` | Is the name of the third source scalable vector register, encoded in the "Za" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
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
- source: `fmad_z_p_zzz.xml`
</details>