## BFMLS
_ARM A64 Instruction_

**Title**: BFMLS (indexed) -- A64 | **Class**: `sve2` | **XML ID**: `bfmls_z_zzzi`

**Architecture**: `FEAT_SVE_B16B16` (ARMv9.4)

**Summary**: BFloat16 fused multiply-subtract vectors by indexed elements

**Description**:
Multiply all BFloat16 elements within each 128-bit segment of the first
source vector by the specified element in the corresponding second
source vector segment. The products are then destructively subtracted
without intermediate rounding from the corresponding elements of the
addend and destination vector.

The elements within the second source vector are specified using an
immediate index which selects the same element position within each
128-bit vector segment. The index range is from 0 to 7.

This instruction follows SVE2 non-widening BFloat16 numerical behaviors.

This instruction is unpredicated.

ID_AA64ZFR0_EL1.B16B16 indicates whether this instruction is implemented.

### Variant: `SVE2`
- **Assembly**: `BFMLS  <Zda>.H, <Zn>.H, <Zm>.H[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  15  11 10  9   4  |
|-----------------------------------------|
| 011 0010 0   0   i3h 1   i3l Zm  0000 1   1   Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fma_by_indexed_elem.sve_fp_fma_by_indexed_elem.bfmls_z_zzzi_h)

```
if !IsFeatureImplemented(FEAT_SVE_B16B16) then EndOfDecode(Decode_UNDEF);
constant integer index = UInt(i3h:i3l);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant boolean op1_neg = TRUE;
constant boolean op3_neg = FALSE;
```

#### Execute (A64.sve.sve_fp_fma_by_indexed_elem.sve_fp_fma_by_indexed_elem.bfmls_z_zzzi_h)

```
if IsFeatureImplemented(FEAT_SME2) then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 16;
constant integer eltspersegment = 128 DIV 16;
constant bits(VL) op1 = Z[n, VL];
constant bits(VL) op2 = Z[m, VL];
bits(VL) result = Z[da, VL];

for e = 0 to elements-1
    constant integer segmentbase = e - (e MOD eltspersegment);
    constant integer s = segmentbase + index;
    constant bits(16) elem2 = Elem[op2, s, 16];
    constant bits(16) elem1 = if op1_neg then BFNeg(Elem[op1, e, 16]) else Elem[op1, e, 16];
    constant bits(16) elem3 = if op3_neg then BFNeg(Elem[result, e, 16]) else Elem[result, e, 16];
    Elem[result, e, 16] = BFMulAdd(elem3, elem1, elem2, FPCR);

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
- source: `bfmls_z_zzzi.xml`
</details>