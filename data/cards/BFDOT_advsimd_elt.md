## BFDOT
_ARM A64 Instruction_

**Title**: BFDOT (by element) -- A64 | **Class**: `advsimd` | **XML ID**: `BFDOT_advsimd_elt`

**Architecture**: `FEAT_BF16` (ARMv8.6)

**Summary**: BFloat16 floating-point dot product (vector, by element)

**Description**:
This instruction delimits the source vectors into pairs of
BFloat16 elements. The BFloat16 pair within the second source
vector is specified using an immediate index. The index range
is from 0 to 3 inclusive.

If FEAT_EBF16 is not implemented or FPCR.EBF is 0,
this instruction:

If FEAT_EBF16 is implemented and FPCR.EBF is 1,
then this instruction:

Irrespective of FEAT_EBF16 and FPCR.EBF, this instruction:

ID_AA64ISAR1_EL1.BF16 indicates whether this instruction is supported.

### Variant: `Advanced SIMD`
- **Assembly**: `BFDOT  <Vd>.<Ta>, <Vn>.<Tb>, <Vm>.2H[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20 19  15  11 10  9   4  |
|-----------------------------------------------|
| 0   Q   0   0   111 1   01  L   M   Rm  1111 H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdelem.BFDOT_asimdelem_E)

```
if !IsFeatureImplemented(FEAT_BF16) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Rn);
constant integer m = UInt(M:Rm);
constant integer d = UInt(Rd);
constant integer i = UInt(H:L);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV 32;
```

#### Execute (A64.simd_dp.asimdelem.BFDOT_asimdelem_E)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(128)      operand2 = V[m, 128];
constant bits(datasize) operand3 = V[d, datasize];
bits(datasize) result;

for e = 0 to elements-1
    constant bits(16) elt1_a = Elem[operand1, 2 * e + 0, 16];
    constant bits(16) elt1_b = Elem[operand1, 2 * e + 1, 16];
    constant bits(16) elt2_a = Elem[operand2, 2 * i + 0, 16];
    constant bits(16) elt2_b = Elem[operand2, 2 * i + 1, 16];

    constant bits(32) sum = Elem[operand3, e, 32];
    Elem[result, e, 32] = BFDotAdd(sum, elt1_a, elt1_b, elt2_a, elt2_b, FPCR);

V[d, datasize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_BF16)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Tb>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vm>` | `register (128-bit)` | `M:Rm` | Is the name of the second SIMD&FP source register, encoded in the "M:Rm" fields. |
| `<index>` | `unknown` | `H:L` | Is the immediate index of a pair of 16-bit elements in the range 0 to 3, encoded in the "H:L" fields. |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2S |
| 1 | 4S |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 4H |
| 1 | 8H |

---
<details><summary>Metadata</summary>

- advsimd-reguse: `2reg-element`
- isa: `A64`
- source: `bfdot_advsimd_elt.xml`
</details>