## SUNPK
_ARM A64 Instruction_

**Title**: SUNPK -- A64 | **Class**: `mortlach2` | **XML ID**: `sunpk_mz_z`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Unpack and sign-extend multi-vector elements

**Description**:
This instruction unpacks elements from one or two source
vectors and then sign-extends them to place in elements of twice their size
within the two or four destination vectors.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `Two registers`
- **Assembly**: `SUNPK  { <Zd1>.<T>-<Zd2>.<T> }, <Zn>.<Tb>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   4   0 |
|--------------------------------------|
| 1   10  0000 1   size 1   001 01  111000 Zn  Zd  0   |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi2_wide_int.sunpk_mz_z_2)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer d = UInt(Zd:'0');
constant integer nreg = 2;
constant boolean unsigned = FALSE;
```

#### Execute (A64.sme.mortlach_multi_sve_4.mortlach_multi2_wide_int.sunpk_mz_z_2)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV esize;
constant integer hsize = esize DIV 2;
constant integer sreg = nreg DIV 2;
array [0..3] of bits(VL) results;

for r = 0 to sreg-1
    constant bits(VL) operand = Z[n+r, VL];
    for i = 0 to 1
        for e = 0 to elements-1
            constant bits(hsize) element = Elem[operand, i*elements + e, hsize];
            Elem[results[2*r+i], e, esize] = Extend(element, esize, unsigned);

for r = 0 to nreg-1
    Z[d+r, VL] = results[r];
```

### Variant: `Four registers`
- **Assembly**: `SUNPK  { <Zd1>.<T>-<Zd4>.<T> }, { <Zn1>.<Tb>-<Zn2>.<Tb> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   5  4   1  0 |
|--------------------------------------------|
| 1   10  0000 1   size 1   101 01  111000 Zn  0   Zd  0   0   |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi4_wide_int.sunpk_mz_z_4)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if size == '00' then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn:'0');
constant integer d = UInt(Zd:'00');
constant integer nreg = 4;
constant boolean unsigned = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Two registers" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 2. |
| `<Zd1>` | `register (128-bit)` | `Zd` | For the "Four registers" variant: is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 4. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zd2>` | `register (128-bit)` | `Zd` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zd" times 2 plus 1. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the source scalable vector register, encoded in the "Zn" field. |
| `<Tb>` | `unknown` | `size` | Is the size specifier, |
| `<Zd4>` | `register (128-bit)` | `Zd` | Is the name of the fourth scalable vector register of the destination multi-vector group, encoded as "Zd" times 4 plus 3. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 2. |
| `<Zn2>` | `register (128-bit)` | `Zn` | Is the name of the second scalable vector register of the source multi-vector group, encoded as "Zn" times 2 plus 1. |

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
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |
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
- source: `sunpk_mz_z.xml`
</details>