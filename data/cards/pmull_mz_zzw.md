## PMULL
_ARM A64 Instruction_

**Title**: PMULL -- A64 | **Class**: `sve2` | **XML ID**: `pmull_mz_zzw`

**Architecture**: `FEAT_SVE_AES2` (ARMv9.6)

**Summary**: Multi-vector polynomial multiply long

**Description**:
Polynomial multiply over [0, 1] the corresponding even-numbered elements of the first and
second source vectors, and place the results in the overlapping double-width
elements of the first destination vector. Perform the same operation with odd-numbered elements
of the source vectors, writing to the second destination vector. This instruction is unpredicated.

This instruction is legal when executed in Streaming SVE mode if both FEAT_SSVE_AES
and FEAT_SVE_AES2 are implemented.

**Attributes**: SM Policy: `SM_0_or_1`

### Variant: `SVE2`
- **Assembly**: `PMULL  { <Zd1>.Q-<Zd2>.Q }, <Zn>.D, <Zm>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12   9   4   0 |
|-----------------------------------|
| 010 0010 1   00  1   Zm  111 110 Zn  Zd  0   |
```

#### Decode (A64.sve.sve_intx_crypto.sve_crypto_pmull_multi.pmull_mz_zzw_1x2)

```
if !IsFeatureImplemented(FEAT_SVE_AES2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 128;
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd:'0');
```

#### Execute (A64.sve.sve_intx_crypto.sve_crypto_pmull_multi.pmull_mz_zzw_1x2)

```
if IsFeatureImplemented(FEAT_SSVE_AES) then
    CheckSVEEnabled();
else
    CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result_lo;
bits(VL) result_hi;

for e = 0 to elements-1
    constant bits(esize DIV 2) element1_lo = Elem[operand1, 2*e + 0, esize DIV 2];
    constant bits(esize DIV 2) element2_lo = Elem[operand2, 2*e + 0, esize DIV 2];
    constant bits(esize DIV 2) element1_hi = Elem[operand1, 2*e + 1, esize DIV 2];
    constant bits(esize DIV 2) element2_hi = Elem[operand2, 2*e + 1, esize DIV 2];
    Elem[result_lo, e, esize] = PolynomialMult(element1_lo, element2_lo);
    Elem[result_hi, e, esize] = PolynomialMult(element1_hi, element2_hi);

Z[d + 0, VL] = result_lo;
Z[d + 1, VL] = result_hi;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE_AES2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | Is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 2. |
| `<Zd2>` | `register (128-bit)` | `Zd` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zd" times 2 plus 1. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- ldstruct-regcount: `to-2reg`
- source: `pmull_mz_zzw.xml`
</details>