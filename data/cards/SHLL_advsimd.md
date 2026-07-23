## SHLL
_ARM A64 Instruction_

**Title**: SHLL, SHLL2 -- A64 | **Class**: `advsimd` | **XML ID**: `SHLL_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Shift left long (by element size)

**Description**:
This instruction reads
each vector element in the lower or upper half of the
 source SIMD&FP
register,
left shifts each result by the element size,
writes the final result to a vector,
and writes the
vector to the
destination SIMD&FP register.
The destination vector elements are twice
as long as the source vector elements.

The SHLL instruction extracts
vector elements from the lower half
of the source register. The SHLL2 instruction extracts
vector elements from the upper half
of the source register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Vector`
- **Assembly**: `SHLL{2}  <Vd>.<Ta>, <Vn>.<Tb>, #<shift>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21  16  11   9   4  |
|--------------------------------------|
| 0   Q   1   0   111 0   size 10000 10011 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.SHLL_asimdmisc_S)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

if size == '11' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer datasize = 64;
constant integer part = UInt(Q);
constant integer elements = datasize DIV esize;

constant integer shift = esize;
```

#### Execute (A64.simd_dp.asimdmisc.SHLL_asimdmisc_S)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = Vpart[n, part, datasize];
bits(2*datasize) result;
integer element;

for e = 0 to elements-1
    element = SInt(Elem[operand, e, esize]) << shift;
    Elem[result, e, 2*esize] = element<2*esize-1:0>;

V[d, 2*datasize] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `size != '11'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `2` | `unknown` | `Q` | Is the second and upper half specifier. If present it causes the operation to be performed on the upper 64 bits of the registers holding the narrower  |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `size` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Tb>` | `unknown` | `size:Q` | Is an arrangement specifier, |
| `<shift>` | `shift` | `size` | Is the left shift amount, which must be equal to the source element width in bits, |

**2 Value Table**:

| bitfield | symbol |
|---|---|
| 0 | [absent] |
| 1 | [present] |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | 8H |
| 01 | 4S |
| 10 | 2D |
| 11 | RESERVED |

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
| 00 | 8 |
| 01 | 16 |
| 10 | 32 |
| 11 | RESERVED |

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
- source: `shll_advsimd.xml`
</details>