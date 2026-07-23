## cmpeq_p_p_zi
_ARM A64 Instruction_

**Title**: CMP<cc> (immediate) -- A64 | **Class**: `sve` | **XML ID**: `cmpeq_p_p_zi`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Compare vector to immediate

**Description**:
Compare active integer elements in the
 source vector with an immediate, and
place the boolean results of the specified
comparison in the corresponding elements of the destination
predicate.  Inactive elements in the destination predicate register are set to zero. Sets the First (N), None (Z), !Last (C)
condition flags based on the predicate result,
and the V flag to zero.

**Attributes**: Predicated; DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `Equal`
- **Assembly**: `CMPEQ  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  3  |
|-----------------------------------------|
| 001 0010 1   size 0   imm5 1   0   0   Pg  Zn  0   Pd  |
```

#### Decode (A64.sve.sve_cmpsimm.sve_int_scmp_vi.cmpeq_p_p_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_EQ;
constant integer imm = SInt(imm5);
constant boolean unsigned = FALSE;
```

#### Execute (A64.sve.sve_cmpsimm.sve_int_scmp_vi.cmpeq_p_p_zi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand1 = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
bits(PL) result;
constant integer psize = esize DIV 8;

for e = 0 to elements-1
    constant integer element1 = Int(Elem[operand1, e, esize], unsigned);
    if ActivePredicateElement(mask, e, esize) then
        boolean cond;
        case cmp_op of
            when Cmp_EQ cond = element1 == imm;
            when Cmp_NE cond = element1 != imm;
            when Cmp_GE cond = element1 >= imm;
            when Cmp_LT cond = element1 <  imm;
            when Cmp_GT cond = element1 >  imm;
            when Cmp_LE cond = element1 <= imm;
        constant bit pbit = if cond then '1' else '0';
        Elem[result, e, psize] = ZeroExtend(pbit, psize);
    else
        Elem[result, e, psize] = ZeroExtend('0', psize);

PSTATE.<N,Z,C,V> = PredTest(mask, result, esize);
P[d, PL] = result;
```

### Variant: `Greater than`
- **Assembly**: `CMPGT  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  3  |
|-----------------------------------------|
| 001 0010 1   size 0   imm5 0   0   0   Pg  Zn  1   Pd  |
```

#### Decode (A64.sve.sve_cmpsimm.sve_int_scmp_vi.cmpgt_p_p_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_GT;
constant integer imm = SInt(imm5);
constant boolean unsigned = FALSE;
```

### Variant: `Greater than or equal`
- **Assembly**: `CMPGE  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  3  |
|-----------------------------------------|
| 001 0010 1   size 0   imm5 0   0   0   Pg  Zn  0   Pd  |
```

#### Decode (A64.sve.sve_cmpsimm.sve_int_scmp_vi.cmpge_p_p_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_GE;
constant integer imm = SInt(imm5);
constant boolean unsigned = FALSE;
```

### Variant: `Higher`
- **Assembly**: `CMPHI  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  13 12   9   4  3  |
|-----------------------------------|
| 001 0010 0   size 1   imm7 0   Pg  Zn  1   Pd  |
```

#### Decode (A64.sve.sve_cmpuimm.sve_int_ucmp_vi.cmphi_p_p_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_GT;
constant integer imm = UInt(imm7);
constant boolean unsigned = TRUE;
```

### Variant: `Higher or same`
- **Assembly**: `CMPHS  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  13 12   9   4  3  |
|-----------------------------------|
| 001 0010 0   size 1   imm7 0   Pg  Zn  0   Pd  |
```

#### Decode (A64.sve.sve_cmpuimm.sve_int_ucmp_vi.cmphs_p_p_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_GE;
constant integer imm = UInt(imm7);
constant boolean unsigned = TRUE;
```

### Variant: `Less than`
- **Assembly**: `CMPLT  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  3  |
|-----------------------------------------|
| 001 0010 1   size 0   imm5 0   0   1   Pg  Zn  0   Pd  |
```

#### Decode (A64.sve.sve_cmpsimm.sve_int_scmp_vi.cmplt_p_p_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_LT;
constant integer imm = SInt(imm5);
constant boolean unsigned = FALSE;
```

### Variant: `Less than or equal`
- **Assembly**: `CMPLE  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  3  |
|-----------------------------------------|
| 001 0010 1   size 0   imm5 0   0   1   Pg  Zn  1   Pd  |
```

#### Decode (A64.sve.sve_cmpsimm.sve_int_scmp_vi.cmple_p_p_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_LE;
constant integer imm = SInt(imm5);
constant boolean unsigned = FALSE;
```

### Variant: `Lower`
- **Assembly**: `CMPLO  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  13 12   9   4  3  |
|-----------------------------------|
| 001 0010 0   size 1   imm7 1   Pg  Zn  0   Pd  |
```

#### Decode (A64.sve.sve_cmpuimm.sve_int_ucmp_vi.cmplo_p_p_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_LT;
constant integer imm = UInt(imm7);
constant boolean unsigned = TRUE;
```

### Variant: `Lower or same`
- **Assembly**: `CMPLS  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  13 12   9   4  3  |
|-----------------------------------|
| 001 0010 0   size 1   imm7 1   Pg  Zn  1   Pd  |
```

#### Decode (A64.sve.sve_cmpuimm.sve_int_ucmp_vi.cmpls_p_p_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_LE;
constant integer imm = UInt(imm7);
constant boolean unsigned = TRUE;
```

### Variant: `Not equal`
- **Assembly**: `CMPNE  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  3  |
|-----------------------------------------|
| 001 0010 1   size 0   imm5 1   0   0   Pg  Zn  1   Pd  |
```

#### Decode (A64.sve.sve_cmpsimm.sve_int_scmp_vi.cmpne_p_p_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_NE;
constant integer imm = SInt(imm5);
constant boolean unsigned = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<imm>` | `immediate` | `imm5` | For the "Equal", "Greater than or equal", "Greater than", "Less than or equal", "Less than", and "Not equal" variants: is the signed immediate operand |
| `<imm>` | `immediate` | `imm7` | For the "Higher or same", "Higher", "Lower or same", and "Lower" variants: is the unsigned immediate operand, in the range 0 to 127, encoded in the "i |

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
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its operand registers when its governing predicate register contains the same value for each execution.
                
                
                  The values of the NZCV flags.
                
              
            
          
        
        If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the predicate register or NZCV condition flags written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `cmpeq_p_p_zi.xml`
</details>