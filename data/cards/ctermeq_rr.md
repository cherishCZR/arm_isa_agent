## ctermeq_rr
_ARM A64 Instruction_

**Title**: CTERMEQ, CTERMNE -- A64 | **Class**: `sve` | **XML ID**: `ctermeq_rr`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Compare and terminate loop

**Description**:
Detect termination conditions in serialized vector
loops.  Tests whether the comparison
between the scalar source operands holds true and if
not tests the state of the !Last condition flag
(C) which indicates whether the previous flag-setting
predicate instruction selected the last element of the
vector partition.

The Z and C condition flags are preserved by this
instruction.  The N and V condition flags are set as a
pair to generate one of the following conditions for a
subsequent conditional instruction:

The scalar source operands are 32-bit or 64-bit general-purpose
registers of the same size.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `Equal`
- **Assembly**: `CTERMEQ  <R><n>, <R><m>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  15  13  11   9   4  3  |
|-----------------------------------------|
| 001 0010 1   1   sz  1   Rm  00  10  00  Rn  0   0000 |
```

#### Decode (A64.sve.sve_cmpgpr.sve_int_cterm.ctermeq_rr_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32 << UInt(sz);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant CmpOp cmp_op = Cmp_EQ;
```

#### Execute (A64.sve.sve_cmpgpr.sve_int_cterm.ctermeq_rr_)

```
CheckSVEEnabled();
constant bits(esize) operand1 = X[n, esize];
constant bits(esize) operand2 = X[m, esize];
constant integer element1 = UInt(operand1);
constant integer element2 = UInt(operand2);
boolean term;

case cmp_op of
    when Cmp_EQ term = element1 == element2;
    when Cmp_NE term = element1 != element2;
if term then
    PSTATE.N = '1';
    PSTATE.V = '0';
else
    PSTATE.N = '0';
    PSTATE.V = (NOT PSTATE.C);
```

### Variant: `Not equal`
- **Assembly**: `CTERMNE  <R><n>, <R><m>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  15  13  11   9   4  3  |
|-----------------------------------------|
| 001 0010 1   1   sz  1   Rm  00  10  00  Rn  1   0000 |
```

#### Decode (A64.sve.sve_cmpgpr.sve_int_cterm.ctermne_rr_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32 << UInt(sz);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant CmpOp cmp_op = Cmp_NE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<R>` | `unknown` | `sz` | Is a width specifier, |
| `<n>` | `unknown` | `Rn` | Is the number [0-30] of the source general-purpose register or the name ZR (31), encoded in the "Rn" field. |
| `<m>` | `unknown` | `Rm` | Is the number [0-30] of the source general-purpose register or the name ZR (31), encoded in the "Rm" field. |

**<R> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | W |
| 1 | X |

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
- source: `ctermeq_rr.xml`
</details>