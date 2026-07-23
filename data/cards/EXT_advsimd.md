## EXT
_ARM A64 Instruction_

**Title**: EXT -- A64 | **Class**: `advsimd` | **XML ID**: `EXT_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Extract vector from pair of vectors

**Description**:
This instruction extracts the lowest vector elements from the
second source SIMD&FP register and the highest vector elements from the first
source SIMD&FP register,
concatenates the results into a vector,
and writes the vector to the destination SIMD&FP register vector.
The index value specifies the lowest vector element to extract from the
first source register, and consecutive elements are extracted from
the first, then second, source registers until the destination vector is filled.



Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Advanced SIMD`
- **Assembly**: `EXT  <Vd>.<T>, <Vn>.<T>, <Vm>.<T>, #<index>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  27  24 23  21 20  15 14  10  9   4  |
|-----------------------------------------|
| 0   Q   10  111 0   00  0   Rm  0   imm4 0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdext.EXT_asimdext_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if Q == '0' && imm4<3> == '1' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = 64 << UInt(Q);
constant integer position = 8 * UInt(imm4);
```

#### Execute (A64.simd_dp.asimdext.EXT_asimdext_only)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) hi = V[m, datasize];
constant bits(datasize) lo = V[n, datasize];
constant bits(datasize*2) concat = hi : lo;

V[d, datasize] = concat<(position+datasize)-1:position>;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `Q != '0' \|\| imm4<3> != '1'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<index>` | `unknown` | `Q:imm4` | Is the lowest numbered byte element to be extracted, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |

**<index> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | UInt(imm4<2:0>) |
| 1 | RESERVED |
| x | UInt(imm4) |

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
- source: `ext_advsimd.xml`
</details>