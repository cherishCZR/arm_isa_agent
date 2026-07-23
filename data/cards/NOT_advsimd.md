## NOT
_ARM A64 Instruction_

**Title**: NOT -- A64 | **Class**: `advsimd` | **XML ID**: `NOT_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Bitwise NOT (vector)

**Description**:
This instruction reads each vector element from the source SIMD&FP register,
places the inverse of each value into a vector, and writes the
vector to the destination SIMD&FP register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Vector`
- **Assembly**: `NOT  <Vd>.<T>, <Vn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21  16  11   9   4  |
|--------------------------------------|
| 0   Q   1   0   111 0   00  10000 00101 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.NOT_asimdmisc_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer esize = 8;
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV 8;
```

#### Execute (A64.simd_dp.asimdmisc.NOT_asimdmisc_R)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = V[n, datasize];
bits(datasize) result;
bits(esize) element;

for e = 0 to elements-1
    element = Elem[operand, e, esize];
    Elem[result, e, esize] = NOT(element);

V[d, datasize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |

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

- advsimd-type: `simd`
- isa: `A64`
- source: `not_advsimd.xml`
</details>