## UADDV
_ARM A64 Instruction_

**Title**: UADDV -- A64 | **Class**: `sve` | **XML ID**: `uaddv_r_p_z`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Unsigned add reduction to scalar

**Description**:
Unsigned add horizontally across all lanes of a vector, and place the result in the
SIMD&FP scalar destination register.
Narrow elements are first zero-extended to 64 bits. Inactive elements in the source vector are treated as zero.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `UADDV  <Dd>, <Pg>, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  17 16 15  12   9   4  |
|--------------------------------------|
| 000 0010 0   size 0   000 0   1   001 Pg  Zn  Vd  |
```

#### Decode (A64.sve.sve_int_pred_red.sve_int_reduce_0.uaddv_r_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Vd);
```

#### Execute (A64.sve.sve_int_pred_red.sve_int_reduce_0.uaddv_r_p_z_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
integer sum = 0;

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        constant integer element = UInt(Elem[operand, e, esize]);
        sum = sum + element;

V[d, 64] = sum<63:0>;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Dd>` | `register (64-bit)` | `Vd` | Is the 64-bit name of the destination SIMD&FP register, encoded in the "Vd" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |

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
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `uaddv_r_p_z.xml`
</details>