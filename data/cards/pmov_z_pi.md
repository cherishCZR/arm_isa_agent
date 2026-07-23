## PMOV
_ARM A64 Instruction_

**Title**: PMOV (to vector) -- A64 | **Class**: `sve2` | **XML ID**: `pmov_z_pi`

**Architecture**: `FEAT_SVE2p1 || FEAT_SME2p1` (FEAT_SVE2p1 || FEAT_SME2p1)

**Summary**: Move predicate to vector

**Description**:
Copy the source SVE predicate register elements into the destination vector
register as a packed bitmap with one bit per predicate element, where bit value
0b1 represents a TRUE predicate element, and bit value 0b0 represents a FALSE
predicate element.

Because the number of bits in an SVE predicate element scales with the
vector element size, the behavior varies according to the specified element
size.

The portion index is optional, defaulting to 0 if omitted. When the
index is zero, the instruction writes zeroes to the most significant
VL-(VL/esize) bits of the destination vector register. When a non-zero
index is specified, the packed bitmap is inserted into the destination
vector register, and the unindexed blocks remain unchanged.

### Variant: `Byte`
- **Assembly**: `PMOV  <Zd>, <Pn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  16 15   9  8   4  |
|--------------------------------------|
| 000 0010 1   00  1   01  01  1   001110 0   Pn  Zd  |
```

#### Decode (A64.sve.sve_perm_unpred_d.sve_int_mov_p2v.pmov_z_pi_b)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Pn);
constant integer d = UInt(Zd);
constant integer esize = 8;
constant integer imm = 0;
```

#### Execute (A64.sve.sve_perm_unpred_d.sve_int_mov_p2v.pmov_z_pi_b)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) operand = P[n, PL];
bits(VL) result;

if imm == 0 then
    result = Zeros(VL);
else
    result = Z[d, VL];

for e = 0 to elements-1
    result<(elements * imm) + e> = PredicateElement(operand, e, esize);

Z[d, VL] = result;
```

### Variant: `Doubleword`
- **Assembly**: `PMOV  <Zd>{[<imm>]}, <Pn>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  16 15   9  8   4  |
|-----------------------------------------|
| 000 0010 1   1   i3h 1   01  i3l 1   001110 0   Pn  Zd  |
```

#### Decode (A64.sve.sve_perm_unpred_d.sve_int_mov_p2v.pmov_z_pi_d)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Pn);
constant integer d = UInt(Zd);
constant integer esize = 64;
constant integer imm = UInt(i3h:i3l);
```

### Variant: `Halfword`
- **Assembly**: `PMOV  <Zd>{[<imm>]}, <Pn>.H`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18 17 16 15   9  8   4  |
|-----------------------------------------|
| 000 0010 1   00  1   01  1   i1  1   001110 0   Pn  Zd  |
```

#### Decode (A64.sve.sve_perm_unpred_d.sve_int_mov_p2v.pmov_z_pi_h)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Pn);
constant integer d = UInt(Zd);
constant integer esize = 16;
constant integer imm = UInt(i1);
```

### Variant: `Word`
- **Assembly**: `PMOV  <Zd>{[<imm>]}, <Pn>.S`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  16 15   9  8   4  |
|--------------------------------------|
| 000 0010 1   01  1   01  i2  1   001110 0   Pn  Zd  |
```

#### Decode (A64.sve.sve_perm_unpred_d.sve_int_mov_p2v.pmov_z_pi_s)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Pn);
constant integer d = UInt(Zd);
constant integer esize = 32;
constant integer imm = UInt(i2);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Pn>` | `unknown` | `Pn` | Is the name of the source scalable predicate register, encoded in the "Pn" field. |
| `<imm>` | `immediate` | `i3h:i3l` | For the "Doubleword" variant: is the optional portion index, in the range 0 to 7, defaulting to 0, encoded in the "i3h:i3l" fields. |
| `<imm>` | `immediate` | `i1` | For the "Halfword" variant: is the optional portion index, in the range 0 to 1, defaulting to 0, encoded in the "i1" field. |
| `<imm>` | `immediate` | `i2` | For the "Word" variant: is the optional portion index, in the range 0 to 3, defaulting to 0, encoded in the "i2" field. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p1) \|\| IsFeatureImplemented(FEAT_SME2p1)` |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `pmov_z_pi.xml`
</details>