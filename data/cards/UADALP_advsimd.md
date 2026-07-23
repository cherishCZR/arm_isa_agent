## UADALP
_ARM A64 Instruction_

**Title**: UADALP -- A64 | **Class**: `advsimd` | **XML ID**: `UADALP_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Unsigned add and accumulate long pairwise

**Description**:
This instruction adds pairs of adjacent unsigned integer values from the vector
in the source SIMD&FP register
and accumulates the
results with the vector elements of the destination
SIMD&FP register.
The destination vector elements are twice
as long as the source vector elements.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Vector`
- **Assembly**: `UADALP  <Vd>.<Ta>, <Vn>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21  16  14 13  11   9   4  |
|--------------------------------------------|
| 0   Q   1   0   111 0   size 10000 00  1   10  10  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdmisc.UADALP_asimdmisc_P)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if size == '11' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);

constant integer esize = 8 << UInt(size);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV (2 * esize);
```

#### Execute (A64.simd_dp.asimdmisc.UADALP_asimdmisc_P)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand = V[n, datasize];
bits(datasize) result  = V[d, datasize];

bits(2*esize) sum;
integer op1;
integer op2;

for e = 0 to elements-1
    op1 = UInt(Elem[operand, 2*e+0, esize]);
    op2 = UInt(Elem[operand, 2*e+1, esize]);
    sum = (op1+op2)<2*esize-1:0>;
    Elem[result, e, 2*esize] = Elem[result, e, 2*esize] + sum;

V[d, datasize] = result;
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
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `size:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |
| `<Tb>` | `unknown` | `size:Q` | Is an arrangement specifier, |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| 0 | 1D |
| 1 | 2D |
| x | RESERVED |

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
- source: `uadalp_advsimd.xml`
</details>