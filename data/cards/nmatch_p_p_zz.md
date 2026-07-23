## NMATCH
_ARM A64 Instruction_

**Title**: NMATCH -- A64 | **Class**: `sve2` | **XML ID**: `nmatch_p_p_zz`

**Architecture**: `FEAT_SVE2` (ARMv9.0)

**Summary**: Detect no matching elements, setting the condition flags

**Description**:
This instruction compares each active 8-bit or 16-bit character in the first
source vector with all of the characters in the corresponding
128-bit segment of the second source vector. Where the
first source element detects
no matching characters
in the second segment it places true in the corresponding element of the
destination predicate, otherwise false. Inactive elements in the destination predicate register are set to zero.
Sets the First (N), None (Z), !Last (C)
condition flags based on the predicate result,
and the V flag to zero.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: Predicated; SM Policy: `SM_0_only`

### Variant: `SVE2`
- **Assembly**: `NMATCH  <Pd>.<T>, <Pg>/Z, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12   9   4  3  |
|-----------------------------------|
| 010 0010 1   size 1   Zm  100 Pg  Zn  1   Pd  |
```

#### Decode (A64.sve.sve_intx_string.sve_intx_match.nmatch_p_p_zz_)

```
if !IsFeatureImplemented(FEAT_SVE2) then EndOfDecode(Decode_UNDEF);
if size IN {'1x'} then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer g = UInt(Pg);
constant integer d = UInt(Pd);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
```

#### Execute (A64.sve.sve_intx_string.sve_intx_match.nmatch_p_p_zz_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant integer eltspersegment = 128 DIV esize;
constant bits(PL) mask = P[g, PL];
constant bits(VL) operand1 = if AnyActiveElement(mask, esize) then Z[n, VL] else Zeros(VL);
constant bits(VL) operand2 = if AnyActiveElement(mask, esize) then Z[m, VL] else Zeros(VL);
bits(PL) result;
constant integer psize = esize DIV 8;

for e = 0 to elements-1
    if ActivePredicateElement(mask, e, esize) then
        constant integer segmentbase = e - (e MOD eltspersegment);
        Elem[result, e, psize] = ZeroExtend('1', psize);
        constant bits(esize) element1 = Elem[operand1, e, esize];
        for i = segmentbase to (segmentbase + eltspersegment) - 1
            constant bits(esize) element2 = Elem[operand2, i, esize];
            if element1 == element2 then
                Elem[result, e, psize] = ZeroExtend('0', psize);
    else
        Elem[result, e, psize] = ZeroExtend('0', psize);

PSTATE.<N,Z,C,V> = PredTest(mask, result, esize);
P[d, PL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2)` |
| 🚫 ENCODING_UNDEF | `size IN{'1x'}` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<T>` | `unknown` | `size<0>` | Is the size specifier, |
| `<Pg>` | `unknown` | `Pg` | Is the name of the governing scalable predicate register P0-P7, encoded in the "Pg" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | B |
| 1 | H |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `nmatch_p_p_zz.xml`
</details>