## UDOT
_ARM A64 Instruction_

**Title**: UDOT (by element) -- A64 | **Class**: `advsimd` | **XML ID**: `UDOT_advsimd_elt`

**Architecture**: `FEAT_DotProd` (ARMv8.4)

**Summary**: Dot product unsigned arithmetic (vector, by element)

**Description**:
This instruction
performs the dot product of the four 8-bit elements in each 32-bit element of
the first source register with the four 8-bit elements of an indexed 32-bit
element in the second source register, accumulating the result into the
corresponding 32-bit element of the destination register.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

In Armv8.2 and Armv8.3, this is an OPTIONAL instruction.
From Armv8.4 it is mandatory for all implementations to support it.

### Variant: `Vector`
- **Assembly**: `UDOT  <Vd>.<Ta>, <Vn>.<Tb>, <Vm>.4B[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20 19  15  11 10  9   4  |
|-----------------------------------------------|
| 0   Q   1   0   111 1   size L   M   Rm  1110 H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdelem.UDOT_asimdelem_D)

```
if !IsFeatureImplemented(FEAT_DotProd) then EndOfDecode(Decode_UNDEF);
if size  != '10' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(M:Rm);
constant integer index = UInt(H:L);

constant integer esize = 8 << UInt(size);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
```

#### Execute (A64.simd_dp.asimdelem.UDOT_asimdelem_D)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(128) operand2 = V[m, 128];
bits(datasize) result = V[d, datasize];
for e = 0 to elements-1
    integer res = 0;
    integer element1, element2;
    for i = 0 to 3
        element1 = UInt(Elem[operand1, 4 * e + i, esize DIV 4]);
        element2 = UInt(Elem[operand2, 4 * index + i, esize DIV 4]);

        res = res + element1 * element2;
    Elem[result, e, esize] = Elem[result, e, esize] + res;
V[d, datasize] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_DotProd)` |
| 🚫 ENCODING_UNDEF | `size == '10'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP third source and destination register, encoded in the "Rd" field. |
| `<Ta>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Tb>` | `unknown` | `Q` | Is an arrangement specifier, |
| `<Vm>` | `register (128-bit)` | `M:Rm` | Is the name of the second SIMD&FP source register, encoded in the "M:Rm" fields. |
| `<index>` | `unknown` | `H:L` | Is the element index, encoded in the "H:L" fields. |

**<Ta> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 2S |
| 1 | 4S |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |

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

- advsimd-reguse: `2reg-element`
- isa: `A64`
- source: `udot_advsimd_elt.xml`
</details>