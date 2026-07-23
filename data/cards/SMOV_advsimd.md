## SMOV
_ARM A64 Instruction_

**Title**: SMOV -- A64 | **Class**: `advsimd` | **XML ID**: `SMOV_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Signed move vector element to general-purpose register

**Description**:
This instruction reads the signed integer from the
source SIMD&FP register,
sign-extends it to form a 32-bit or 64-bit value, and writes the result to
destination general-purpose register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Advanced SIMD (SMOV_asimdins_W_w)` (32-bit)
- **Condition**: `Q == 0`
- **Assembly**: `SMOV  <Wd>, <Vn>.<Ts>[<index>]`
- **Fixed bits**: `Q`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15 14  10  9   4  |
|--------------------------------|
| 0   Q   0   01110000 imm5 0   0101 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdins.SMOV_asimdins_W_w)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if imm5 IN 'xx000' then EndOfDecode(Decode_UNDEF);
constant integer size = LowestSetBitNZ(imm5<2:0>);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 8 << size;
constant integer datasize = 32 << UInt(Q);
if datasize <= esize then EndOfDecode(Decode_UNDEF);
constant integer index = UInt(imm5<4:size+1>);
constant integer idxdsize = 64 << UInt(imm5<4>);
```

#### Execute (A64.simd_dp.asimdins.SMOV_asimdins_W_w)

```
if index == 0 then
    CheckFPEnabled64();
else
    CheckFPAdvSIMDEnabled64();
constant bits(idxdsize) operand = V[n, idxdsize];

X[d, datasize] = SignExtend(Elem[operand, index, esize], datasize);
```

#### Constraints
_2× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `imm5 NOT IN 'xx000'` |
| 🚫 ENCODING_UNDEF | `datasize <= esize` |

### Variant: `Advanced SIMD (SMOV_asimdins_X_x)` (64-bit)
- **Condition**: `Q == 1`
- **Assembly**: `SMOV  <Xd>, <Vn>.<Ts>[<index>]`
- **Fixed bits**: `Q`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15 14  10  9   4  |
|--------------------------------|
| 0   Q   0   01110000 imm5 0   0101 1   Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Ts>` | `unknown` | `imm5` | For the "32-bit" variant: is an element size specifier, |
| `<Ts>` | `unknown` | `imm5` | For the "64-bit" variant: is an element size specifier, |
| `<index>` | `unknown` | `imm5` | For the "32-bit" variant: is the element index |
| `<index>` | `unknown` | `imm5` | For the "64-bit" variant: is the element index |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |

**<Ts> Value Table**:

| bitfield | symbol |
|---|---|
| xxx00 | RESERVED |
| xxxx1 | B |
| xxx10 | H |

**<Ts> Value Table**:

| bitfield | symbol |
|---|---|
| xx000 | RESERVED |
| xxxx1 | B |
| xxx10 | H |
| xx100 | S |

**<index> Value Table**:

| bitfield | symbol |
|---|---|
| xxx00 | RESERVED |
| xxxx1 | UInt(imm5<4:1>) |
| xxx10 | UInt(imm5<4:2>) |

**<index> Value Table**:

| bitfield | symbol |
|---|---|
| xx000 | RESERVED |
| xxxx1 | UInt(imm5<4:1>) |
| xxx10 | UInt(imm5<4:2>) |
| xx100 | UInt(imm5<4:3>) |

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
- vector-xfer-type: `general-from-element`
- source: `smov_advsimd.xml`
</details>