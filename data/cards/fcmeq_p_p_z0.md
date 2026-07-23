## fcmeq_p_p_z0
_ARM A64 Instruction_

**Title**: FCM<cc> (zero) -- A64 | **Class**: `sve` | **XML ID**: `fcmeq_p_p_z0`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Floating-point compare vector with zero

**Description**:
Compare active floating-point elements in the
 source vector with zero, and
place the boolean results of the specified
comparison in the corresponding elements of the destination
predicate.  Inactive elements in the destination predicate register are set to zero. Does not set the condition flags.

**Attributes**: Predicated

### Variant: `Equal`
- **Assembly**: `FCMEQ  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #0.0`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18 17 16 15  12   9   4  3  |
|-----------------------------------------|
| 011 0010 1   size 010 0   1   0   001 Pg  Zn  0   Pd  |
```

#### Decode (A64.sve.sve_fp_cmpzero.sve_fp_2op_p_pd.fcmeq_p_p_z0_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp op = Cmp_EQ;
```

#### Execute (A64.sve.sve_fp_cmpzero.sve_fp_2op_p_pd.fcmeq_p_p_z0_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
bits(PL) result;
constant integer psize = esize DIV 8;

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        constant bits(esize) element = Elem[operand, e, esize];
        boolean res;
        case op of
            when Cmp_EQ res = FPCompareEQ(element, 0<esize-1:0>, FPCR);
            when Cmp_GE res = FPCompareGE(element, 0<esize-1:0>, FPCR);
            when Cmp_GT res = FPCompareGT(element, 0<esize-1:0>, FPCR);
            when Cmp_NE res = FPCompareNE(element, 0<esize-1:0>, FPCR);
            when Cmp_LT res = FPCompareGT(0<esize-1:0>, element, FPCR);
            when Cmp_LE res = FPCompareGE(0<esize-1:0>, element, FPCR);
        constant bit pbit = if res then '1' else '0';
        Elem[result, e, psize] = ZeroExtend(pbit, psize);
    else
        Elem[result, e, psize] = ZeroExtend('0', psize);

P[d, PL] = result;
```

### Variant: `Greater than`
- **Assembly**: `FCMGT  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #0.0`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18 17 16 15  12   9   4  3  |
|-----------------------------------------|
| 011 0010 1   size 010 0   0   0   001 Pg  Zn  1   Pd  |
```

#### Decode (A64.sve.sve_fp_cmpzero.sve_fp_2op_p_pd.fcmgt_p_p_z0_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp op = Cmp_GT;
```

### Variant: `Greater than or equal`
- **Assembly**: `FCMGE  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #0.0`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18 17 16 15  12   9   4  3  |
|-----------------------------------------|
| 011 0010 1   size 010 0   0   0   001 Pg  Zn  0   Pd  |
```

#### Decode (A64.sve.sve_fp_cmpzero.sve_fp_2op_p_pd.fcmge_p_p_z0_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp op = Cmp_GE;
```

### Variant: `Less than`
- **Assembly**: `FCMLT  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #0.0`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18 17 16 15  12   9   4  3  |
|-----------------------------------------|
| 011 0010 1   size 010 0   0   1   001 Pg  Zn  0   Pd  |
```

#### Decode (A64.sve.sve_fp_cmpzero.sve_fp_2op_p_pd.fcmlt_p_p_z0_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp op = Cmp_LT;
```

### Variant: `Less than or equal`
- **Assembly**: `FCMLE  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #0.0`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18 17 16 15  12   9   4  3  |
|-----------------------------------------|
| 011 0010 1   size 010 0   0   1   001 Pg  Zn  1   Pd  |
```

#### Decode (A64.sve.sve_fp_cmpzero.sve_fp_2op_p_pd.fcmle_p_p_z0_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp op = Cmp_LE;
```

### Variant: `Not equal`
- **Assembly**: `FCMNE  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, #0.0`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18 17 16 15  12   9   4  3  |
|-----------------------------------------|
| 011 0010 1   size 010 0   1   1   001 Pg  Zn  0   Pd  |
```

#### Decode (A64.sve.sve_fp_cmpzero.sve_fp_2op_p_pd.fcmne_p_p_z0_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant CmpOp op = Cmp_NE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |

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
- source: `fcmeq_p_p_z0.xml`
</details>