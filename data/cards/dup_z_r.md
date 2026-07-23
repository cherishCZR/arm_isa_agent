## DUP
_ARM A64 Instruction_

**Title**: DUP (scalar) -- A64 | **Class**: `sve` | **XML ID**: `dup_z_r`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Broadcast general-purpose register to vector elements (unpredicated)

**Description**:
Unconditionally broadcast the general-purpose scalar source register into each element of the
destination vector. This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `SVE`
- **Assembly**: `DUP  <Zd>.<T>, <R><n|SP>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  15   9   4  |
|--------------------------------|
| 000 0010 1   size 1   00  000 001110 Rn  Zd  |
```

#### Decode (A64.sve.sve_perm_unpred_d.sve_int_perm_dup_r.dup_z_r_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Rn);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_perm_unpred_d.sve_int_perm_dup_r.dup_z_r_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
bits(64) operand;
if n == 31 then
    operand = SP[64];
else
    operand = X[n, 64];
bits(VL) result;

for e = 0 to elements-1
    Elem[result, e, esize] = operand<esize-1:0>;

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
| `<n\|SP>` | `unknown` | `Rn` | Is the number [0-30] of the general-purpose source register or the name SP (31), encoded in the "Rn" field. |

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
- source: `dup_z_r.xml`
</details>