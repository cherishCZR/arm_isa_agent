## DUP
_ARM A64 Instruction_

**Title**: DUP (general) -- A64 | **Class**: `advsimd` | **XML ID**: `DUP_advsimd_gen`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Duplicate general-purpose register to vector

**Description**:
This instruction duplicates the contents of the
source general-purpose register
into a scalar or each element in a vector,
and writes the result to the SIMD&FP destination register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Advanced SIMD`
- **Assembly**: `DUP  <Vd>.<T>, <R><n>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  22  20  15 14  10  9   4  |
|-----------------------------------------|
| 0   Q   0   0   111 00  00  imm5 0   0001 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdins.DUP_asimdins_DR_r)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if imm5 IN 'x0000' then EndOfDecode(Decode_UNDEF);
if imm5 IN 'x1000' && Q == '0' then EndOfDecode(Decode_UNDEF);
constant integer size = LowestSetBitNZ(imm5<3:0>);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
// imm5<4:size+1> is IGNORED
constant integer esize = 8 << size;
constant integer datasize = 64 << UInt(Q);
```

#### Execute (A64.simd_dp.asimdins.DUP_asimdins_DR_r)

```
CheckFPAdvSIMDEnabled64();
constant bits(esize) element = X[n, esize];
constant integer elements = datasize DIV esize;
bits(datasize) result;

for e = 0 to elements-1
    Elem[result, e, esize] = element;
V[d, datasize] = result;
```

#### Constraints
_2× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `imm5 NOT IN 'x0000'` |
| 🚫 ENCODING_UNDEF | `imm5 NOT IN 'x1000' \|\| Q != '0'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `arrangement` | `imm5:Q` | Is an arrangement specifier, |
| `<R>` | `unknown` | `imm5` | Is the width specifier for the general-purpose source register, |
| `<n>` | `unknown` | `Rn` | Is the number [0-30] of the general-purpose source register or ZR (31), encoded in the "Rn" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| x | RESERVED |
| 0 | 8B |
| 1 | 16B |
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| 0 | RESERVED |
| 1 | 2D |

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
- source: `dup_advsimd_gen.xml`
</details>