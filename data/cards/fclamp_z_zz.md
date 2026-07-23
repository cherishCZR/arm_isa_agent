## FCLAMP
_ARM A64 Instruction_

**Title**: FCLAMP -- A64 | **Class**: `sve2` | **XML ID**: `fclamp_z_zz`

**Architecture**: `FEAT_SME2 || FEAT_SVE2p1` (FEAT_SME2 || FEAT_SVE2p1)

**Summary**: Floating-point clamp to minimum/maximum number

**Description**:
Clamp each floating-point element in the destination vector
to between the floating-point minimum value in the corresponding element of the
first source vector and the floating-point maximum value in the corresponding element
of the second source vector and destructively place the clamped results
in the corresponding elements of the destination vector.

Regardless of the value of FPCR.AH, the behavior is as follows for each minimum number and maximum number operation:

This instruction is unpredicated.

### Variant: `SVE2`
- **Assembly**: `FCLAMP  <Zd>.<T>, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15   9   4  |
|-----------------------------|
| 011 0010 0   ?   1   Zm  001001 Zn  Zd  |
```

#### Decode (A64.sve.sve_fp_clamp.sve_fp_clamp.fclamp_z_zz_)

```
if !IsFeatureImplemented(FEAT_SME2) && !IsFeatureImplemented(FEAT_SVE2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_fp_clamp.sve_fp_clamp.fclamp_z_zz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
bits(VL) result;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[d, VL];

for e = 0 to elements-1
    constant bits(esize) element1 = Elem[operand1, e, esize];
    constant bits(esize) element2 = Elem[operand2, e, esize];
    constant bits(esize) element3 = Elem[operand3, e, esize];
    constant bits(esize) maxelement = FPMaxNum(element1, element3, FPCR);
    Elem[result, e, esize] = FPMinNum(maxelement, element2, FPCR);
Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) \|\| IsFeatureImplemented(FEAT_SVE2p1)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
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
- source: `fclamp_z_zz.xml`
</details>