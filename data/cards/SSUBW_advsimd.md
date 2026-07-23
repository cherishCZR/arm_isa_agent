## SSUBW
_ARM A64 Instruction_

**Title**: SSUBW, SSUBW2 -- A64 | **Class**: `advsimd` | **XML ID**: `SSUBW_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Signed subtract wide

**Description**:
This instruction subtracts each vector element
in the lower or upper half of the
second source SIMD&FP register from the corresponding vector element
in the first
source SIMD&FP register,
places the result in a vector,
and writes the vector to the SIMD&FP destination register.
All the values in this instruction are signed integer values.

The SSUBW instruction extracts
the second source vector from the lower half
of the second source register. The SSUBW2 instruction extracts
the second source vector from the upper half
of the second source register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Three registers, not all the same type`
- **Assembly**: `SSUBW{2}  <Vd>.<Ta>, <Vn>.<Ta>, <Vm>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15  13 12 11   9   4  |
|-----------------------------------------------|
| 0   Q   0   0   111 0   size 1   Rm  00  1   1   00  Rn  Rd  |
```

#### Decode (A64.simd_dp.asimddiff.SSUBW_asimddiff_W)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if size == '11' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);

constant integer esize = 8 << UInt(size);
constant integer datasize = 64;
constant integer part = UInt(Q);
constant integer elements = datasize DIV esize;
```

#### Execute (A64.simd_dp.asimddiff.SSUBW_asimddiff_W)

```
CheckFPAdvSIMDEnabled64();
constant bits(2*datasize) operand1 = V[n, 2*datasize];
constant bits(datasize) operand2 = Vpart[m, part, datasize];
bits(2*datasize) result;
integer element1;
integer element2;
integer sum;

for e = 0 to elements-1
    element1 = SInt(Elem[operand1, e, 2*esize]);
    element2 = SInt(Elem[operand2, e, esize]);
    sum = element1 - element2;
    Elem[result, e, 2*esize] = sum<2*esize-1:0>;

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
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<Tb>` | `unknown` | `size:Q` | Is an arrangement specifier, |

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

- advsimd-reguse: `3reg-diff`
- advsimd-type: `simd`
- isa: `A64`
- source: `ssubw_advsimd.xml`
</details>