## UZP
_ARM A64 Instruction_

**Title**: UZP (two registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `uzp_mz_zz`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Concatenate elements from two vectors

**Description**:
This instruction concatenates every second element from each of the first and second source vectors
and places them in the corresponding elements of the two destination vectors.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `8-bit to 64-bit elements`
- **Assembly**: `UZP  { <Zd1>.<T>-<Zd2>.<T> }, <Zn>.<T>, <Zm>.<T>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4   0 |
|--------------------------------------|
| 1   10  0000 1   size 1   Zm  110 100 Zn  Zd  1   |
```

#### Decode (A64.sme.mortlach_multi_sve_3.mortlach_multi2_z_z_zip.uzp_mz_zz_2)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd:'0');
```

#### Execute (A64.sme.mortlach_multi_sve_3.mortlach_multi2_z_z_zip.uzp_mz_zz_2)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
if VL < esize * 2 then EndOfDecode(Decode_UNDEF);
constant integer pairs = VL DIV (esize * 2);
bits(VL) result0;
bits(VL) result1;

for r = 0 to 1
    constant integer base = r * pairs;
    constant bits(VL) operand = if r == 0 then Z[n, VL] else Z[m, VL];
    for p = 0 to pairs-1
        Elem[result0, base+p, esize] = Elem[operand, 2*p+0, esize];
        Elem[result1, base+p, esize] = Elem[operand, 2*p+1, esize];

Z[d+0, VL] = result0;
Z[d+1, VL] = result1;
```

### Variant: `128-bit element`
- **Assembly**: `UZP  { <Zd1>.Q-<Zd2>.Q }, <Zn>.Q, <Zm>.Q`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  15  12   9   4   0 |
|--------------------------------------|
| 1   10  0000 1   00  1   Zm  110 101 Zn  Zd  1   |
```

#### Decode (A64.sme.mortlach_multi_sve_3.mortlach_multi2_z_z_long_zip.uzp_mz_zz_2q)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if MaxImplementedSVL() < 256 then EndOfDecode(Decode_UNDEF);
constant integer esize = 128;
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd:'0');
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `MaxImplementedSVL() < 256` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | Is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 2. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zd2>` | `register (128-bit)` | `Zd` | Is the name of the second scalable vector register of the destination multi-vector group, encoded as "Zd" times 2 plus 1. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

**<T> Value Table**:

| bitfield | symbol |
|---|---|
| 00 | B |
| 01 | H |
| 10 | S |
| 11 | D |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SME2)` |

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
- source: `uzp_mz_zz.xml`
</details>