## punpkhi_p_p
_ARM A64 Instruction_

**Title**: PUNPKHI, PUNPKLO -- A64 | **Class**: `sve` | **XML ID**: `punpkhi_p_p`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Unpack and widen half of predicate

**Description**:
Unpack elements from the lowest or highest half of the source
predicate and place in elements of twice their
size within the destination predicate.  This instruction is unpredicated.

### Variant: `High half`
- **Assembly**: `PUNPKHI  <Pd>.H, <Pn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  16 15  12   8   4  3  |
|--------------------------------------|
| 000 0010 1   00  1   1000 1   010 0000 Pn  0   Pd  |
```

#### Decode (A64.sve.sve_perm_predicates.sve_int_perm_punpk.punpkhi_p_p_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer n = UInt(Pn);
constant integer d = UInt(Pd);
constant boolean hi = TRUE;
```

#### Execute (A64.sve.sve_perm_predicates.sve_int_perm_punpk.punpkhi_p_p_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) operand = P[n, PL];
bits(PL) result;
constant integer psize = esize DIV 8;

for e = 0 to elements-1
    constant bit pbit = PredicateElement(operand, if hi then e + elements else e, esize DIV 2);
    Elem[result, e, psize] = ZeroExtend(pbit, psize);

P[d, PL] = result;
```

### Variant: `Low half`
- **Assembly**: `PUNPKLO  <Pd>.H, <Pn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  16 15  12   8   4  3  |
|--------------------------------------|
| 000 0010 1   00  1   1000 0   010 0000 Pn  0   Pd  |
```

#### Decode (A64.sve.sve_perm_predicates.sve_int_perm_punpk.punpklo_p_p_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer n = UInt(Pn);
constant integer d = UInt(Pd);
constant boolean hi = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<Pn>` | `unknown` | `Pn` | Is the name of the source scalable predicate register, encoded in the "Pn" field. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `punpkhi_p_p.xml`
</details>