## WHILERW
_ARM A64 Instruction_

**Title**: WHILERW -- A64 | **Class**: `sve2` | **XML ID**: `whilerw_p_rr`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: While free of read-after-write conflicts

**Description**:
This instruction checks
two addresses for a conflict or overlap between
address ranges of the form [addr,addr+VL÷8),
where VL is the accessible vector length in bits,
that could result in a loop-carried
  dependency through memory due to the use of these
addresses by contiguous load and store instructions
within the same iteration of a loop.  Generate a
predicate whose elements are true while the addresses
cannot conflict within the same iteration, and false
thereafter.  Sets the First (N), None (Z), !Last (C)
condition flags based on the predicate result,
and the V flag to zero.

### Variant: `SVE2`
- **Assembly**: `WHILERW  <Pd>.<T>, <Xn>, <Xm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  13  11   9   4  3  |
|--------------------------------------|
| 001 0010 1   size 1   Rm  00  11  00  Rn  1   Pd  |
```

#### Decode (A64.sve.sve_cmpgpr.sve_int_whilenc.whilerw_p_rr_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer d = UInt(Pd);
```

#### Execute (A64.sve.sve_cmpgpr.sve_int_whilenc.whilerw_p_rr_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = Ones(PL);
constant bits(64) src1 = X[n, 64];
constant bits(64) src2 = X[m, 64];
constant integer operand1 = UInt(src1);
constant integer operand2 = UInt(src2);
bits(PL) result;
constant integer psize = esize DIV 8;

constant integer diff = Abs(operand2 - operand1) DIV (esize DIV 8);
for e = 0 to elements-1
    if diff == 0 || e < diff then
        Elem[result, e, psize] = ZeroExtend('1', psize);
    else
        Elem[result, e, psize] = ZeroExtend('0', psize);

PSTATE.<N,Z,C,V> = PredTest(mask, result, esize);
P[d, PL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first source general-purpose register, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second source general-purpose register, encoded in the "Rm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `whilerw_p_rr.xml`
</details>