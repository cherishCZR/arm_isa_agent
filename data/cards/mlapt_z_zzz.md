## MLAPT
_ARM A64 Instruction_

**Title**: MLAPT -- A64 | **Class**: `sve2` | **XML ID**: `mlapt_z_zzz`

**Architecture**: `FEAT_SVE && FEAT_CPA` (FEAT_SVE && FEAT_CPA)

**Summary**: Multiply-add checked pointer vectors, writing addend [Zda = Zda + Zn * Zm]

**Description**:
Multiply with overflow check the elements of the first and second
source vectors and add pointer check to elements of the third source
(addend) vector.  Destructively place the results in the destination
and third source (addend) vector.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: SM Policy: `SM_0_only`

### Variant: `SVE2`
- **Assembly**: `MLAPT  <Zda>.D, <Zn>.D, <Zm>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  11   9   4  |
|--------------------------------|
| 010 0010 0   11  0   Zm  1101 00  Zn  Zda |
```

#### Decode (A64.sve.sve_ptr_muladd_unpred.sve_ptr_muladd_unpred.mlapt_z_zzz_)

```
if !IsFeatureImplemented(FEAT_SVE) || !IsFeatureImplemented(FEAT_CPA) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

#### Execute (A64.sve.sve_ptr_muladd_unpred.sve_ptr_muladd_unpred.mlapt_z_zzz_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 64;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer element1 = SInt(Elem[operand1, e, 64]);
    constant integer element2 = SInt(Elem[operand2, e, 64]);
    constant integer product = element1 * element2;
    constant boolean overflow = (product != SInt(product<63:0>));
    constant bits(64) addend = Elem[operand3, e, 64];
    Elem[result, e, 64] = PointerMultiplyAddCheck(addend + product, addend, overflow);

Z[da, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) && IsFeatureImplemented(FEAT_CPA)` |

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
- source: `mlapt_z_zzz.xml`
</details>