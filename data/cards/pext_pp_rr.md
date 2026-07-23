## PEXT
_ARM A64 Instruction_

**Title**: PEXT (predicate pair) -- A64 | **Class**: `sve2` | **XML ID**: `pext_pp_rr`

**Architecture**: `FEAT_SME2 || FEAT_SVE2p1` (FEAT_SME2 || FEAT_SVE2p1)

**Summary**: Predicate extract pair from predicate-as-counter

**Description**:
Converts the source predicate-as-counter into a four register wide predicate-as-mask, and
copies the two portions of the mask value selected by the portion index to the two
destination predicate registers. A portion corresponds to a one predicate register fraction
of the wider predicate-as-mask value.

**Attributes**: SM Policy: `SM_1_or_SVE2p1`

### Variant: `SVE2`
- **Assembly**: `PEXT  { <Pd1>.<T>, <Pd2>.<T> }, <PNn>[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  13  10   8  7   4  3  |
|-----------------------------------------|
| 001 0010 1   size 1   00000 01  110 10  i1  PNn 1   Pd  |
```

#### Decode (A64.sve.sve_while_pn.sve_int_ctr_to_mask.pext_pp_rr_)

```
if !IsFeatureImplemented(FEAT_SME2) && !IsFeatureImplemented(FEAT_SVE2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt('1':PNn);
constant integer d0 = UInt(Pd);
constant integer d1 = (UInt(Pd) + 1) MOD 16;
constant integer part = UInt(i1);
```

#### Execute (A64.sve.sve_while_pn.sve_int_ctr_to_mask.pext_pp_rr_)

```
if IsFeatureImplemented(FEAT_SVE2p1) then CheckSVEEnabled(); else CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) pred = P[n, PL];
constant bits(PL*4) mask = CounterToPredicate(pred<15:0>, PL*4);
bits(PL) result0;
bits(PL) result1;
constant integer psize = esize DIV 8;

for e = 0 to elements-1
    constant bit pbit = PredicateElement(mask, part * 2 * elements + e, esize);
    Elem[result0, e, psize] = ZeroExtend(pbit, psize);

for e = 0 to elements-1
    constant bit pbit = PredicateElement(mask, part * 2 * elements + elements + e, esize);
    Elem[result1, e, psize] = ZeroExtend(pbit, psize);

P[d0, PL] = result0;
P[d1, PL] = result1;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) \|\| IsFeatureImplemented(FEAT_SVE2p1)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd1>` | `unknown` | `Pd` | Is the name of the first destination scalable predicate register, encoded in the "Pd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pd2>` | `unknown` | `Pd` | Is the name of the second destination scalable predicate register, encoded in the "Pd" field. |
| `<PNn>` | `unknown` | `PNn` | Is the name of the first source scalable predicate register PN8-PN15, with predicate-as-counter encoding, encoded in the "PNn" field. |
| `<imm>` | `immediate` | `i1` | Is the portion index, in the range 0 to 1, encoded in the "i1" field. |

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
- source: `pext_pp_rr.xml`
</details>