## RSHRNT
_ARM A64 Instruction_

**Title**: RSHRNT -- A64 | **Class**: `sve2` | **XML ID**: `rshrnt_z_zi`

**Architecture**: `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Rounding shift right narrow by immediate (top)

**Description**:
Shift each unsigned integer value in the source
vector elements right by an immediate value, and place the rounded results in
the odd-numbered half-width destination elements, leaving the even-numbered
elements unchanged.
The immediate shift amount is an unsigned value in the range 1
to number of bits per element.
This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `RSHRNT  <Zd>.<T>, <Zn>.<Tb>, #<const>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23 22 21 20  18  15 14 13 12 11 10  9   4  |
|--------------------------------------------------|
| 010 0010 1   0   tszh 1   tszl imm3 0   0   0   1   1   1   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_narrowing.sve_intx_shift_narrow.rshrnt_z_zi_)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant bits(3) tsize = tszh:tszl;
if tsize == '000' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << HighestSetBit(tsize);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant integer shift = (2 * esize) - UInt(tsize:imm3);
```

#### Execute (A64.sve.sve_intx_narrowing.sve_intx_shift_narrow.rshrnt_z_zi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV (2 * esize);
constant bits(VL) operand = Z[n, VL];
bits(VL) result = Z[d, VL];
for e = 0 to elements-1
    constant bits(2*esize) element = Elem[operand, e, 2*esize];
    constant integer res = (UInt(element) + (1 << (shift-1))) >> shift;
    Elem[result, 2*e + 1, esize] = res<esize-1:0>;

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
| `<const>` | `unknown` | `tszh:tszl:imm3` | Is the immediate shift amount, in the range 1 to number of bits per element, encoded in "tszh:tszl:imm3". |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | B |
| 1x | H |
| xx | S |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 1x | S |
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
- source: `rshrnt_z_zi.xml`
</details>