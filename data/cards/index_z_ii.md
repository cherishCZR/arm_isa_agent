## INDEX
_ARM A64 Instruction_

**Title**: INDEX (immediates) -- A64 | **Class**: `sve` | **XML ID**: `index_z_ii`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Create index starting from and incremented by immediate

**Description**:
Populates the destination vector by setting the first element to
the first signed immediate integer operand and monotonically incrementing
the value by the second signed immediate integer operand for each subsequent element.
 This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `INDEX  <Zd>.<T>, #<imm1>, #<imm2>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  11   9   4  |
|--------------------------------|
| 000 0010 0   size 1   imm5b 0100 00  imm5 Zd  |
```

#### Decode (A64.sve.sve_index.sve_int_index_ii.index_z_ii_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer d = UInt(Zd);
constant integer imm1 = SInt(imm5);
constant integer imm2 = SInt(imm5b);
```

#### Execute (A64.sve.sve_index.sve_int_index_ii.index_z_ii_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
bits(VL) result;

for e = 0 to elements-1
    constant integer index = imm1 + e * imm2;
    Elem[result, e, esize] = index<esize-1:0>;

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<imm1>` | `immediate` | `imm5` | Is the first signed immediate operand, in the range -16 to 15, encoded in the "imm5" field. |
| `<imm2>` | `immediate` | `imm5b` | Is the second signed immediate operand, in the range -16 to 15, encoded in the "imm5b" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

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
- source: `index_z_ii.xml`
</details>