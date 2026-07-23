## FMLAL_advsimd_vec
_ARM A64 Instruction_

**Title**: FMLAL, FMLAL2 (vector) -- A64 | **Class**: `advsimd` | **XML ID**: `FMLAL_advsimd_vec`

**Architecture**: `FEAT_FHM` (ARMv8.4)

**Summary**: Floating-point fused multiply-add long to accumulator (vector)

**Description**:
This instruction multiplies corresponding half-precision
floating-point values in the vectors in the two source SIMD&FP
registers, and accumulates the intermediate product without rounding
to the corresponding single-precision vector element of the
destination SIMD&FP register.

This instruction can generate a floating-point exception.
  Depending on the settings in FPCR,
  the exception results in either a flag being set in FPSR
  or a synchronous exception being generated.
  For more information, see
  Floating-point exceptions and exception traps.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

In Armv8.2 and Armv8.3, this is an OPTIONAL instruction.
From Armv8.4, it is mandatory for all implementations to support it.

### Variant: `FMLAL`
- **Assembly**: `FMLAL  <Vd>.<Ta>, <Vn>.<Tb>, <Vm>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21 20  15  10  9   4  |
|--------------------------------------------|
| 0   Q   0   0   111 0   0   0   1   Rm  11101 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame.FMLAL_asimdsame_F)

```
if !IsFeatureImplemented(FEAT_FHM) then EndOfDecode(Decode_UNDEF);
if sz == '1' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 32;
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
constant integer part = 0;
```

#### Execute (A64.simd_dp.asimdsame.FMLAL_asimdsame_F)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize DIV 2) operand1 = Vpart[n, part, datasize DIV 2];
constant bits(datasize DIV 2) operand2 = Vpart[m, part, datasize DIV 2];
constant bits(datasize) operand3 = V[d, datasize];
bits(datasize) result;
bits(esize DIV 2) element1;
bits(esize DIV 2) element2;

for e = 0 to elements-1
    element1 = Elem[operand1, e, esize DIV 2];
    element2 = Elem[operand2, e, esize DIV 2];
    Elem[result, e, esize] = FPMulAddH(Elem[operand3, e, esize], element1, element2, FPCR);
V[d, datasize] = result;
```

### Variant: `FMLAL2`
- **Assembly**: `FMLAL2  <Vd>.<Ta>, <Vn>.<Tb>, <Vm>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21 20  15  10  9   4  |
|--------------------------------------------|
| 0   Q   1   0   111 0   0   0   1   Rm  11001 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame.FMLAL2_asimdsame_F)

```
if !IsFeatureImplemented(FEAT_FHM) then EndOfDecode(Decode_UNDEF);
if sz == '1' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 32;
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
constant integer part = 1;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Tb>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2S |
| 1 | 4S |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2H |
| 1 | 4H |

### Encoding Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FHM)` |
| 🚫 ENCODING_UNDEF | `sz != '1'` |

---
<details><summary>Metadata</summary>

- advsimd-reguse: `3reg-same`
- advsimd-type: `simd`
- isa: `A64`
- source: `fmlal_advsimd_vec.xml`
</details>