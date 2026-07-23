## SPLICE
_ARM A64 Instruction_

**Title**: SPLICE -- A64 | **Class**: `sve` | **XML ID**: `splice_z_p_zz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME), `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Splice two vectors under predicate control

**Description**:
Select a region from the first source vector and copy it to the
lowest-numbered elements of the result. Then set any remaining elements
of the result to a copy of the lowest-numbered elements from the second
source vector. The region is selected using the first and last true
elements in the vector select predicate register.
The result is placed
destructively in the destination and first source vector,
   or constructively in the destination vector.

### Variant: `Constructive`
- **Assembly**: `SPLICE  <Zd>.<T>, <Pv>, { <Zn1>.<T>, <Zn2>.<T> }`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  16 15  13 12   9   4  |
|-----------------------------------------|
| 000 0010 1   size 1   0   110 1   10  0   Pv  Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_pred.sve_intx_perm_splice.splice_z_p_zz_con)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer v = UInt(Pv);
constant integer dst = UInt(Zd);
constant integer s1 = UInt(Zn);
constant integer s2 = (s1 + 1) MOD 32;
```

#### Execute (A64.sve.sve_perm_pred.sve_intx_perm_splice.splice_z_p_zz_con)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer PL = VL DIV 8;
constant integer elements = VL DIV esize;
constant bits(PL) mask = P[v, PL];
constant bits(VL) operand1 = if AnyActiveElement(mask, esize) then Z[s1, VL] else Zeros(VL);
constant bits(VL) operand2 = Z[s2, VL];
bits(VL) result;
integer x = 0;
boolean active = FALSE;
constant integer lastnum = LastActiveElement(mask, esize);

if lastnum >= 0 then
    for e = 0 to lastnum
        active = active || ActivePredicateElement(mask, e, esize);
        if active then
            Elem[result, x, esize] = Elem[operand1, e, esize];
            x = x + 1;

constant integer nelements = (elements - x) - 1;
for e = 0 to nelements
    Elem[result, x, esize] = Elem[operand2, e, esize];
    x = x + 1;

Z[dst, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Variant: `Destructive`
- **Assembly**: `SPLICE  <Zdn>.<T>, <Pv>, <Zdn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  16 15  13 12   9   4  |
|-----------------------------------------|
| 000 0010 1   size 1   0   110 0   10  0   Pv  Zm  Zdn |
```

#### Decode (A64.sve.sve_perm_pred.sve_int_perm_splice.splice_z_p_zz_des)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer v = UInt(Pv);
constant integer dst = UInt(Zdn);
constant integer s1 = dst;
constant integer s2 = UInt(Zm);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Pv>` | `unknown` | `Pv` | Is the name of the vector select predicate register P0-P7, encoded in the "Pv" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded in the "Zn" field. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the source multi-vector group, encoded in the "Zn" field. |
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the first source and destination scalable vector register, encoded in the "Zdn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

### Operational Notes

The destructive variant of this instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must
conform to all of the following requirements, otherwise the behavior of the MOVPRFX and the destructive variant of this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `splice_z_p_zz.xml`
</details>