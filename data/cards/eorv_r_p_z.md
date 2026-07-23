## EORV
_ARM A64 Instruction_

**Title**: EORV -- A64 | **Class**: `sve` | **XML ID**: `eorv_r_p_z`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Bitwise exclusive-OR reduction to scalar

**Description**:
Bitwise exclusive-OR horizontally across all lanes of a vector, and place the result in the
SIMD&FP scalar destination register.
 Inactive elements in the source vector are treated as zero.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `EORV  <V><d>, <Pg>, <Zn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  17  15  12   9   4  |
|-----------------------------------|
| 000 0010 0   size 0   110 01  001 Pg  Zn  Vd  |
```

#### Decode (A64.sve.sve_int_pred_red.sve_int_reduce_2.eorv_r_p_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Vd);
```

#### Execute (A64.sve.sve_int_pred_red.sve_int_reduce_2.eorv_r_p_z_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
bits(esize) result = Zeros(esize);

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        result = result EOR Elem[operand, e, esize];

V[d, esize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<V>` | `register (128-bit)` | `size` | Is a width specifier, |
| `<d>` | `unknown` | `Vd` | Is the number [0-31] of the destination SIMD&FP register, encoded in the "Vd" field. |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

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
- source: `eorv_r_p_z.xml`
</details>