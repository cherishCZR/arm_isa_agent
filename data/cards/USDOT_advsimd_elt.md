## USDOT
_ARM A64 Instruction_

**Title**: USDOT (by element) -- A64 | **Class**: `advsimd` | **XML ID**: `USDOT_advsimd_elt`

**Architecture**: `FEAT_I8MM` (PROFILE_A)

**Summary**: Dot product with unsigned and signed integers (vector, by element)

**Description**:
This instruction performs the dot product of the
four unsigned 8-bit integer values in each 32-bit element of the first source register with the
four signed 8-bit integer values in an indexed 32-bit element of the second source register,
accumulating the result into the corresponding 32-bit element of the destination register.

From Armv8.2 to Armv8.5, this is an OPTIONAL instruction.
From Armv8.6 it is mandatory for implementations that include Advanced SIMD to support it.
ID_AA64ISAR1_EL1.I8MM indicates whether this instruction is supported.

### Variant: `Vector`
- **Assembly**: `USDOT  <Vd>.<Ta>, <Vn>.<Tb>, <Vm>.4B[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23 22 21 20 19  15  11 10  9   4  |
|--------------------------------------------------|
| 0   Q   0   0   111 1   1   0   L   M   Rm  1111 H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdelem.USDOT_asimdelem_D)

```
if !IsFeatureImplemented(FEAT_I8MM) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Rn);
constant integer m = UInt(M:Rm);
constant integer d = UInt(Rd);
constant integer i = UInt(H:L);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV 32;
```

#### Execute (A64.simd_dp.asimdelem.USDOT_asimdelem_D)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(128)      operand2 = V[m, 128];
constant bits(datasize) operand3 = V[d, datasize];
bits(datasize) result;

for e = 0 to elements-1
    bits(32) res = Elem[operand3, e, 32];
    for b = 0 to 3
        constant integer element1 = UInt(Elem[operand1, 4 * e + b, 8]);
        constant integer element2 = SInt(Elem[operand2, 4 * i + b, 8]);
        res = res + element1 * element2;
    Elem[result, e, 32] = res;
V[d, datasize] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_I8MM)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP third source and destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Tb>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vm>` | `register (128-bit)` | `M:Rm` | Is the name of the second SIMD&FP source register, encoded in the "M:Rm" fields. |
| `<index>` | `unknown` | `H:L` | Is the immediate index of a 32-bit group of four 8-bit values, in the range 0 to 3, encoded in the "H:L" fields. |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2S |
| 1 | 4S |

**<Tb> Value Table**:

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

- advsimd-reguse: `2reg-element`
- isa: `A64`
- source: `usdot_advsimd_elt.xml`
</details>