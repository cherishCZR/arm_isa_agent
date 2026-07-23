## SHRN
_ARM A64 Instruction_

**Title**: SHRN, SHRN2 -- A64 | **Class**: `advsimd` | **XML ID**: `SHRN_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Shift right narrow (immediate)

**Description**:
This instruction reads
each unsigned integer value from the
source SIMD&FP register,
right shifts each result by an immediate value,
puts the final result into a vector,
and writes the
vector to the lower or upper half of the
destination SIMD&FP register.
The destination vector elements are half as long as the source vector elements.
The results are truncated. For rounded results, see
RSHRN.

The SHRN instruction writes the vector
to the lower half of the
destination register and clears the upper half.
The SHRN2 instruction writes the vector
to the upper half of the
destination register without affecting the other bits of the register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Vector`
- **Assembly**: `SHRN{2}  <Vd>.<Tb>, <Vn>.<Ta>, #<shift>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  22  18  15  11 10  9   4  |
|-----------------------------------------|
| 0   Q   0   0   111 10  ?   immb 1000 0   1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdshf.SHRN_asimdshf_N)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if immh == '0000' then SEE(asimdimm);
if immh<3> == '1' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 8 << HighestSetBitNZ(immh<2:0>);
constant integer datasize = 64;
constant integer part = UInt(Q);
constant integer elements = datasize DIV esize;

constant integer shift = (2 * esize) - UInt(immh:immb);
constant boolean round = FALSE;
```

#### Execute (A64.simd_dp.asimdshf.SHRN_asimdshf_N)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize*2) operand = V[n, datasize*2];
bits(datasize) result;
integer element;

for e = 0 to elements-1
    element = RShr(UInt(Elem[operand, e, 2*esize]), shift, round);
    Elem[result, e, esize] = element<esize-1:0>;

Vpart[d, part, datasize] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `immh<3> != '1'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `2` | `unknown` | `Q` | Is the second and upper half specifier. If present it causes the operation to be performed on the upper 64 bits of the registers holding the narrower  |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Tb>` | `unknown` | `immh:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Ta>` | `unknown` | `immh` | Is an arrangement specifier, |
| `<shift>` | `shift` | `immh:immb` | Is the right shift amount, in the range 1 to the destination element width in bits, |

**2 Value Table**:

| bitfield | symbol |
|---|---|
| 0 | [absent] |
| 1 | [present] |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| x | RESERVED |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | 8H |
| 001x | 4S |
| 01xx | 2D |
| 1xxx | RESERVED |

**<shift> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | 16 - UInt(immh:immb) |
| 001x | 32 - UInt(immh:immb) |
| 01xx | 64 - UInt(immh:immb) |
| 1xxx | RESERVED |

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
- source: `shrn_advsimd.xml`
</details>