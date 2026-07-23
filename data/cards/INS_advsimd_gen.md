## INS
_ARM A64 Instruction_

**Title**: INS (general) -- A64 | **Class**: `advsimd` | **XML ID**: `INS_advsimd_gen`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Insert vector element from general-purpose register

**Description**:
This instruction copies the contents of
the source general-purpose register
to the specified vector element in the destination SIMD&FP register.

This instruction can insert data into individual elements within a SIMD&FP
register without clearing the remaining bits to zero.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Advanced SIMD`
- **Assembly**: `INS  <Vd>.<Ts>[<index>], <R><n>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  22  20  15 14  10  9   4  |
|-----------------------------------------|
| 0   1   0   0   111 00  00  imm5 0   0011 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdins.INS_asimdins_IR_r)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if imm5 IN 'x0000' then EndOfDecode(Decode_UNDEF);
constant integer size = LowestSetBitNZ(imm5<3:0>);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer index = UInt(imm5<4:size+1>);
constant integer esize = 8 << size;
```

#### Execute (A64.simd_dp.asimdins.INS_asimdins_IR_r)

```
CheckFPAdvSIMDEnabled64();
constant bits(esize) element = X[n, esize];
bits(128) result = V[d, 128];

Elem[result, index, esize] = element;
V[d, 128] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `imm5 NOT IN 'x0000'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ts>` | `unknown` | `imm5` | Is an element size specifier, |
| `<index>` | `unknown` | `imm5` | Is the element index |
| `<R>` | `unknown` | `imm5` | Is the width specifier for the general-purpose source register, |
| `<n>` | `unknown` | `Rn` | Is the number [0-30] of the general-purpose source register or ZR (31), encoded in the "Rn" field. |

**<Ts> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | B |
| xxx10 | H |
| xx100 | S |
| x1000 | D |

**<index> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | UInt(imm5<4:1>) |
| xxx10 | UInt(imm5<4:2>) |
| xx100 | UInt(imm5<4:3>) |
| x1000 | UInt(imm5<4>) |

**<R> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | W |
| xxx10 | W |
| xx100 | W |
| x1000 | X |

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
- vector-xfer-type: `vector-from-general`
- source: `ins_advsimd_gen.xml`
</details>