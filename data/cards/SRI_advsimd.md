## SRI
_ARM A64 Instruction_

**Title**: SRI -- A64 | **Class**: `advsimd` | **XML ID**: `SRI_advsimd`

**Architecture**: `FEAT_AdvSIMD` (ARMv8.0)

**Summary**: Shift right and insert (immediate)

**Description**:
This instruction reads
each vector element in the
source SIMD&FP
register,
right shifts each vector element by an immediate value, and
inserts the result into the corresponding vector element
in the destination SIMD&FP register such that the new zero bits created
by the shift are not inserted but retain their existing value.
Bits shifted out of the right of each vector element
of the source register are lost.



Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Scalar`
- **Assembly**: `SRI  D<d>, D<n>, #<shift>`
**Encoding Diagram (32-bit)**:

```text
| 31  29 28 27  24  22  18  15  10  9   4  |
|-----------------------------------|
| 01  1   1   111 10  1xxx immb 01000 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asisdshf.SRI_asisdshf_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if immh<3> != '1' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 8 << 3;
constant integer datasize = esize;
constant integer elements = 1;
constant integer shift = (esize * 2) - UInt(immh:immb);
```

#### Execute (A64.simd_dp.asisdshf.SRI_asisdshf_R)

```
CheckFPAdvSIMDEnabled64();
constant bits(datasize) operand  = V[n, datasize];
constant bits(datasize) operand2 = V[d, datasize];
constant bits(esize) mask = LSR(Ones(esize), shift);
bits(datasize) result;
bits(esize) shifted;

for e = 0 to elements-1
    shifted = LSR(Elem[operand, e, esize], shift);
    Elem[result, e, esize] = (Elem[operand2, e, esize] AND NOT(mask)) OR shifted;
V[d, datasize] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `immh<3> == '1'` |

### Variant: `Vector`
- **Assembly**: `SRI  <Vd>.<T>, <Vn>.<T>, #<shift>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  22  18  15  10  9   4  |
|--------------------------------------|
| 0   Q   1   0   111 10  ?   immb 01000 1   Rn  Rd  |
```

#### Decode (A64.simd_dp.asimdshf.SRI_asimdshf_R)

```
if !IsFeatureImplemented(FEAT_AdvSIMD) then EndOfDecode(Decode_UNDEF);
if immh == '0000' then SEE(asimdimm);
if immh<3>:Q == '10' then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer esize = 8 << HighestSetBitNZ(immh);
constant integer datasize = 64 << UInt(Q);
constant integer elements = datasize DIV esize;
constant integer shift = (esize * 2) - UInt(immh:immb);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `immh<3>:Q != '10'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<d>` | `register (64-bit)` | `Rd` | Is the number of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<n>` | `register (64-bit)` | `Rn` | Is the number of the SIMD&FP source register, encoded in the "Rn" field. |
| `<shift>` | `shift` | `immh:immb` | For the "Scalar" variant: is the right shift amount, in the range 1 to 64, encoded as 128 - UInt("immh:immb"). |
| `<shift>` | `shift` | `immh:immb` | For the "Vector" variant: is the right shift amount, in the range 1 to the element width in bits, |
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<T>` | `arrangement` | `immh:Q` | Is an arrangement specifier, |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the SIMD&FP source register, encoded in the "Rn" field. |

**<shift> Value Table**:

| bitfield | symbol |
|---|---|
| 0001 | 16 - UInt(immh:immb) |
| 001x | 32 - UInt(immh:immb) |
| 01xx | 64 - UInt(immh:immb) |
| 1xxx | 128 - UInt(immh:immb) |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | 8B |
| 1 | 16B |
| 0 | 4H |
| 1 | 8H |
| 0 | 2S |
| 1 | 4S |
| 0 | RESERVED |
| 1 | 2D |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_AdvSIMD)` |

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
- source: `sri_advsimd.xml`
</details>