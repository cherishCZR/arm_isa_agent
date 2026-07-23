## SRI
_ARM A64 Instruction_

**Title**: SRI -- A64 | **Class**: `sve2` | **XML ID**: `sri_z_zzi`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Shift right and insert (immediate)

**Description**:
Shift each source vector element right by an immediate value, and insert
the result into the corresponding vector element in the destination
vector register, merging the shifted bits from each source element with
existing bits in each destination vector element. The immediate shift amount is an unsigned value in the range 1
to number of bits per element. This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `SRI  <Zd>.<T>, <Zn>.<T>, #<const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15  13  10  9   4  |
|--------------------------------------|
| 010 0010 1   tszh 0   tszl imm3 11  110 0   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_acc.sve_intx_shift_insert.sri_z_zzi_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant bits(4) tsize = tszh:tszl;
if tsize == '0000' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << HighestSetBit(tsize);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer shift = (2 * esize) - UInt(tsize:imm3);
```

#### Execute (A64.sve.sve_intx_acc.sve_intx_shift_insert.sri_z_zzi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand = Z[n, VL];
bits(VL) result = Z[d, VL];

for e = 0 to elements-1
    constant bits(esize) element1 = Elem[result, e, esize];
    constant bits(esize) element2 = Elem[operand, e, esize];
    constant bits(esize) mask = LSR(Ones(esize), shift);
    constant bits(esize) shiftedval = LSR(element2, shift);
    Elem[result, e, esize] = (element1 AND (NOT mask)) OR shiftedval;

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `tszh:tszl != '0000'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `arrangement` | `tszh:tszl` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<const>` | `unknown` | `tszh:tszl:imm3` | Is the immediate shift amount, in the range 1 to number of bits per element, encoded in "tszh:tszl:imm3". |

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
- source: `sri_z_zzi.xml`
</details>