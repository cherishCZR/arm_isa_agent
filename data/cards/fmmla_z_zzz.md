## FMMLA
_ARM A64 Instruction_

**Title**: FMMLA (non-widening) -- A64 | **Class**: `sve` | **XML ID**: `fmmla_z_zzz`

**Architecture**: `FEAT_F32MM` (PROFILE_A), `FEAT_F64MM` (PROFILE_A)

**Summary**: Floating-point matrix multiply-accumulate

**Description**:
This instruction supports
single-precision and double-precision data types in a 2x2
matrix contained in segments of 128 or 256 bits,
respectively. It multiplies the 2x2 matrix
in each segment of the first source vector by the 2x2 matrix in the
corresponding segment of the second source vector. The intermediate products
are rounded before they are summed, and the intermediate sum is rounded
before accumulation into the 2x2 matrix held in the corresponding segment
of the addend and destination vector. This is equivalent
to performing a 2-way dot product per destination element. This instruction
is unpredicated.

The single-precision variant is vector length agnostic.
The double-precision variant requires that the Effective SVE vector length is
at least 256 bits.

ID_AA64ZFR0_EL1.F32MM indicates whether the single-precision variant is implemented.

ID_AA64ZFR0_EL1.F64MM indicates whether the double-precision variant is implemented.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: SM Policy: `SM_0_only`

### Variant: `32-bit element`
- **Assembly**: `FMMLA  <Zda>.S, <Zn>.S, <Zm>.S`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15   9   4  |
|-----------------------------|
| 011 0010 0   10  1   Zm  111001 Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fmmla.sve_fp_fmmla.fmmla_z_zzz_s)

```
if !IsFeatureImplemented(FEAT_F32MM) then EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

#### Execute (A64.sve.sve_fp_fmmla.sve_fp_fmmla.fmmla_z_zzz_s)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
if VL < esize * 4 then EndOfDecode(Decode_UNDEF);
constant integer segments = VL DIV (4 * esize);
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result = Zeros(VL);
bits(4*esize) op1, op2;
bits(4*esize) res, addend;

for s = 0 to segments-1
    op1    = Elem[operand1, s, 4*esize];
    op2    = Elem[operand2, s, 4*esize];
    addend = Elem[operand3, s, 4*esize];
    res    = FPMatMulAdd(addend, op1, op2, esize, FPCR);
    Elem[result, s, 4*esize] = res;

Z[da, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_F32MM)` |

### Variant: `64-bit element`
- **Assembly**: `FMMLA  <Zda>.D, <Zn>.D, <Zm>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15   9   4  |
|-----------------------------|
| 011 0010 0   11  1   Zm  111001 Zn  Zda |
```

#### Decode (A64.sve.sve_fp_fmmla.sve_fp_fmmla.fmmla_z_zzz_d)

```
if !IsFeatureImplemented(FEAT_F64MM) then EndOfDecode(Decode_UNDEF);
constant integer esize = 64;
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_F64MM)` |

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
- source: `fmmla_z_zzz.xml`
</details>