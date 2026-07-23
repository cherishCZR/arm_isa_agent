## USMMLA
_ARM A64 Instruction_

**Title**: USMMLA -- A64 | **Class**: `sve` | **XML ID**: `usmmla_z_zzz`

**Architecture**: `FEAT_SVE && FEAT_I8MM` (FEAT_SVE && FEAT_I8MM)

**Summary**: Unsigned by signed 8-bit integer matrix multiply-accumulate to 32-bit integer

**Description**:
The unsigned by signed
integer matrix multiply-accumulate instruction multiplies
the 2×8 matrix of unsigned 8-bit integer values held in each 128-bit segment of
the first source vector by the 8×2 matrix of signed 8-bit integer values in the
corresponding segment of the second source vector. The resulting 2×2 widened 32-bit
integer matrix product is then destructively added to the 32-bit integer
matrix accumulator held in the corresponding segment of the addend and
destination vector. This is equivalent to performing an 8-way dot product
per destination element.

This instruction is unpredicated.

ID_AA64ZFR0_EL1.I8MM indicates whether this instruction is implemented.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: SM Policy: `SM_0_only`

### Variant: `SVE`
- **Assembly**: `USMMLA  <Zda>.S, <Zn>.B, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  13   9   4  |
|--------------------------------|
| 010 0010 1   10  0   Zm  10  0110 Zn  Zda |
```

#### Decode (A64.sve.sve_intx_constructive.sve_intx_mmla.usmmla_z_zzz_)

```
if !IsFeatureImplemented(FEAT_SVE) || !IsFeatureImplemented(FEAT_I8MM) then
    EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
constant boolean op1_unsigned = TRUE;
constant boolean op2_unsigned = FALSE;
```

#### Execute (A64.sve.sve_intx_constructive.sve_intx_mmla.usmmla_z_zzz_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer segments = VL DIV 128;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result = Zeros(VL);
bits(128) op1, op2;
bits(128) res, addend;

for s = 0 to segments-1
    op1    = Elem[operand1, s, 128];
    op2    = Elem[operand2, s, 128];
    addend = Elem[operand3, s, 128];
    res    = MatMulAdd(addend, op1, op2, op1_unsigned, op2_unsigned);
    Elem[result, s, 128] = res;

Z[da, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) && IsFeatureImplemented(FEAT_I8MM)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

### Operational Notes

If PSTATE.DIT is 1:
        
          
            The execution time of this instruction is independent of:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
          
            The response of this instruction to asynchronous exceptions does not vary based on:
                
                  The values of the data supplied in any of its registers.
                
                
                  The values of the NZCV flags.
                
              
            
          
        
        This instruction might be immediately preceded in program order by a MOVPRFX instruction. The MOVPRFX must conform to all of the following requirements, otherwise the behavior of the MOVPRFX and this instruction is CONSTRAINED UNPREDICTABLE:
        
          
            The MOVPRFX must be unpredicated.
          
          
            The MOVPRFX must specify the same destination register as this instruction.
          
          
            The destination register must not refer to architectural register state referenced by any other source operand register of this instruction.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `usmmla_z_zzz.xml`
</details>