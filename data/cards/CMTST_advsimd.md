## CMTST
_ARM A64 Instruction_

**Title**: CMTST -- A64 | **Class**: `advsimd` | **XML ID**: `CMTST_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Compare bitwise test bits nonzero (vector)

**Description**:
This instruction reads each vector element in the first source SIMD&FP register,
performs an AND with the corresponding vector element in the second source SIMD&FP register,
and if the result is not zero, sets every bit of the corresponding vector element
in the destination SIMD&FP register to one,
otherwise sets every bit of the corresponding vector element
in the destination SIMD&FP register to zero.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Scalar`
- **Assembly**: `CMTST  D<d>, D<n>, D<m>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23  21 20  15  10  9   4  |
|--------------------------------------|
| 01  0   1   111 0   11  1   Rm  10001 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdsame.CMTST_asisdsame_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 8 << UInt(size);
constant integer datasize = esize;
constant integer elements = 1;
```

#### Execute (A64.simd_dp.asisdsame.CMTST_asisdsame_only)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(datasize) operand2 = V[m, datasize];
bits(datasize) result;
bits(esize) element1;
bits(esize) element2;

for e = 0 to elements-1
    element1 = Elem[operand1, e, esize];
    element2 = Elem[operand2, e, esize];
    Elem[result, e, esize] = if !IsZero(element1 AND element2) then Ones(esize) else Zeros(esize);

V[d, datasize] = result;
```

### Variant: `Vector`
- **Assembly**: `CMTST  <Vd>.<T>, <Vn>.<T>, <Vm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15  10  9   4  |
|-----------------------------------------|
| 0   Q   0   0   111 0   size 1   Rm  10001 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame.CMTST_asimdsame_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if size:Q == '110' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 8 << UInt(size);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `size:Q != '110'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<d>` | `register (64-bit)` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<n>` | `register (64-bit)` | `Rn` | Is the number of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<m>` | `register (64-bit)` | `Rm` | Is the number of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `arrangement` | `size:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| 0 | RESERVED |
| 1 | 2D |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `cmtst_advsimd.xml`
</details>