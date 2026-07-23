## SMAXV
_ARM A64 Instruction_

**Title**: SMAXV -- A64 | **Class**: `advsimd` | **XML ID**: `SMAXV_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Signed maximum across vector

**Description**:
This instruction compares all the
vector elements in the source SIMD&FP register,
and writes the largest of the values
as a scalar to the destination SIMD&FP register.
All the values in this instruction are signed integer values.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Advanced SIMD`
- **Assembly**: `SMAXV  <V><d>, <Vn>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21  16 15  11   9   4  |
|-----------------------------------------|
| 0   Q   0   0   111 0   size 11000 0   1010 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdall.SMAXV_asimdall_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if size:Q == '100' then EndOfDecode(Decode_UNDEF);
if size == '11' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 8 << UInt(size);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;

constant boolean unsigned = FALSE;
```

#### Execute (A64.simd_dp.asimdall.SMAXV_asimdall_only)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = V[n, datasize];
integer max = Int(Elem[operand, 0, esize], unsigned);

for e = 1 to elements-1
    constant integer element = Int(Elem[operand, e, esize], unsigned);
    max = Max(max, element);

V[d, esize] = max<esize-1:0>;
```

#### Constraints
_2× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `size:Q != '100'` |
| 🚫 ENCODING_UNDEF | `size != '11'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<V>` | `register (128-bit)` | `size` | Is the destination width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<T>` | `arrangement` | `size:Q` | Is an arrangement specifier, |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | RESERVED |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |
| 0 | 4H |
| 1 | 8H |
| 0 | RESERVED |
| 1 | 4S |
| x | RESERVED |

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
- source: `smaxv_advsimd.xml`
</details>