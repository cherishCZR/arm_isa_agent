## BFMUL
_ARM A64 Instruction_

**Title**: BFMUL (indexed) -- A64 | **Class**: `sve2` | **XML ID**: `bfmul_z_zzi`

**Architecture**: `FEAT_SVE_B16B16` (ARMv9.4)

**Summary**: BFloat16 multiply vectors by indexed elements

**Description**:
Multiply all BFloat16 elements within each 128-bit segment of the first
source vector by the specified element in the corresponding second
source vector segment and place the results in the corresponding
elements of the destination vector.

The elements within the second source vector are specified using an
immediate index which selects the same element position within each
128-bit vector segment. The index range is from 0 to 7.

This instruction follows SVE2 non-widening BFloat16 numerical behaviors.

This instruction is unpredicated.

ID_AA64ZFR0_EL1.B16B16 indicates whether this instruction is implemented.

### Variant: `SVE2`
- **Assembly**: `BFMUL  <Zd>.H, <Zn>.H, <Zm>.H[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  15  11 10  9   4  |
|-----------------------------------------|
| 011 0010 0   0   i3h 1   i3l Zm  0010 1   0   Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_fmul_by_indexed_elem.sve_fp_fmul_by_indexed_elem.bfmul_z_zzi_h)

```
if !IsFeatureImplemented(FEAT_SVE_B16B16) then EndOfDecode(Decode_UNDEF);
constant integer index = UInt(i3h:i3l);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_fp_fmul_by_indexed_elem.sve_fp_fmul_by_indexed_elem.bfmul_z_zzi_h)

```
if IsFeatureImplemented(FEAT_SME2) then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 16;
constant integer eltspersegment = 128 DIV 16;
constant bits(VL) op1 = Z[n, VL];
constant bits(VL) op2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer segmentbase = e - (e MOD eltspersegment);
    constant integer s = segmentbase + index;
    constant bits(16) elem2 = Elem[op2, s, 16];
    constant bits(16) elem1 = Elem[op1, e, 16];
    Elem[result, e, 16] = BFMul(elem1, elem2, FPCR);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE_B16B16)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register Z0-Z7, encoded in the "Zm" field. |
| `<imm>` | `immediate` | `i3h:i3l` | Is the immediate index, in the range 0 to 7, encoded in the "i3h:i3l" fields. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `bfmul_z_zzi.xml`
</details>