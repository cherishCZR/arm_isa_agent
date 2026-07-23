## REV
_ARM A64 Instruction_

**Title**: REV (predicate) -- A64 | **Class**: `sve` | **XML ID**: `rev_p_p`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Reverse all elements in a predicate

**Description**:
Reverse the order of all elements in the source
predicate and place in the destination predicate.
This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `REV  <Pd>.<T>, <Pn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12   8   4  3  |
|-----------------------------------|
| 000 0010 1   size 1   10100 010 0000 Pn  0   Pd  |
```

#### Decode (A64.sve.sve_perm_predicates.sve_int_perm_reverse_p.rev_p_p_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Pn);
constant integer d = UInt(Pd);
```

#### Execute (A64.sve.sve_perm_predicates.sve_int_perm_reverse_p.rev_p_p_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant bits(PL) operand = P[n, PL];
constant bits(PL) result = Reverse(operand, esize DIV 8);
P[d, PL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pn>` | `unknown` | `Pn` | Is the name of the source scalable predicate register, encoded in the "Pn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `rev_p_p.xml`
</details>