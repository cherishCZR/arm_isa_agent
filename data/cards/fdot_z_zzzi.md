## FDOT
_ARM A64 Instruction_

**Title**: FDOT (2-way, indexed, FP16 to FP32) -- A64 | **Class**: `sve2` | **XML ID**: `fdot_z_zzzi`

**Architecture**: `FEAT_SME2 || FEAT_SVE2p1` (FEAT_SME2 || FEAT_SVE2p1)

**Summary**: Half-precision indexed dot product to single-precision

**Description**:
This instruction computes the fused sum-of-products
of a pair of half-precision values held in each 32-bit element
of the first source vector and a pair of half-precision values
in an indexed 32-bit element of the second source vector, without intermediate rounding,
and then destructively adds the single-precision sum-of-products to the
corresponding single-precision element of the destination vector.

The half-precision pairs within the second source vector are specified
using an immediate index which selects the same pair position within each 128-bit vector segment.
The index range is from 0 to 3.

This instruction is unpredicated.

### Variant: `SVE2`
- **Assembly**: `FDOT  <Zda>.S, <Zn>.H, <Zm>.H[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  15  13 12 11   9   4  |
|--------------------------------------------|
| 011 0010 0   0   0   1   i2  Zm  01  0   0   00  Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fma_w_by_indexed_elem.sve_fp_fdot_by_indexed_elem.fdot_z_zzzi_)

```
if !IsFeatureImplemented(FEAT_SME2) && !IsFeatureImplemented(FEAT_SVE2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant integer index = UInt(i2);
```

#### Execute (A64.sve.sve_fp_fma_w_by_indexed_elem.sve_fp_fdot_by_indexed_elem.fdot_z_zzzi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 32;
constant integer eltspersegment = 128 DIV 32;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer segmentbase = e - (e MOD eltspersegment);
    constant integer s = segmentbase + index;
    constant bits(16) elt1_a = Elem[operand1, 2 * e + 0, 16];
    constant bits(16) elt1_b = Elem[operand1, 2 * e + 1, 16];
    constant bits(16) elt2_a = Elem[operand2, 2 * s + 0, 16];
    constant bits(16) elt2_b = Elem[operand2, 2 * s + 1, 16];
    bits(32) sum = Elem[operand3, e, 32];

    sum = FPDotAdd(sum, elt1_a, elt1_b, elt2_a, elt2_b, FPCR);
    Elem[result, e, 32] = sum;

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
| `<imm>` | `immediate` | `i2` | Is the immediate index of a group of two 16-bit elements within each 128-bit vector segment, in the range 0 to 3, encoded in the "i2" field. |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fdot_z_zzzi.xml`
</details>