## DUPQ
_ARM A64 Instruction_

**Title**: DUPQ -- A64 | **Class**: `sve2` | **XML ID**: `dupq_z_zi`

**Architecture**: `FEAT_SVE2p1 || FEAT_SME2p1` (FEAT_SVE2p1 || FEAT_SME2p1)

**Summary**: Broadcast indexed element within each quadword vector segment (unpredicated)

**Description**:
Unconditionally broadcast the indexed element within each
128-bit source vector segment to all elements
of the corresponding destination vector segment.
This instruction is unpredicated.

The immediate element index is in the range of 0 to 15 (bytes), 7
(halfwords), 3 (words) or 1 (doublewords).

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE2`
- **Assembly**: `DUPQ  <Zd>.<T>, <Zn>.<T>[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20 19  15   9   4  |
|--------------------------------|
| 000 0010 1   00  1   i1  tsz 001001 Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_quads_a.sve_int_perm_dupq_i.dupq_z_zi_)

```
if !IsFeatureImplemented(FEAT_SVE2p1) && !IsFeatureImplemented(FEAT_SME2p1) then
    EndOfDecode(Decode_UNDEF);
if tsz == '0000' then EndOfDecode(Decode_UNDEF);
constant integer lsb = LowestSetBit(tsz);
constant integer esize = 8 << lsb;
constant bits(5) imm = i1:tsz;
constant integer index = UInt(imm<4:(lsb+1)>);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_perm_quads_a.sve_int_perm_dupq_i.dupq_z_zi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer segments = VL DIV 128;
constant integer elements = 128 DIV esize;
constant bits(VL) operand = Z[n, VL];
bits(VL) result;
bits(esize) element;

for s = 0 to segments-1
    element = Elem[operand, s * elements + index, esize];
    Elem[result, s, 128] = Replicate(element, 128 DIV esize);

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2p1) \|\| IsFeatureImplemented(FEAT_SME2p1)` |
| 🚫 ENCODING_UNDEF | `tsz != '0000'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `tsz` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<imm>` | `immediate` | `i1:tsz` | Is the immediate index, in the range 0 to one less than the number of elements in 128 bits, encoded in "i1:tsz". |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 0000 | RESERVED |
| xxx1 | B |
| xx10 | H |
| x100 | S |
| 1000 | D |

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
- source: `dupq_z_zi.xml`
</details>