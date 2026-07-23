## FMOPA
_ARM A64 Instruction_

**Title**: FMOPA (non-widening) -- A64 | **Class**: `N/A` | **XML ID**: `fmopa_za_pp_zz`

**Architecture**: `FEAT_SME_F16F16` (ARMv9.4), `FEAT_SME` (PROFILE_A), `FEAT_SME_F64F64` (ARMv9.2)

**Summary**: Floating-point outer product and accumulate

**Description**:
The half-precision variant works with a
      16-bit element ZA tile.

The single-precision variant works with a 32-bit element ZA tile.

The double-precision variant works with a 64-bit element ZA tile.

This instruction generates an outer product of the first source
vector and the second source vector.
In case of the half-precision variant, the
      first source is SVLH×1 vector and the second source is
      1×SVLH vector.
In case of the single-precision variant, the first source is SVLS×1
vector and the second source is 1×SVLS vector.
In case of the double-precision variant, the first source is SVLD×1
vector and the second source is 1×SVLD vector.

Each source vector is independently predicated by a corresponding governing predicate.
When either source vector element is Inactive
the corresponding destination tile element remains unmodified.

The resulting outer product, SVLH×SVLH in case of half-precision variant,
SVLS×SVLS in case of single-precision variant or
SVLD×SVLD in case of double-precision variant, is then
destructively added to the destination tile.
This is equivalent to performing a single multiply-accumulate
to each of the destination tile elements.

This instruction follows SME ZA-targeting floating-point behaviors.

ID_AA64SMFR0_EL1.F64F64 indicates whether the double-precision variant is
implemented, and ID_AA64SMFR0_EL1.F16F16 indicates whether the half-precision variant is implemented.

**Attributes**: Predicated; SM Policy: `SM_1_only`

### Variant: `Half-precision`
- **Assembly**: `FMOPA  <ZAda>.H, <Pn>/M, <Pm>/M, <Zn>.H, <Zm>.H`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4  3   1  0 |
|--------------------------------------------|
| 1   00  0000 1   10  0   Zm  Pm  Pn  Zn  0   10  0   ZAda |
```

#### Decode (A64.sme.mortlach2_misc_prod.mortlach_f16f16_prod.fmopa_za_pp_zz_16)

```
if !IsFeatureImplemented(FEAT_SME_F16F16) then EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer a = UInt(Pn);
constant integer b = UInt(Pm);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(ZAda);
```

#### Execute (A64.sme.mortlach2_misc_prod.mortlach_f16f16_prod.fmopa_za_pp_zz_16)

```
CheckStreamingSVEAndZAEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer dim = VL DIV esize;
constant bits(PL) mask1 = P[a, PL];
constant bits(PL) mask2 = P[b, PL];
constant bits(VL) op1 = Z[n, VL];
constant bits(VL) op2 = Z[m, VL];
constant bits(dim*dim*esize) op3 = ZAtile[da, esize, dim*dim*esize];
bits(dim*dim*esize) result;

for row = 0 to dim-1
    for col = 0 to dim-1
        constant bits(esize) elem2 = Elem[op2, col, esize];
        constant bits(esize) elem3 = Elem[op3, row*dim+col, esize];

        if (ActivePredicateElement(mask1, row, esize) &&
              ActivePredicateElement(mask2, col, esize)) then
            constant bits(esize) elem1 = Elem[op1, row, esize];
            Elem[result, row*dim+col, esize] = FPMulAdd_ZA(elem3, elem1, elem2, FPCR);
        else
            Elem[result, row*dim+col, esize] = elem3;

ZAtile[da, esize, dim*dim*esize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_F16F16)` |

### Variant: `Single-precision`
- **Assembly**: `FMOPA  <ZAda>.S, <Pn>/M, <Pm>/M, <Zn>.S, <Zm>.S`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4  3   1  |
|-----------------------------------------|
| 1   00  0000 0   10  0   Zm  Pm  Pn  Zn  0   00  ZAda |
```

#### Decode (A64.sme.mortlach_32bit_fp_prod.mortlach_f32f32_prod.fmopa_za_pp_zz_32)

```
if !IsFeatureImplemented(FEAT_SME) then EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer a = UInt(Pn);
constant integer b = UInt(Pm);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(ZAda);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME)` |

### Variant: `Double-precision`
- **Assembly**: `FMOPA  <ZAda>.D, <Pn>/M, <Pm>/M, <Zn>.D, <Zm>.D`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  24 23  21 20  15  12   9   4  3  2  |
|--------------------------------------------|
| 1   0   0   0000 0   11  0   Zm  Pm  Pn  Zn  0   0   ZAda |
```

#### Decode (A64.sme.mortlach_64bit_prod.mortlach_f64f64_prod.fmopa_za_pp_zz_64)

```
if !IsFeatureImplemented(FEAT_SME_F64F64) then EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer a = UInt(Pn);
constant integer b = UInt(Pm);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(ZAda);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME_F64F64)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<ZAda>` | `register (128-bit)` | `ZAda` | For the "Half-precision" variant: is the name of the ZA tile ZA0-ZA1, encoded in the "ZAda" field. |
| `<ZAda>` | `register (128-bit)` | `ZAda` | For the "Single-precision" variant: is the name of the ZA tile ZA0-ZA3, encoded in the "ZAda" field. |
| `<ZAda>` | `register (128-bit)` | `ZAda` | For the "Double-precision" variant: is the name of the ZA tile ZA0-ZA7, encoded in the "ZAda" field. |
| `<Pn>` | `unknown` | `Pn` | Is the name of the first governing scalable predicate register P0-P7, encoded in the "Pn" field. |
| `<Pm>` | `unknown` | `Pm` | Is the name of the second governing scalable predicate register P0-P7, encoded in the "Pm" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fmopa_za_pp_zz.xml`
</details>