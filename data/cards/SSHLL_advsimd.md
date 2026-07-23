## SSHLL
_ARM A64 Instruction_

**Title**: SSHLL, SSHLL2 -- A64 | **Class**: `advsimd` | **XML ID**: `SSHLL_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Signed shift left long (immediate)

**Description**:
This instruction reads each vector element
from the source SIMD&FP register,
left shifts each vector element by the specified shift amount,
places the result into a vector,
and writes
the vector to the destination SIMD&FP
register.
The destination vector elements are twice
as long as the source vector elements.
All the values in this instruction are signed integer values.

The SSHLL instruction extracts
vector elements from the lower half
of the source register. The SSHLL2 instruction extracts
vector elements from the upper half
of the source register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Vector`
- **Assembly**: `SSHLL{2}  <Vd>.<Ta>, <Vn>.<Tb>, #<shift>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  22  18  15  10  9   4  |
|--------------------------------------|
| 0   Q   0   0   111 10  ?   immb 10100 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdshf.SSHLL_asimdshf_L)

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

constant integer shift = UInt(immh:immb) - esize;
constant boolean unsigned = FALSE;
```

#### Execute (A64.simd_dp.asimdshf.SSHLL_asimdshf_L)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = Vpart[n, part, datasize];
bits(datasize*2) result;
integer element;

for e = 0 to elements-1
    element = Int(Elem[operand, e, esize], unsigned) << shift;
    Elem[result, e, 2*esize] = element<2*esize-1:0>;

V[d, datasize*2] = result;
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
| `<Ta>` | `unknown` | `immh` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Tb>` | `unknown` | `immh:Q` | Is an arrangement specifier, |
| `<shift>` | `shift` | `immh:immb` | Is the left shift amount, in the range 0 to the source element width in bits minus 1, |

**2 Value Table**:

| bitfield | symbol |
|---|---|
| 0 | [absent] |
| 1 | [present] |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | 8H |
| 001x | 4S |
| 01xx | 2D |
| 1xxx | RESERVED |

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

**<shift> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | UInt(immh:immb) - 8 |
| 001x | UInt(immh:immb) - 16 |
| 01xx | UInt(immh:immb) - 32 |
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
- source: `sshll_advsimd.xml`
</details>