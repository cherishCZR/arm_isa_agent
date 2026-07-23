## TBL
_ARM A64 Instruction_

**Title**: TBL -- A64 | **Class**: `N/A` | **XML ID**: `tbl_z_zz`

**Architecture**: `FEAT_SVE || FEAT_SME` (FEAT_SVE || FEAT_SME), `FEAT_SVE2 || FEAT_SME` (FEAT_SVE2 || FEAT_SME)

**Summary**: Programmable table lookup in one or two vector table (zeroing)

**Description**:
Reads each element of the second
source (index) vector and uses its value to select an indexed element from
a table of elements consisting of
   one or two consecutive vector registers,
   where the first or only vector
   holds the lower numbered elements,
and places the indexed table element in the destination vector element corresponding
to the index vector element.
If an index value is greater than or equal to the
 number of
vector elements
then it places zero in the corresponding destination vector element.

Since the index values can select any element in a vector this operation
is not naturally vector length agnostic.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`)

### Variant: `Single register table`
- **Assembly**: `TBL  <Zd>.<T>, { <Zn>.<T> }, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15   9   4  |
|-----------------------------|
| 000 0010 1   size 1   Zm  001100 Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_unpred_c.sve_int_perm_tbl.tbl_z_zz_1)

```
if !IsFeatureImplemented(FEAT_SVE) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant boolean double_table = FALSE;
```

#### Execute (A64.sve.sve_perm_unpred_c.sve_int_perm_tbl.tbl_z_zz_1)

```
CheckSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant bits(VL) indexes = Z[m, VL];
bits(VL) result;
constant integer table_size = if double_table then VL*2 else VL;
constant integer table_elems = table_size DIV esize;
bits(table_size) table;

if double_table then
    constant bits(VL) top = Z[(n + 1) MOD 32, VL];
    constant bits(VL) bottom = Z[n, VL];
    table = (top:bottom)<table_size-1:0>;
else
    table = Z[n, table_size];

for e = 0 to elements-1
    constant integer idx = UInt(Elem[indexes, e, esize]);
    Elem[result, e, esize] = if idx < table_elems then Elem[table, idx, esize] else Zeros(esize);

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE) \|\| IsFeatureImplemented(FEAT_SME)` |

### Variant: `Two register table`
- **Assembly**: `TBL  <Zd>.<T>, { <Zn1>.<T>, <Zn2>.<T> }, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  10  9   4  |
|--------------------------------|
| 000 0010 1   size 1   Zm  00101 0   Zn  Zd  |
```

#### Decode (A64.sve.sve_perm_unpred_b.sve_int_perm_tbl_3src.tbl_z_zz_2)

```
if !IsFeatureImplemented(FEAT_SVE2) && !IsFeatureImplemented(FEAT_SME) then
    EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
constant boolean double_table = TRUE;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE2) \|\| IsFeatureImplemented(FEAT_SME)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the first source multi-vector group, encoded in the "Zn" field. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the first source multi-vector group, encoded in the "Zn" field. |

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
- source: `tbl_z_zz.xml`
</details>