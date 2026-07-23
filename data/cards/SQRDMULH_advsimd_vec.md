## SQRDMULH
_ARM A64 Instruction_

**Title**: SQRDMULH (vector) -- A64 | **Class**: `advsimd` | **XML ID**: `SQRDMULH_advsimd_vec`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Signed saturating rounding doubling multiply returning high half

**Description**:
This instruction multiplies the values of corresponding elements of
the two source SIMD&FP registers,
doubles the results, places the most significant half of the final results into a vector,
and writes the vector to the destination
SIMD&FP register.

The results are
rounded. For truncated results, see SQDMULH.

If overflow occurs with any of the results, those results are saturated. If saturation occurs,
the cumulative saturation bit
FPSR.QC is set.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Scalar`
- **Assembly**: `SQRDMULH  <V><d>, <V><n>, <V><m>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24 23  21 20  15  10  9   4  |
|--------------------------------------|
| 01  1   1   111 0   size 1   Rm  10110 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdsame.SQRDMULH_asisdsame_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if size == '11' || size == '00' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 8 << UInt(size);
constant integer datasize = esize;
constant integer elements = 1;
constant boolean rounding = TRUE;
```

#### Execute (A64.simd_dp.asisdsame.SQRDMULH_asisdsame_only)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand1 = V[n, datasize];
constant bits(datasize) operand2 = V[m, datasize];
bits(datasize) result;
integer element1;
integer element2;
integer product;
boolean sat;

for e = 0 to elements-1
    element1 = SInt(Elem[operand1, e, esize]);
    element2 = SInt(Elem[operand2, e, esize]);
    product = 2 * element1 * element2;
    product = RShr(product, esize, rounding);
    (Elem[result, e, esize], sat) = SignedSatQ(product, esize);
    if sat then FPSR.QC = '1';

V[d, datasize] = result;
```

### Variant: `Vector`
- **Assembly**: `SQRDMULH  <Vd>.<T>, <Vn>.<T>, <Vm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24 23  21 20  15  10  9   4  |
|-----------------------------------------|
| 0   Q   1   0   111 0   size 1   Rm  10110 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdsame.SQRDMULH_asimdsame_only)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if size == '11' || size == '00' then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer esize = 8 << UInt(size);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
constant boolean rounding = TRUE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<V>` | `register (128-bit)` | `size` | Is a width specifier, |
| `<d>` | `unknown` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<n>` | `unknown` | `Rn` | Is the number of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<m>` | `unknown` | `Rm` | Is the number of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `arrangement` | `size:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

**<V> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | RESERVED |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| x | RESERVED |
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| x | RESERVED |

### Encoding Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |
| 🚫 ENCODING_UNDEF | `size != '11' && size != '00'` |

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
- source: `sqrdmulh_advsimd_vec.xml`
</details>