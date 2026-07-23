## ZIP
_ARM A64 Instruction_

**Title**: ZIP (four registers) -- A64 | **Class**: `mortlach2` | **XML ID**: `zip_mz_z`

**Architecture**: `FEAT_SME2` (ARMv9.3)

**Summary**: Interleave elements from four vectors

**Description**:
This instruction places the four-way interleaved elements from the four source vectors
in the corresponding elements of the four destination vectors.

This instruction is unpredicated.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_1_only`

### Variant: `8-bit to 64-bit elements`
- **Assembly**: `ZIP  { <Zd1>.<T>-<Zd4>.<T> }, { <Zn1>.<T>-<Zn4>.<T> }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   6   4   1  0 |
|--------------------------------------------|
| 1   10  0000 1   size 1   101 10  111000 Zn  00  Zd  0   0   |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi4_z_z_zip.zip_mz_z_4)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if size == '11' && MaxImplementedSVL() < 256 then EndOfDecode(Decode_UNDEF);
constant integer esize = 8 << UInt(size);
constant integer n = UInt(Zn:'00');
constant integer d = UInt(Zd:'00');
```

#### Execute (A64.sme.mortlach_multi_sve_4.mortlach_multi4_z_z_zip.zip_mz_z_4)

```
CheckStreamingSVEEnabled();
constant integer VL = CurrentVL;
if VL < esize * 4 then EndOfDecode(Decode_UNDEF);
constant integer quads = VL DIV (esize * 4);
constant bits(VL) operand0 = Z[n, VL];
constant bits(VL) operand1 = Z[n+1, VL];
constant bits(VL) operand2 = Z[n+2, VL];
constant bits(VL) operand3 = Z[n+3, VL];
bits(VL) result;

for r = 0 to 3
    constant integer base = r * quads;
    for q = 0 to quads-1
        Elem[result, 4*q+0, esize] = Elem[operand0, base+q, esize];
        Elem[result, 4*q+1, esize] = Elem[operand1, base+q, esize];
        Elem[result, 4*q+2, esize] = Elem[operand2, base+q, esize];
        Elem[result, 4*q+3, esize] = Elem[operand3, base+q, esize];
    Z[d+r, VL] = result;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `size != '11' \|\| MaxImplementedSVL() < 256` |

### Variant: `128-bit element`
- **Assembly**: `ZIP  { <Zd1>.Q-<Zd4>.Q }, { <Zn1>.Q-<Zn4>.Q }`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  24 23  21 20  17  15   9   6   4   1  0 |
|--------------------------------------------|
| 1   10  0000 1   00  1   101 11  111000 Zn  00  Zd  0   0   |
```

#### Decode (A64.sme.mortlach_multi_sve_4.mortlach_multi4_z_z_long_zip.zip_mz_z_4q)

```
if !IsFeatureImplemented(FEAT_SME2) then EndOfDecode(Decode_UNDEF);
if MaxImplementedSVL() < 512 then EndOfDecode(Decode_UNDEF);
constant integer esize = 128;
constant integer n = UInt(Zn:'00');
constant integer d = UInt(Zd:'00');
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `MaxImplementedSVL() < 512` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd1>` | `register (128-bit)` | `Zd` | Is the name of the first scalable vector register of the destination multi-vector group, encoded as "Zd" times 4. |
| `<T>` | `unknown` | `size` | Is the size specifier, |
| `<Zd4>` | `register (128-bit)` | `Zd` | Is the name of the fourth scalable vector register of the destination multi-vector group, encoded as "Zd" times 4 plus 3. |
| `<Zn1>` | `register (128-bit)` | `Zn` | Is the name of the first scalable vector register of the source multi-vector group, encoded as "Zn" times 4. |
| `<Zn4>` | `register (128-bit)` | `Zn` | Is the name of the fourth scalable vector register of the source multi-vector group, encoded as "Zn" times 4 plus 3. |

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
- source: `zip_mz_z.xml`
</details>