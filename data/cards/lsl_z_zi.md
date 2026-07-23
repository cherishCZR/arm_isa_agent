## LSL
_ARM A64 Instruction_

**Title**: LSL (immediate, unpredicated) -- A64 | **Class**: `sve` | **XML ID**: `lsl_z_zi`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Logical shift left by immediate (unpredicated)

**Description**:
Shift left by immediate each element of the source vector,
and place the results in the corresponding elements of the destination vector.
The immediate shift amount is an unsigned value in the range 0
to number of bits per element minus 1. This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `LSL  <Zd>.<T>, <Zn>.<T>, #<const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  12 11   9   4  |
|--------------------------------------|
| 000 0010 0   tszh 1   tszl imm3 100 1   11  Zn  Zd  |
```

#### Decode (A64.sve.sve_int_unpred_shift.sve_int_bin_cons_shift_b.lsl_z_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant bits(4) tsize = tszh:tszl;
if tsize == '0000' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << HighestSetBit(tsize);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer shift = UInt(tsize:imm3) - esize;
```

#### Execute (A64.sve.sve_int_unpred_shift.sve_int_bin_cons_shift_b.lsl_z_zi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = Z[n, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(esize) element1 = Elem[operand1, e, esize];
    Elem[result, e, esize] = LSL(element1, shift);

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `tszh:tszl != '0000'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `arrangement` | `tszh:tszl` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<const>` | `unknown` | `tszh:tszl:imm3` | Is the immediate shift amount, in the range 0 to number of bits per element minus 1, encoded in "tszh:tszl:imm3". |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | B |
| 1x | H |
| xx | S |
| xx | D |

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
- source: `lsl_z_zi.xml`
</details>