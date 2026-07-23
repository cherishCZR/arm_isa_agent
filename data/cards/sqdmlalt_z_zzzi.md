## SQDMLALT
_ARM A64 Instruction_

**Title**: SQDMLALT (indexed) -- A64 | **Class**: `sve2` | **XML ID**: `sqdmlalt_z_zzzi`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Signed saturating doubling multiply-add long to accumulator (top, indexed)

**Description**:
Multiply then double the odd-numbered signed elements within each 128-bit segment
of the first source vector and the specified signed element in the corresponding
second source vector segment. Each intermediate value is saturated to the
double-width N-bit value's
signed integer range -2(N-1)  to (2(N-1))-1.
Then destructively add to the overlapping double-width elements of the
addend and destination vector.
Each destination element is saturated to the
double-width N-bit element's
signed integer range -2(N-1)  to (2(N-1))-1.

The elements within the second source vector are specified using
an immediate index which selects the same element position within
each 128-bit vector segment.  The index range is from 0 to
one less than the number of elements per 128-bit segment.

### Variant: `32-bit`
- **Assembly**: `SQDMLALT  <Zda>.S, <Zn>.H, <Zm>.H[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  12 11 10  9   4  |
|-----------------------------------------|
| 010 0010 0   10  1   i3h Zm  001 0   i3l 1   Zn  Zda |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_qdmla_long_by_indexed_elem.sqdmlalt_z_zzzi_s)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 16;
constant integer index = UInt(i3h:i3l);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant integer sel = 1;
```

#### Execute (A64.sve.sve_intx_by_indexed_elem.sve_intx_qdmla_long_by_indexed_elem.sqdmlalt_z_zzzi_s)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV (2 * esize);
constant integer eltspersegment = 128 DIV (2 * esize);
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result = Z[da, VL];

for e = 0 to elements-1
    constant integer s = e - (e MOD eltspersegment);
    constant integer element1 = SInt(Elem[operand1, 2 * e + sel,   esize]);
    constant integer element2 = SInt(Elem[operand2, 2 * s + index, esize]);
    constant integer element3 = SInt(Elem[result, e, 2*esize]);
    constant integer product = SInt(SignedSat(2 * element1 * element2, 2*esize));
    constant integer res = element3 + product;
    Elem[result, e, 2*esize] = SignedSat(res, 2*esize);

Z[da, VL] = result;
```

### Variant: `64-bit`
- **Assembly**: `SQDMLALT  <Zda>.D, <Zn>.S, <Zm>.S[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15  12 11 10  9   4  |
|-----------------------------------------|
| 010 0010 0   11  1   i2h Zm  001 0   i2l 1   Zn  Zda |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_qdmla_long_by_indexed_elem.sqdmlalt_z_zzzi_d)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer index = UInt(i2h:i2l);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant integer sel = 1;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "32-bit" variant: is the name of the second source scalable vector register Z0-Z7, encoded in the "Zm" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | For the "64-bit" variant: is the name of the second source scalable vector register Z0-Z15, encoded in the "Zm" field. |
| `<imm>` | `immediate` | `i3h:i3l` | For the "32-bit" variant: is the element index, in the range 0 to 7, encoded in the "i3h:i3l" fields. |
| `<imm>` | `immediate` | `i2h:i2l` | For the "64-bit" variant: is the element index, in the range 0 to 3, encoded in the "i2h:i2l" fields. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operational Notes

This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqdmlalt_z_zzzi.xml`
</details>