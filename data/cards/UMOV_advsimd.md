## UMOV
_ARM A64 Instruction_

**Title**: UMOV -- A64 | **Class**: `advsimd` | **XML ID**: `UMOV_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Unsigned move vector element to general-purpose register

**Description**:
This instruction reads the unsigned integer from the
source SIMD&FP register,
zero-extends it to form a 32-bit or 64-bit value, and writes the result to
the destination general-purpose register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Advanced SIMD (UMOV_asimdins_W_w)` (32-bit)
- **Condition**: `Q == 0`
- **Assembly**: `UMOV  <Wd>, <Vn>.<Ts>[<index>]`
- **Fixed bits**: `Q`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15 14  10  9   4  |
|--------------------------------|
| 0   Q   0   01110000 imm5 0   0111 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdins.UMOV_asimdins_W_w)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if imm5 IN 'x0000' then EndOfDecode(Decode_UNDEF);
constant integer size = LowestSetBitNZ(imm5<3:0>);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 8 << size;
constant integer datasize = 32 << UInt(Q);
if datasize == 64 && esize < 64 then EndOfDecode(Decode_UNDEF);
if datasize == 32 && esize >= 64 then EndOfDecode(Decode_UNDEF);
constant integer index = UInt(imm5<4:size+1>);
constant integer idxdsize = 64 << UInt(imm5<4>);
```

#### Execute (A64.simd_dp.asimdins.UMOV_asimdins_W_w)

```
if index == 0 then
    CheckFPEnabled64();
else
    CheckFPAdvSIMDEnabled64();
constant bits(idxdsize) operand = V[n, idxdsize];

X[d, datasize] = ZeroExtend(Elem[operand, index, esize], datasize);
```

#### Constraints
_3× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `imm5 NOT IN 'x0000'` |
| 🚫 ENCODING_UNDEF | `datasize != 64 \|\| esize < 64` |
| 🚫 ENCODING_UNDEF | `datasize != 32 \|\| esize >= 64` |

### Variant: `Advanced SIMD (UMOV_asimdins_X_x)` (64-bit)
- **Condition**: `Q == 1 && imm5 == x1000`
- **Assembly**: `UMOV  <Xd>, <Vn>.D[<index>]`
- **Fixed bits**: `Q`=`1`, `imm5`=`1000`
- **Bit Pattern**: `????????????????0001??????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  20  15 14  10  9   4  |
|--------------------------------|
| 0   Q   0   01110000 imm5 0   0111 1   Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Ts>` | `unknown` | `imm5` | Is an element size specifier, |
| `<index>` | `unknown` | `imm5` | For the "32-bit" variant: is the element index |
| `<index>` | `unknown` | `imm5` | For the "64-bit" variant: is the element index encoded in "imm5<4>". |
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |

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
- source: `umov_advsimd.xml`
</details>