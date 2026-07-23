## INDEX
_ARM A64 Instruction_

**Title**: INDEX (scalar, immediate) -- A64 | **Class**: `sve` | **XML ID**: `index_z_ri`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Create index starting from general-purpose register and incremented by immediate

**Description**:
Populates the destination vector by setting the first element to
the first signed scalar integer operand and monotonically incrementing
the value by the second signed immediate integer operand for each subsequent element.
The scalar source operand is a general-purpose register in which only the least significant bits corresponding to the vector element size
are used and any remaining bits are ignored. This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `INDEX  <Zd>.<T>, <R><n>, #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  11   9   4  |
|--------------------------------|
| 000 0010 0   size 1   imm5 0100 01  Rn  Zd  |
```

#### Decode (A64.sve.sve_index.sve_int_index_ri.index_z_ri_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Rn);
constant integer d = UInt(Zd);
constant integer imm = SInt(imm5);
```

#### Execute (A64.sve.sve_index.sve_int_index_ri.index_z_ri_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(esize) operand1 = X[n, esize];
constant integer element1 = SInt(operand1);
bits(VL) result;

for e = 0 to elements-1
    constant integer index = element1 + e * imm;
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
| `<R>` | `unknown` | `size` | Is a width specifier, |
| `<n>` | `unknown` | `Rn` | Is the number [0-30] of the source general-purpose register or the name ZR (31), encoded in the "Rn" field. |
| `<imm>` | `immediate` | `imm5` | Is the signed immediate operand, in the range -16 to 15, encoded in the "imm5" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

**<R> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | W |
| 01 | W |
| 10 | W |
| 11 | X |

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
- source: `index_z_ri.xml`
</details>