## UABALT
_ARM A64 Instruction_

**Title**: UABALT -- A64 | **Class**: `sve2` | **XML ID**: `uabalt_z_zzz`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Unsigned absolute difference and accumulate long (top)

**Description**:
Compute the absolute difference between odd-numbered unsigned
elements of the second source vector and corresponding
elements of the first source vector, and destructively add to
the overlapping double-width elements of the addend vector.
This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `UABALT  <Zda>.<T>, <Zn>.<Tb>, <Zm>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  13  11 10  9   4  |
|--------------------------------------|
| 010 0010 1   size 0   Zm  11  00  1   1   Zn  Zda |
```

#### Decode (A64.sve.sve_intx_acc.sve_intx_aba_long.uabalt_z_zzz_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

#### Execute (A64.sve.sve_intx_acc.sve_intx_aba_long.uabalt_z_zzz_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result = Z[da, VL];

for e = 0 to elements-1
    constant integer element1 = UInt(Elem[operand1, 2*e + 1, esize DIV 2]);
    constant integer element2 = UInt(Elem[operand2, 2*e + 1, esize DIV 2]);
    constant bits(esize) absdiff = Abs(element1 - element2)<esize-1:0>;
    Elem[result, e, esize] = Elem[result, e, esize] + absdiff;

Z[da, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Tb>` | `unknown` | `size` | Is the size specifier, |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | B |
| 10 | H |
| 11 | S |

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
- source: `uabalt_z_zzz.xml`
</details>