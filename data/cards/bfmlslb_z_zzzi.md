## BFMLSLB
_ARM A64 Instruction_

**Title**: BFMLSLB (indexed) -- A64 | **Class**: `sve2` | **XML ID**: `bfmlslb_z_zzzi`

**Architecture**: `FEAT_SME2 || FEAT_SVE2p1` (FEAT_SME2 || FEAT_SVE2p1)

**Summary**: BFloat16 multiply-subtract long from single-precision (bottom, indexed)

**Description**:
This BFloat16 multiply-subtract long instruction
widens the even-numbered BFloat16 elements in the first
source vector and the indexed element from the corresponding 128-bit segment
in the second source vector to single-precision format and
then destructively multiplies and subtracts these values
without intermediate rounding from the single-precision elements of the destination vector
that overlap with the corresponding BFloat16 elements in the
first source vector.
This instruction is unpredicated.

### Variant: `SVE2`
- **Assembly**: `BFMLSLB  <Zda>.S, <Zn>.H, <Zm>.H[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  15  13 12 11 10  9   4  |
|-----------------------------------------------|
| 011 0010 0   1   1   1   i3h Zm  01  1   0   i3l 0   Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fma_w_by_indexed_elem.sve_fp_fma_long_by_indexed_elem.bfmlslb_z_zzzi_)

```
if !IsFeatureImplemented(FEAT_SME2) && !IsFeatureImplemented(FEAT_SVE2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant integer index = UInt(i3h:i3l);
constant boolean op1_neg = TRUE;
```

#### Execute (A64.sve.sve_fp_fma_w_by_indexed_elem.sve_fp_fma_long_by_indexed_elem.bfmlslb_z_zzzi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 32;
constant integer eltspersegment = 128 DIV 32;
constant bits(VL) op1 = Z[n, VL];
constant bits(VL) op2 = Z[m, VL];
constant bits(VL) op3 = Z[da, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer segmentbase = e - (e MOD eltspersegment);
    constant integer s = 2 * segmentbase + index;
    constant bits(16) elem1 = (if op1_neg then BFNeg(Elem[op1, 2*e + 0, 16])
                               else Elem[op1, 2*e + 0, 16]);
    constant bits(16) elem2 = Elem[op2, s, 16];
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
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register Z0-Z7, encoded in the "Zm" field. |
| `<imm>` | `immediate` | `i3h:i3l` | Is the immediate index, in the range 0 to 7, encoded in the "i3h:i3l" fields. |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bfmlslb_z_zzzi.xml`
</details>