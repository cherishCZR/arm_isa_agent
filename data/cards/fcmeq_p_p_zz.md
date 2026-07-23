## fcmeq_p_p_zz
_ARM A64 Instruction_

**Title**: FCM<cc> (vectors) -- A64 | **Class**: `sve` | **XML ID**: `fcmeq_p_p_zz`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Floating-point compare vectors

**Description**:
Compare active floating-point elements in the
first source vector with corresponding elements in the second source vector, and
place the boolean results of the specified
comparison in the corresponding elements of the destination
predicate.  Inactive elements in the destination predicate register are set to zero. Does not set the condition flags.

**Attributes**: Predicated

### Variant: `Equal`
- **Assembly**: `FCMEQ  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  3  |
|-----------------------------------------|
| 011 0010 1   size 0   Zm  0   1   1   Pg  Zn  0   Pd  |
```

#### Decode (A64.sve.sve_fp_cmpvev.sve_fp_3op_p_pd.fcmeq_p_p_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_EQ;
```

#### Execute (A64.sve.sve_fp_cmpvev.sve_fp_3op_p_pd.fcmeq_p_p_zz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand1 = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
constant bits(VL) operand2 = if AnyActiveElement(mask, esize) then Z[m, VL] else Zeros(VL);
bits(PL) result;
constant integer psize = esize DIV 8;

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        constant bits(esize) element1 = Elem[operand1, e, esize];
        constant bits(esize) element2 = Elem[operand2, e, esize];
        boolean res;
        case cmp_op of
            when Cmp_EQ res = FPCompareEQ(element1, element2, FPCR);
            when Cmp_GE res = FPCompareGE(element1, element2, FPCR);
            when Cmp_GT res = FPCompareGT(element1, element2, FPCR);
            when Cmp_UN res = FPCompareUN(element1, element2, FPCR);
            when Cmp_NE res = FPCompareNE(element1, element2, FPCR);
            when Cmp_LT res = FPCompareGT(element2, element1, FPCR);
            when Cmp_LE res = FPCompareGE(element2, element1, FPCR);
        constant bit pbit = if res then '1' else '0';
        Elem[result, e, psize] = ZeroExtend(pbit, psize);
    else
        Elem[result, e, psize] = ZeroExtend('0', psize);

P[d, PL] = result;
```

### Variant: `Greater than`
- **Assembly**: `FCMGT  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  3  |
|-----------------------------------------|
| 011 0010 1   size 0   Zm  0   1   0   Pg  Zn  1   Pd  |
```

#### Decode (A64.sve.sve_fp_cmpvev.sve_fp_3op_p_pd.fcmgt_p_p_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_GT;
```

### Variant: `Greater than or equal`
- **Assembly**: `FCMGE  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  3  |
|-----------------------------------------|
| 011 0010 1   size 0   Zm  0   1   0   Pg  Zn  0   Pd  |
```

#### Decode (A64.sve.sve_fp_cmpvev.sve_fp_3op_p_pd.fcmge_p_p_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_GE;
```

### Variant: `Not equal`
- **Assembly**: `FCMNE  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  3  |
|-----------------------------------------|
| 011 0010 1   size 0   Zm  0   1   1   Pg  Zn  1   Pd  |
```

#### Decode (A64.sve.sve_fp_cmpvev.sve_fp_3op_p_pd.fcmne_p_p_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_NE;
```

### Variant: `Unordered`
- **Assembly**: `FCMUO  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14 13 12   9   4  3  |
|-----------------------------------------|
| 011 0010 1   size 0   Zm  1   1   0   Pg  Zn  0   Pd  |
```

#### Decode (A64.sve.sve_fp_cmpvev.sve_fp_3op_p_pd.fcmuo_p_p_zz_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Pd);
constant CmpOp cmp_op = Cmp_UN;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

### Encoding Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

### Operational Notes

If FEAT_SME is implemented and the PE is in Streaming SVE mode, then any subsequent instruction which is dependent on the predicate register written by this instruction might be significantly delayed.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `fcmeq_p_p_zz.xml`
</details>