## URSQRTE
_ARM A64 Instruction_

**Title**: URSQRTE -- A64 | **Class**: `advsimd` | **XML ID**: `URSQRTE_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Unsigned reciprocal square root estimate

**Description**:
This instruction reads each vector element
from the source SIMD&FP register,
calculates an approximate inverse square root for each value,
places the result into a vector,
and writes
the vector to the destination SIMD&FP
register.
All the values in this instruction are unsigned integer values.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Vector`
- **Assembly**: `URSQRTE  <Vd>.<T>, <Vn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21  16  11   9   4  |
|-----------------------------------------|
| 0   Q   1   0   111 0   1   sz  10000 11100 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.URSQRTE_asimdmisc_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

if sz == '1' then EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
```

#### Execute (A64.simd_dp.asimdmisc.URSQRTE_asimdmisc_R)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = V[n, datasize];
bits(datasize) result;
bits(32) element;

for e = 0 to elements-1
    element = Elem[operand, e, 32];
    Elem[result, e, 32] = UnsignedRSqrtEstimate(element);

V[d, datasize] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `sz != '1'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `arrangement` | `sz:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2S |
| 1 | 4S |
| x | RESERVED |

---
<details><summary>Metadata</summary>

- advsimd-type: `simd`
- isa: `A64`
- source: `ursqrte_advsimd.xml`
</details>