## CNTP
_ARM A64 Instruction_

**Title**: CNTP (predicate as counter) -- A64 | **Class**: `sve2` | **XML ID**: `cntp_r_pn`

**Architecture**: `FEAT_SME2 || FEAT_SVE2p1` (FEAT_SME2 || FEAT_SVE2p1)

**Summary**: Set scalar to count from predicate-as-counter

**Description**:
Counts the number of true elements in the source predicate
and places the scalar result in the destination general-purpose register.

**Attributes**: SM Policy: `SM_1_or_SVE2p1`

### Variant: `SVE2`
- **Assembly**: `CNTP  <Xd>, <PNn>.<T>, <vl>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21  18  15  13  10  9  8   4  |
|--------------------------------------|
| 001 0010 1   size 100 000 10  000 vl  1   PNn Rd  |
```

#### Decode (A64.sve.sve_pred_count_a.sve_int_pcount_pn.cntp_r_pn_)

```
if !IsFeatureImplemented(FEAT_SME2) && !IsFeatureImplemented(FEAT_SVE2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(PNn);
constant integer d = UInt(Rd);
constant integer width = 2 << UInt(vl);
```

#### Execute (A64.sve.sve_pred_count_a.sve_int_pcount_pn.cntp_r_pn_)

```
if IsFeatureImplemented(FEAT_SVE2p1) then CheckSVEEnabled(); else CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) pred = P[n, PL];
constant bits(PL*4) mask = CounterToPredicate(pred<15:0>, PL*4);
bits(64) sum = Zeros(64);
constant integer maxelements = elements * width;

for e = 0 to maxelements-1
    if ActivePredicateElement(mask, e, esize) then
        sum = sum + 1;
X[d, 64] = sum;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2) \|\| IsFeatureImplemented(FEAT_SVE2p1)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the destination general-purpose register, encoded in the "Rd" field. |
| `<PNn>` | `unknown` | `PNn` | Is the name of the source scalable predicate register, with predicate-as-counter encoding, encoded in the "PNn" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<vl>` | `unknown` | `vl` | Is the vl specifier, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<vl> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | VLx2 |
| 1 | VLx4 |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `cntp_r_pn.xml`
</details>