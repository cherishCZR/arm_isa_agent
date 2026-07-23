## FTMAD
_ARM A64 Instruction_

**Title**: FTMAD -- A64 | **Class**: `sve` | **XML ID**: `ftmad_z_zzi`

**Architecture**: `FEAT_SVE` (PROFILE_A)

**Summary**: Floating-point trigonometric multiply-add coefficient

**Description**:
The FTMAD instruction multiplies each element of the first
source vector by the absolute value of the corresponding
element of the second source vector and performs a fused
addition of each product with a value obtained from a table of
hard-wired coefficients, and places the results destructively in
the first source vector. This instruction is unpredicated.

The coefficients are selected by a combination of the sign bit
in the second source element and an immediate index in the
range 0 to 7.

FTMAD can be combined with FTSMUL and FTSSEL to
compute values for sin(x) and cos(x). For more
information, see FTSMUL. The coefficients are intended to
provide accurate results for FTSMUL inputs in the range
-π/4 < x ≤ π/4.

For double-precision operations, the coefficients are:

For single-precision operations, the coefficients are:

For half-precision operations, the coefficients are:

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: SM Policy: `SM_0_only`

### Variant: `SVE`
- **Assembly**: `FTMAD  <Zdn>.<T>, <Zdn>.<T>, <Zm>.<T>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  12   9   4  |
|-----------------------------------|
| 011 0010 1   size 0   10  imm3 100 000 Zm  Zdn |
```

#### Decode (A64.sve.sve_fp_pred.sve_fp_ftmad.ftmad_z_zzi_)

```
if !IsFeatureImplemented(FEAT_SVE) then EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer dn = UInt(Zdn);
constant integer m = UInt(Zm);
constant integer imm = UInt(imm3);
```

#### Execute (A64.sve.sve_fp_pred.sve_fp_ftmad.ftmad_z_zzi_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[dn, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(esize) element1 = Elem[operand1, e, esize];
    constant bits(esize) element2 = Elem[operand2, e, esize];
    Elem[result, e, esize] = FPTrigMAdd(imm, element1, element2, FPCR);

Z[dn, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the first source and destination scalable vector register, encoded in the "Zdn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<imm>` | `immediate` | `imm3` | Is the unsigned immediate operand, in the range 0 to 7, encoded in the "imm3" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ftmad_z_zzi.xml`
</details>