## MUL
_ARM A64 Instruction_

**Title**: MUL (by element) -- A64 | **Class**: `advsimd` | **XML ID**: `MUL_advsimd_elt`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Multiply (vector, by element)

**Description**:
This instruction
multiplies the vector elements
in the first source SIMD&FP register by the specified
value in the second source SIMD&FP register,
places the results in a vector, and
writes the vector to the destination SIMD&FP register.
All the values in this instruction are unsigned integer values.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Vector`
- **Assembly**: `MUL  <Vd>.<T>, <Vn>.<T>, <Vm>.<Ts>[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20 19  15  11 10  9   4  |
|-----------------------------------------------|
| 0   Q   0   0   111 1   size L   M   Rm  1000 H   0   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdelem.MUL_asimdelem_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
constant integer idxdsize = 64 << UInt(H);
integer index;
bit Rmhi;
case size of
    when '01' index = UInt(H:L:M); Rmhi = '0';
    when '10' index = UInt(H:L);   Rmhi = M;
    otherwise EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rmhi:Rm);
constant integer esize = 8 << UInt(size);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
```

#### Execute (A64.simd_dp.asimdelem.MUL_asimdelem_R)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(idxdsize) operand2 = V[m, idxdsize];
bits(datasize) result;
integer element1;
integer element2;
bits(esize) product;

element2 = UInt(Elem[operand2, index, esize]);
for e = 0 to elements-1
    element1 = UInt(Elem[operand1, e, esize]);
    product = (element1 * element2)<esize-1:0>;
    Elem[result, e, esize] = product;

V[d, datasize] = result;
```

#### Constraints
_1× ↩ DECODE_FALLBACK / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| ↩ DECODE_FALLBACK | `matching encodings` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `arrangement` | `size:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `size:M:Rm` | Is the name of the second SIMD&FP source register, |
| `<Ts>` | `unknown` | `size` | Is an element size specifier, |
| `<index>` | `unknown` | `size:H:L:M` | Is the element index, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| x | RESERVED |
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| x | RESERVED |

**<Vm> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | UInt('0':Rm) |
| 10 | UInt(M:Rm) |
| 11 | RESERVED |

**<Ts> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | RESERVED |

**<index> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | UInt(H:L:M) |
| 10 | UInt(H:L) |
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

- advsimd-reguse: `2reg-element`
- isa: `A64`
- source: `mul_advsimd_elt.xml`
</details>