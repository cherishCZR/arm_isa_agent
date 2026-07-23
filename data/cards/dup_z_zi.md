## DUP
_ARM A64 Instruction_

**Title**: DUP (indexed) -- A64 | **Class**: `sve` | **XML ID**: `dup_z_zi`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Broadcast indexed element to vector (unpredicated)

**Description**:
Unconditionally broadcast the indexed source vector element into each element of the
destination vector. This instruction is unpredicated.

The immediate element index is in the range of 0
to 63 (bytes), 31 (halfwords), 15 (words), 7
(doublewords) or 3 (quadwords).  Selecting an
element beyond the accessible vector length causes
the destination vector to be set to zero.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `DUP  <Zd>.<T>, <Zn>.<T>[<imm>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15   9   4  |
|-----------------------------|
| 000 0010 1   imm2 1   tsz 001000 Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_unpred_a.sve_int_perm_dup_i.dup_z_zi_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if tsz == '00000' then EndOfDecode(Decode_UNDEF);
constant integer lsb = LowestSetBit(tsz);
constant integer esize = 8 << lsb;
constant bits(7) imm = imm2:tsz;
constant integer index = UInt(imm<6:(lsb+1)>);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_perm_unpred_a.sve_int_perm_dup_i.dup_z_zi_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) operand1 = if index < elements then Z[n, VL] else Zeros(VL);
bits(VL) result;
bits(esize) element;

if index >= elements then
    element = Zeros(esize);
else
    element = Elem[operand1, index, esize];
result = Replicate(element, VL DIV esize);

Z[d, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `tsz != '00000'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `tsz` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<imm>` | `immediate` | `imm2:tsz` | Is the immediate index, in the range 0 to one less than the number of elements in 512 bits, encoded in "imm2:tsz". |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00000 | RESERVED |
| xxxx1 | B |
| xxx10 | H |
| xx100 | S |
| x1000 | D |
| 10000 | Q |

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
- source: `dup_z_zi.xml`
</details>