## FCPY
_ARM A64 Instruction_

**Title**: FCPY -- A64 | **Class**: `sve` | **XML ID**: `fcpy_z_p_i`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Copy 8-bit floating-point immediate to vector elements (predicated)

**Description**:
Copy a floating-point immediate into each active element
in the destination vector. Inactive elements in the destination vector register remain unmodified.

**Attributes**: Predicated

### Variant: `SVE`
- **Assembly**: `FCPY  <Zd>.<T>, <Pg>/M, #<const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  19  15  12   4  |
|-----------------------------|
| 000 0010 1   size 01  Pg  110 imm8 Zd  |
```

#### Decode (A64.sve.sve_wideimm_pred.sve_int_dup_fpimm_pred.fcpy_z_p_i_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer d = UInt(Zd);
constant bits(esize) imm = VFPExpandImm(imm8, esize);
```

#### Execute (A64.sve.sve_wideimm_pred.sve_int_dup_fpimm_pred.fcpy_z_p_i_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
bits(VL) result = Z[d, VL];

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        Elem[result, e, esize] = imm;

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register, encoded in the "Pg" field. |
| `<const>` | `unknown` | `imm8` | Is a floating-point immediate value expressible as ±n÷16×2^r, where n and r are integers such that 16 ≤ n ≤ 31 and -3 ≤ r ≤ 4, i.e. a normalized binar |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX can be predicated or unpredicated.
          
          
            A predicated MOVPRFX must use the same governing predicate register as this instruction.
          
          
            A predicated MOVPRFX must use the larger of the destination element size and first source element size in the preferred disassembly of this instruction.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcpy_z_p_i.xml`
</details>