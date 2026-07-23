## zip1_p_pp
_ARM A64 Instruction_

**Title**: ZIP1, ZIP2 (predicates) -- A64 | **Class**: `sve` | **XML ID**: `zip1_p_pp`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Interleave elements from two half predicates

**Description**:
Interleave alternating  elements from the
lowest or highest halves of the first and second
source predicates and place in elements of the
destination predicate.  This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `High halves`
- **Assembly**: `ZIP2  <Pd>.<T>, <Pn>.<T>, <Pm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  12  10  9  8   4  3  |
|--------------------------------------------|
| 000 0010 1   size 1   0   Pm  010 00  1   0   Pn  0   Pd  |
```

#### Decode (A64.sve.sve_perm_predicates.sve_int_perm_bin_perm_pp.zip2_p_pp_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Pn);
constant integer m = UInt(Pm);
constant integer d = UInt(Pd);
constant integer part = 1;
```

#### Execute (A64.sve.sve_perm_predicates.sve_int_perm_bin_perm_pp.zip2_p_pp_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer pairs = VL DIV (esize * 2);
constant bits(PL) operand1 = P[n, PL];
constant bits(PL) operand2 = P[m, PL];
bits(PL) result;

constant integer base = part * pairs;
for p = 0 to pairs-1
    Elem[result, 2*p+0, esize DIV 8] = Elem[operand1, base+p, esize DIV 8];
    Elem[result, 2*p+1, esize DIV 8] = Elem[operand2, base+p, esize DIV 8];

P[d, PL] = result;
```

### Variant: `Low halves`
- **Assembly**: `ZIP1  <Pd>.<T>, <Pn>.<T>, <Pm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  12  10  9  8   4  3  |
|--------------------------------------------|
| 000 0010 1   size 1   0   Pm  010 00  0   0   Pn  0   Pd  |
```

#### Decode (A64.sve.sve_perm_predicates.sve_int_perm_bin_perm_pp.zip1_p_pp_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Pn);
constant integer m = UInt(Pm);
constant integer d = UInt(Pd);
constant integer part = 0;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pn>` | `unknown` | `Pn` | Is the name of the first source scalable predicate register, encoded in the "Pn" field. |
| `<Pm>` | `unknown` | `Pm` | Is the name of the second source scalable predicate register, encoded in the "Pm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

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
- source: `zip1_p_pp.xml`
</details>