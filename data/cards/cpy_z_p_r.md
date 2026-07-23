## CPY
_ARM A64 Instruction_

**Title**: CPY (scalar) -- A64 | **Class**: `sve` | **XML ID**: `cpy_z_p_r`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Copy general-purpose register to vector elements (predicated)

**Description**:
Copy the general-purpose scalar source register
to each active element in the destination vector. Inactive elements in the destination vector register remain unmodified.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `CPY  <Zd>.<T>, <Pg>/M, <R><n|SP>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  16 15  13 12   9   4  |
|-----------------------------------------|
| 000 0010 1   size 1   0   100 0   10  1   Pg  Rn  Zd  |
```

#### Decode (A64.sve.sve_perm_pred.sve_int_perm_cpy_r.cpy_z_p_r_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Rn);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_perm_pred.sve_int_perm_cpy_r.cpy_z_p_r_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
bits(VL) result = Z[d, VL];
if AnyActiveElement(mask, esize) then
    bits(64) operand1;
    if n == 31 then
        operand1 = SP[64];
    else
        operand1 = X[n, 64];

    for e = 0 to elements-1
        if ActivePredicateElement(mask, e, esize) then
            Elem[result, e, esize] = operand1<esize-1:0>;

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<R>` | `unknown` | `size` | Is a width specifier, |
| `<n\|SP>` | `unknown` | `Rn` | Is the number [0-30] of the general-purpose source register or the name SP (31), encoded in the "Rn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<R> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | W |
| 01 | W |
| 10 | W |
| 11 | X |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
        
        This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX can be predicated or unpredicated.
          
          
            A predicated MOVPRFX must use the same governing predicate register as this instruction.
          
          
            A predicated MOVPRFX must use the larger of the destination element size and first source element size in the preferred disassembly of this instructio
... (truncated)

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `cpy_z_p_r.xml`
</details>