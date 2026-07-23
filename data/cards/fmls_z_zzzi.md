## FMLS
_ARM A64 Instruction_

**Title**: FMLS (indexed) -- A64 | **Class**: `sve` | **XML ID**: `fmls_z_zzzi`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Floating-point fused multiply-subtract by indexed elements (Zda = Zda + -Zn * Zm[indexed])

**Description**:
Multiply all floating-point elements within each 128-bit
segment of the first source vector by the specified element in
the corresponding second source vector segment.  The products are then destructively subtracted without intermediate rounding from the corresponding
elements of the addend and destination vector.

The elements within the second source vector are specified using
an immediate index which selects the same element position within
each 128-bit vector segment.  The index range is from 0 to
one less than the number of elements per 128-bit segment.
This instruction is unpredicated.

### Variant: `Half-precision`
- **Assembly**: `FMLS  <Zda>.H, <Zn>.H, <Zm>.H[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  15  11 10  9   4  |
|-----------------------------------------|
| 011 0010 0   0   i3h 1   i3l Zm  0000 0   1   Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fma_by_indexed_elem.sve_fp_fma_by_indexed_elem.fmls_z_zzzi_h)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer index = UInt(i3h:i3l);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant boolean op1_neg = TRUE;
constant boolean op3_neg = FALSE;
```

#### Execute (A64.sve.sve_fp_fma_by_indexed_elem.sve_fp_fma_by_indexed_elem.fmls_z_zzzi_h)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer eltspersegment = 128 DIV esize;
constant bits(VL) op1 = Z[n, VL];
constant bits(VL) op2 = Z[m, VL];
bits(VL) result = Z[da, VL];

for e = 0 to elements-1
    constant integer segmentbase = e - (e MOD eltspersegment);
    constant integer s = segmentbase + index;
    constant bits(esize) elem2 = Elem[op2, s, esize];
    constant bits(esize) elem1 = (if op1_neg then FPNeg(Elem[op1, e, esize], FPCR)
                                  else Elem[op1, e, esize]);
    constant bits(esize) elem3 = (if op3_neg then FPNeg(Elem[result, e, esize], FPCR)
                                  else Elem[result, e, esize]);
    Elem[result, e, esize] = FPMulAdd(elem3, elem1, elem2, FPCR);

Z[da, VL] = result;
```

### Variant: `Single-precision`
- **Assembly**: `FMLS  <Zda>.S, <Zn>.S, <Zm>.S[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  11 10  9   4  |
|--------------------------------------|
| 011 0010 0   10  1   i2  Zm  0000 0   1   Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fma_by_indexed_elem.sve_fp_fma_by_indexed_elem.fmls_z_zzzi_s)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer index = UInt(i2);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant boolean op1_neg = TRUE;
constant boolean op3_neg = FALSE;
```

### Variant: `Double-precision`
- **Assembly**: `FMLS  <Zda>.D, <Zn>.D, <Zm>.D[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  11 10  9   4  |
|--------------------------------------|
| 011 0010 0   11  1   i1  Zm  0000 0   1   Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fma_by_indexed_elem.sve_fp_fma_by_indexed_elem.fmls_z_zzzi_d)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer index = UInt(i1);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant boolean op1_neg = TRUE;
constant boolean op3_neg = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "Half-precision" and "Single-precision" variants: is the name of the second source scalable vector register Z0-Z7, encoded in the "Zm" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "Double-precision" variant: is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<imm>` | `immediate` | `i3h:i3l` | For the "Half-precision" variant: is the immediate index, in the range 0 to 7, encoded in the "i3h:i3l" fields. |
| `<imm>` | `immediate` | `i2` | For the "Single-precision" variant: is the immediate index, in the range 0 to 3, encoded in the "i2" field. |
| `<imm>` | `immediate` | `i1` | For the "Double-precision" variant: is the immediate index, in the range 0 to 1, encoded in the "i1" field. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmls_z_zzzi.xml`
</details>