## USDOT
_ARM A64 Instruction_

**Title**: USDOT (indexed) -- A64 | **Class**: `sve` | **XML ID**: `usdot_z_zzzi`

**Architecture**: `(FEAT_SVE || FEAT_SME) && FEAT_I8MM` ((FEAT_SVE || FEAT_SME) && FEAT_I8MM)

**Summary**: Unsigned by signed 8-bit integer indexed dot product to 32-bit integer

**Description**:
The unsigned by signed integer indexed dot
product instruction computes the dot product of a group of four unsigned
8-bit  integer values held in each 32-bit  element of the first source
vector multiplied by a group of four signed 8-bit  integer values in
an indexed 32-bit  element of the
second source vector, and then destructively adds the widened dot product to
the corresponding 32-bit  element of the destination vector.

The groups within the second source vector are specified using
an immediate index which selects the same group position within
each 128-bit vector segment.  The index range is from 0 to
3.

This instruction is unpredicated.

ID_AA64ZFR0_EL1.I8MM indicates whether this instruction is implemented.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `USDOT  <Zda>.S, <Zn>.B, <Zm>.B[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  10  9   4  |
|-----------------------------------|
| 010 0010 0   10  1   i2  Zm  00011 0   Zn  Zda |
```

#### Decode (A64.sve.sve_intx_by_indexed_elem.sve_intx_mixed_dot_by_indexed_elem.usdot_z_zzzi_s)

```
if ((!IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME)) ||
    !IsFeatureImplemented(FEAT_I8MM)) then EndOfDecode(Decode_UNDEF);
constant integer esize = 32;
constant integer index = UInt(i2);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer da = UInt(Zda);
```

#### Execute (A64.sve.sve_intx_by_indexed_elem.sve_intx_mixed_dot_by_indexed_elem.usdot_z_zzzi_s)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer eltspersegment = 128 DIV esize;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
constant bits(VL) operand3 = Z[da, VL];
bits(VL) result;

for e = 0 to elements-1
    constant integer segmentbase = e - (e MOD eltspersegment);
    constant integer s = segmentbase + index;
    bits(esize) res = Elem[operand3, e, esize];
    for i = 0 to 3
        constant integer element1 = UInt(Elem[operand1, 4 * e + i, esize DIV 4]);
        constant integer element2 = SInt(Elem[operand2, 4 * s + i, esize DIV 4]);
        res = res + element1 * element2;
    Elem[result, e, esize] = res;

Z[da, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `((IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)) && IsFeatureImplemented(FEAT_I8MM))` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zda>` | `register (128-bit)` | `Zda` | Is the name of the third source and destination scalable vector register, encoded in the "Zda" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register Z0-Z7, encoded in the "Zm" field. |
| `<imm>` | `immediate` | `i2` | Is the immediate index of a 32-bit group of four 8-bit values within each 128-bit vector segment, in the range 0 to 3, encoded in the "i2" field. |

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
- source: `usdot_z_zzzi.xml`
</details>