## PMLAL
_ARM A64 Instruction_

**Title**: PMLAL -- A64 | **Class**: `sve2` | **XML ID**: `pmlal_mz_zzzw`

**Architecture**: `FEAT_SVE_AES2` (ARMv9.6)

**Summary**: Multi-vector polynomial multiply long and accumulate vectors

**Description**:
Polynomial multiply over [0, 1] the corresponding even-numbered elements of the first and
second source vectors, and bitwise exclusive-OR the result with the overlapping double-width
elements of the first destination vector. Perform the same operation with odd-numbered elements
of the source vectors, writing to the second destination vector. This instruction is unpredicated.

This instruction is legal when executed in Streaming SVE mode if both FEAT_SSVE_AES
and FEAT_SVE_AES2 are implemented.

**Attributes**: SM Policy: `SM_0_or_1`

### Variant: `SVE2`
- **Assembly**: `PMLAL  { <Zda1>.Q-<Zda2>.Q }, <Zn>.D, <Zm>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12   9   4   0 |
|-----------------------------------|
| 010 0010 1   00  1   Zm  111 111 Zn  Zda 0   |
```

#### Decode (A64.sve.sve_intx_crypto.sve_crypto_pmlal_multi.pmlal_mz_zzzw_1x2)

```
if !IsFeatureImplemented(FEAT_SVE_AES2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 128;
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda:'0');
```

#### Execute (A64.sve.sve_intx_crypto.sve_crypto_pmlal_multi.pmlal_mz_zzzw_1x2)

```
if IsFeatureImplemented(FEAT_SSVE_AES) then
    CheckSVEEnabled();
else
    CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result_lo = Z[da + 0, VL];
bits(VL) result_hi = Z[da + 1, VL];

for e = 0 to elements-1
    constant bits(esize DIV 2) element1_lo = Elem[operand1, 2*e + 0, esize DIV 2];
    constant bits(esize DIV 2) element2_lo = Elem[operand2, 2*e + 0, esize DIV 2];
    constant bits(esize DIV 2) element1_hi = Elem[operand1, 2*e + 1, esize DIV 2];
    constant bits(esize DIV 2) element2_hi = Elem[operand2, 2*e + 1, esize DIV 2];
    constant bits(esize) product_lo = PolynomialMult(element1_lo, element2_lo);
    constant bits(esize) product_hi = PolynomialMult(element1_hi, element2_hi);
    Elem[result_lo, e, esize] = Elem[result_lo, e, esize] EOR product_lo;
    Elem[result_hi, e, esize] = Elem[result_hi, e, esize] EOR product_hi;

Z[da + 0, VL] = result_lo;
Z[da + 1, VL] = result_hi;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE_AES2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda1>` | `register (128-bit)` | `Zda` | Is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zda" times 2. |
| `<Zda2>` | `register (128-bit)` | `Zda` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zda" times 2 plus 1. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- ldstruct-regcount: `to-2reg`
- source: `pmlal_mz_zzzw.xml`
</details>