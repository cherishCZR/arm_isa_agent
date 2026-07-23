## sunpkhi_z_z
_ARM A64 Instruction_

**Title**: SUNPKHI, SUNPKLO -- A64 | **Class**: `sve` | **XML ID**: `sunpkhi_z_z`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME)

**Summary**: Signed unpack and extend half of vector

**Description**:
Unpack elements from the lowest or highest half of the source
vector and then sign-extend them to place in
elements of twice their size within the
destination vector.  This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `High half`
- **Assembly**: `SUNPKHI  <Zd>.<T>, <Zn>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18 17 16 15   9   4  |
|--------------------------------------|
| 000 0010 1   size 1   10  0   0   1   001110 Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_unpred_d.sve_int_perm_unpk.sunpkhi_z_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean unsigned = FALSE;
constant boolean hi = TRUE;
```

#### Execute (A64.sve.sve_perm_unpred_d.sve_int_perm_unpk.sunpkhi_z_z_)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer hsize = esize DIV 2;
constant integer offset = if hi then elements else 0;
constant bits(VL) operand = Z[n, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(hsize) element = Elem[operand, e + offset, hsize];
    Elem[result, e, esize] = Extend(element, esize, unsigned);

Z[d, VL] = result;
```

### Variant: `Low half`
- **Assembly**: `SUNPKLO  <Zd>.<T>, <Zn>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18 17 16 15   9   4  |
|--------------------------------------|
| 000 0010 1   size 1   10  0   0   0   001110 Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_unpred_d.sve_int_perm_unpk.sunpklo_z_z_)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd);
constant boolean unsigned = FALSE;
constant boolean hi = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<Tb>` | `unknown` | `size` | Is the size specifier, |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | H |
| 10 | S |
| 11 | D |

**<Tb> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | RESERVED |
| 01 | B |
| 10 | H |
| 11 | S |

### Encoding Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |
| 🚫 ENCODING_UNDEF | `size != '00'` |

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
- source: `sunpkhi_z_z.xml`
</details>