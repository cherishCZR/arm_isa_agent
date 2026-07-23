## PMOV
_ARM A64 Instruction_

**Title**: PMOV (to predicate) -- A64 | **Class**: `sve2` | **XML ID**: `pmov_p_zi`

**Architecture**: `FEAT_SVE2p1 || FEAT_SME2p1` (FEAT_SVE2p1 || FEAT_SME2p1)

**Summary**: Move predicate from vector

**Description**:
Copy a packed bitmap, where bit value 0b1 represents TRUE and bit value 0b0
represents FALSE, from a portion of the source vector register to elements of the
destination SVE predicate register.

Because the number of bits in an SVE predicate element scales with the vector
element size, the behavior varies according to the specified element size.

The portion index is optional, defaulting to 0 if omitted.

### Variant: `Byte`
- **Assembly**: `PMOV  <Pd>.B, <Zn>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  16 15   9   4  3  |
|--------------------------------------|
| 000 0010 1   00  1   01  01  0   001110 Zn  0   Pd  |
```

#### Decode (A64.sve.sve_perm_unpred_d.sve_int_mov_v2p.pmov_p_zi_b)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant integer esize = 8;
constant integer imm = 0;
```

#### Execute (A64.sve.sve_perm_unpred_d.sve_int_mov_v2p.pmov_p_zi_b)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(VL) operand = Z[n, VL];
bits(PL) result;
constant integer psize = esize DIV 8;

for e = 0 to elements-1
    Elem[result, e, psize] = ZeroExtend(operand<(elements * imm) + e>, psize);

P[d, PL] = result;
```

### Variant: `Doubleword`
- **Assembly**: `PMOV  <Pd>.D, <Zn>{[<imm>]}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  16 15   9   4  3  |
|-----------------------------------------|
| 000 0010 1   1   i3h 1   01  i3l 0   001110 Zn  0   Pd  |
```

#### Decode (A64.sve.sve_perm_unpred_d.sve_int_mov_v2p.pmov_p_zi_d)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant integer esize = 64;
constant integer imm = UInt(i3h:i3l);
```

### Variant: `Halfword`
- **Assembly**: `PMOV  <Pd>.H, <Zn>{[<imm>]}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18 17 16 15   9   4  3  |
|-----------------------------------------|
| 000 0010 1   00  1   01  1   i1  0   001110 Zn  0   Pd  |
```

#### Decode (A64.sve.sve_perm_unpred_d.sve_int_mov_v2p.pmov_p_zi_h)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant integer esize = 16;
constant integer imm = UInt(i1);
```

### Variant: `Word`
- **Assembly**: `PMOV  <Pd>.S, <Zn>{[<imm>]}`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  16 15   9   4  3  |
|--------------------------------------|
| 000 0010 1   01  1   01  i2  0   001110 Zn  0   Pd  |
```

#### Decode (A64.sve.sve_perm_unpred_d.sve_int_mov_v2p.pmov_p_zi_s)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer d = UInt(Pd);
constant integer esize = 32;
constant integer imm = UInt(i2);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Pd>` | `unknown` | `Pd` | Is the name of the destination scalable predicate register, encoded in the "Pd" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
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
- source: `pmov_p_zi.xml`
</details>