## FMLSLB
_ARM A64 Instruction_

**Title**: FMLSLB (vectors) -- A64 | **Class**: `sve2` | **XML ID**: `fmlslb_z_zzz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Half-precision multiply-subtract long from single-precision (bottom)

**Description**:
This half-precision multiply-subtract long instruction
widens the even-numbered half-precision elements in the first
source vector and the corresponding elements
in the second source vector to single-precision format and
then destructively multiplies and subtracts these values
without intermediate rounding from the single-precision elements of the destination vector
that overlap with the corresponding half-precision elements in the
source vectors.
This instruction is unpredicated.

### Variant: `SVE2`
- **Assembly**: `FMLSLB  <Zda>.S, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  15  13 12  10  9   4  |
|-----------------------------------------|
| 011 0010 0   1   0   1   Zm  10  1   00  0   Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fma_w.sve_fp_fma_long.fmlslb_z_zzz_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant boolean op1_neg = TRUE;
```

#### Execute (A64.sve.sve_fp_fma_w.sve_fp_fma_long.fmlslb_z_zzz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) op1 = Z[n, VL];
constant bits(VL) op2 = Z[m, VL];
constant bits(VL) op3 = Z[da, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(esize DIV 2) elem1 = (if op1_neg then FPNeg(Elem[op1, 2*e + 0, esize DIV 2], FPCR)
                                        else Elem[op1, 2*e + 0, esize DIV 2]);
    constant bits(esize DIV 2) elem2 = Elem[op2, 2*e + 0, esize DIV 2];
    constant bits(esize) elem3 = Elem[op3, e, esize];
    Elem[result, e, esize] = FPMulAddH(elem3, elem1, elem2, FPCR);

Z[da, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
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
- source: `fmlslb_z_zzz.xml`
</details>