## DUP
_ARM A64 Instruction_

**Title**: DUP (element) -- A64 | **Class**: `advsimd` | **XML ID**: `DUP_advsimd_elt`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Duplicate vector element to vector or scalar

**Description**:
This instruction duplicates the vector element at the specified element index
in the source SIMD&FP register
into a scalar or each element in a vector,
and writes the result to the destination SIMD&FP register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Scalar`
- **Assembly**: `DUP  <V><d>, <Vn>.<T>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24  22  20  15 14  10  9   4  |
|--------------------------------------|
| 01  0   1   111 00  00  imm5 0   0000 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdone.DUP_asisdone_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if imm5 IN 'x0000' then EndOfDecode(Decode_UNDEF);
constant integer size = LowestSetBitNZ(imm5<3:0>);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer index = UInt(imm5<4:size+1>);
constant integer idxdsize = 64 << UInt(imm5<4>);
constant integer esize = 8 << size;
constant integer datasize = esize;
constant integer elements = 1;
```

#### Execute (A64.simd_dp.asisdone.DUP_asisdone_only)

```
CheckFPAdvSIMDEnabled64();
constant bits(idxdsize) operand = V[n, idxdsize];
bits(datasize) result;
bits(esize) element;

element = Elem[operand, index, esize];
for e = 0 to elements-1
    Elem[result, e, esize] = element;
V[d, datasize] = result;
```

### Variant: `Vector`
- **Assembly**: `DUP  <Vd>.<T>, <Vn>.<Ts>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  22  20  15 14  10  9   4  |
|-----------------------------------------|
| 0   Q   0   0   111 00  00  imm5 0   0000 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdins.DUP_asimdins_DV_v)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if imm5 IN 'x0000' then EndOfDecode(Decode_UNDEF);
if imm5 IN 'x1000' && Q == '0' then EndOfDecode(Decode_UNDEF);
constant integer size = LowestSetBitNZ(imm5<3:0>);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer index = UInt(imm5<4:size+1>);
constant integer idxdsize = 64 << UInt(imm5<4>);
constant integer esize = 8 << size;
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `imm5 NOT IN 'x1000' \|\| Q != '0'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<V>` | `register (128-bit)` | `imm5` | Is the destination width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<T>` | `unknown` | `imm5` | For the "Scalar" variant: is the element width specifier, |
| `<T>` | `arrangement` | `imm5:Q` | For the "Vector" variant: is an arrangement specifier, |
| `<index>` | `unknown` | `imm5` | Is the element index |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ts>` | `unknown` | `imm5` | Is an element size specifier, |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | B |
| xxx10 | H |
| xx100 | S |
| x1000 | D |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | B |
| xxx10 | H |
| xx100 | S |
| x1000 | D |

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

**<index> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | UInt(imm5<4:1>) |
| xxx10 | UInt(imm5<4:2>) |
| xx100 | UInt(imm5<4:3>) |
| x1000 | UInt(imm5<4>) |

**<Ts> Value Table**:

| bitfield | symbol |
|---|---|
| x0000 | RESERVED |
| xxxx1 | B |
| xxx10 | H |
| xx100 | S |
| x1000 | D |

### Encoding Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `imm5 NOT IN 'x0000'` |

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
- source: `dup_advsimd_elt.xml`
</details>