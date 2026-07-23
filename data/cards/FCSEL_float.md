## FCSEL
_ARM A64 Instruction_

**Title**: FCSEL -- A64 | **Class**: `float` | **XML ID**: `FCSEL_float`

**Summary**: Floating-point conditional select (scalar)

**Description**:
This instruction allows the SIMD&FP destination register to
take the value from either one or the other of two
SIMD&FP source registers. If the condition passes,
the first SIMD&FP source register value is taken, otherwise
the second SIMD&FP source register value is taken.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Floating-point (FCSEL_H_floatsel)` (Half-precision)
- **Condition**: `ftype == 11`
- **Assembly**: `FCSEL  <Hd>, <Hn>, <Hm>, <cond>`
- **Fixed bits**: `ftype`=`11`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  11   9   4  |
|-----------------------------------|
| 0   0   0   11110 ftype 1   Rm  cond 11  Rn  Rd  |
```

#### Decode (A64.simd_dp.floatsel.FCSEL_H_floatsel)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
if ftype == '10' then EndOfDecode(Decode_UNDEF);
if ftype == '11' && !IsFeatureImplemented(FEAT_FP16) then EndOfDecode(Decode_UNDEF);

constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);

constant integer datasize = 8 << UInt(ftype EOR '10');
constant bits(4) condition = cond;
```

#### Execute (A64.simd_dp.floatsel.FCSEL_H_floatsel)

```
CheckFPEnabled64();
bits(datasize) result;

constant boolean condition_holds = ConditionHolds(condition);
result = if condition_holds then V[n, datasize] else V[m, datasize];

V[d, datasize] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 2× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |
| 🚫 ENCODING_UNDEF | `ftype != '10'` |
| 🔒 FEATURE_GATE | `ftype != '11' \|\| IsFeatureImplemented(FEAT_FP16)` |

### Variant: `Floating-point (FCSEL_S_floatsel)` (Single-precision)
- **Condition**: `ftype == 00`
- **Assembly**: `FCSEL  <Sd>, <Sn>, <Sm>, <cond>`
- **Fixed bits**: `ftype`=`00`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  11   9   4  |
|-----------------------------------|
| 0   0   0   11110 ftype 1   Rm  cond 11  Rn  Rd  |
```

### Variant: `Floating-point (FCSEL_D_floatsel)` (Double-precision)
- **Condition**: `ftype == 01`
- **Assembly**: `FCSEL  <Dd>, <Dn>, <Dm>, <cond>`
- **Fixed bits**: `ftype`=`01`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28  23  21 20  15  11   9   4  |
|-----------------------------------|
| 0   0   0   11110 ftype 1   Rm  cond 11  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Hd>` | `register (16-bit)` | `Rd` | Is the 16-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Hn>` | `register (16-bit)` | `Rn` | Is the 16-bit name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Hm>` | `register (16-bit)` | `Rm` | Is the 16-bit name of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<cond>` | `condition` | `cond` | Is one of the standard conditions, encoded in the standard way, and |
| `<Sd>` | `register (32-bit)` | `Rd` | Is the 32-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Sm>` | `register (32-bit)` | `Rm` | Is the 32-bit name of the second SIMD&FP source register, encoded in the "Rm" field. |
| `<Dd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Dn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Dm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second SIMD&FP source register, encoded in the "Rm" field. |

**<cond> Value Table**:

| bitfield | symbol |
|---|---|
| 0000 | EQ |
| 0001 | NE |
| 0010 | CS |
| 0011 | CC |
| 0100 | MI |
| 0101 | PL |
| 0110 | VS |
| 0111 | VC |
| 1000 | HI |
| 1001 | LS |
| 1010 | GE |
| 1011 | LT |
| 1100 | GT |
| 1101 | LE |
| 1110 | AL |
| 1111 | NV |

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
- source: `fcsel_float.xml`
</details>