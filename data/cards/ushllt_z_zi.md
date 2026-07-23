## USHLLT
_ARM A64 Instruction_

**Title**: USHLLT -- A64 | **Class**: `sve2` | **XML ID**: `ushllt_z_zi`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Unsigned shift left long by immediate (top)

**Description**:
Shift left by immediate each odd-numbered unsigned element of the source
vector, and place the results in the overlapping double-width elements of the
destination vector.
The immediate shift amount is an unsigned value in the range 0
to number of bits per element minus 1.
This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `USHLLT  <Zd>.<T>, <Zn>.<Tb>, #<const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  15  13  11 10  9   4  |
|--------------------------------------------|
| 010 0010 1   0   tszh 0   tszl imm3 10  10  1   1   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_constructive.sve_intx_shift_long.ushllt_z_zi_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant bits(3) tsize = tszh:tszl;
if tsize == '000' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << HighestSetBit(tsize);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer shift = UInt(tsize:imm3) - esize;
```

#### Execute (A64.sve.sve_intx_constructive.sve_intx_shift_long.ushllt_z_zi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV (2 * esize);
constant bits(VL) operand = Z[n, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(esize) element = Elem[operand, 2*e + 1, esize];
    constant integer shifted_value = UInt(element) << shift;
    Elem[result, e, 2*esize] = shifted_value<2*esize-1:0>;

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `tszh:tszl != '000'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `arrangement` | `tszh:tszl` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<Tb>` | `unknown` | `tszh:tszl` | Is the size specifier, |
| `<const>` | `unknown` | `tszh:tszl:imm3` | Is the immediate shift amount, in the range 0 to number of bits per element minus 1, encoded in "tszh:tszl:imm3". |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 1x | S |
| xx | D |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | B |
| 1x | H |
| xx | S |

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
- source: `ushllt_z_zi.xml`
</details>