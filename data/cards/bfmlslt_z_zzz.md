## BFMLSLT
_ARM A64 Instruction_

**Title**: BFMLSLT (vectors) -- A64 | **Class**: `sve2` | **XML ID**: `bfmlslt_z_zzz`

**Architecture**: `FEAT_SME2 || FEAT_SVE2p1` (FEAT_SME2 || FEAT_SVE2p1)

**Summary**: BFloat16 multiply-subtract long from single-precision (top)

**Description**:
This BFloat16 multiply-subtract long instruction
widens the odd-numbered BFloat16 elements in the first
source vector and the corresponding elements
in the second source vector to single-precision format and
then destructively multiplies and subtracts these values
without intermediate rounding from the single-precision elements of the destination vector
that overlap with the corresponding BFloat16 elements in the
source vectors.
This instruction is unpredicated.

### Variant: `SVE2`
- **Assembly**: `BFMLSLT  <Zda>.S, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  15  13 12  10  9   4  |
|-----------------------------------------|
| 011 0010 0   1   1   1   Zm  10  1   00  1   Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fma_w.sve_fp_fma_long.bfmlslt_z_zzz_)

```
if !IsFeatureImplemented(FEAT_SME2) && !IsFeatureImplemented(FEAT_SVE2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant boolean op1_neg = TRUE;
```

#### Execute (A64.sve.sve_fp_fma_w.sve_fp_fma_long.bfmlslt_z_zzz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 32;
constant bits(VL) op1 = Z[n, VL];
constant bits(VL) op2 = Z[m, VL];
constant bits(VL) op3 = Z[da, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(16) elem1 = (if op1_neg then BFNeg(Elem[op1, 2*e + 1, 16])
                               else Elem[op1, 2*e + 1, 16]);
    constant bits(16) elem2 = Elem[op2, 2*e + 1, 16];
    constant bits(32) elem3 = Elem[op3, e, 32];
    Elem[result, e, 32] = BFMulAddH(elem3, elem1, elem2, FPCR);

Z[da, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) \|\| IsFeatureImplemented(FEAT_SVE2p1)` |

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
- source: `bfmlslt_z_zzz.xml`
</details>