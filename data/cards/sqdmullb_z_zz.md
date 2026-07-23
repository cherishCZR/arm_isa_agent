## SQDMULLB
_ARM A64 Instruction_

**Title**: SQDMULLB (vectors) -- A64 | **Class**: `sve2` | **XML ID**: `sqdmullb_z_zz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Signed saturating doubling multiply long (bottom)

**Description**:
Multiply the corresponding even-numbered signed elements of the first
and second source vectors, double and place the results in
the overlapping double-width elements of the destination vector.
Each result element is saturated to the
double-width N-bit element's
signed integer range -2(N-1)  to (2(N-1))-1.
This instruction is unpredicated.

### Variant: `SVE2`
- **Assembly**: `SQDMULLB  <Zd>.<T>, <Zn>.<Tb>, <Zm>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15 14  12 11 10  9   4  |
|-----------------------------------------|
| 010 0010 1   size 0   Zm  0   11  0   0   0   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_cons_widening.sve_intx_cons_mul_long.sqdmullb_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_intx_cons_widening.sve_intx_cons_mul_long.sqdmullb_z_zz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer element1 = SInt(Elem[operand1, 2*e + 0, esize DIV 2]);
    constant integer element2 = SInt(Elem[operand2, 2*e + 0, esize DIV 2]);
    constant integer res = 2 * element1 * element2;
    Elem[result, e, esize] = SignedSat(res, esize);

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Tb>` | `unknown` | `size` | Is the size specifier, |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | B |
| 10 | H |
| 11 | S |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `sqdmullb_z_zz.xml`
</details>