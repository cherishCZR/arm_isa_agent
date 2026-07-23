## AESDIMC
_ARM A64 Instruction_

**Title**: AESDIMC -- A64 | **Class**: `sve2` | **XML ID**: `aesdimc_mz_zzi`

**Architecture**: `FEAT_SVE_AES2` (ARMv9.6)

**Summary**: Multi-vector AES single round decryption and inverse mix columns

**Description**:
The AESDIMC instruction reads a 16-byte state array from each
128-bit segment of the two or four first source vectors, together with a
round key from the indexed 128-bit segment of the corresponding 512-bit
portion of the second source vector.
Each state array undergoes a single round of the
AddRoundKey(), InvShiftRows(), InvSubBytes(), and InvMixColumns() transformations in accordance with the AES
standard. Each updated state array is destructively placed in the
corresponding segment of the two or four first source vectors.

When the vector length is less than 512 bits, the most
significant bits of the index are ignored to select the indexed
128-bit segment of the second source vector.
This instruction is unpredicated.

This instruction is legal when executed in Streaming SVE mode if both
FEAT_SSVE_AES and FEAT_SVE_AES2 are implemented.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_or_1`

### Variant: `Two registers`
- **Assembly**: `AESDIMC  { <Zdn1>.B-<Zdn2>.B }, { <Zdn1>.B-<Zdn2>.B }, <Zm>.Q[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  16 15  12  10  9   4   0 |
|--------------------------------------------|
| 010 0010 1   00  1   i2  01  1   111 01  1   Zm  Zdn 0   |
```

#### Decode (A64.sve.sve_intx_crypto.sve_crypto_binary_multi2.aesdimc_mz_zzi_2x1)

```
if !IsFeatureImplemented(FEAT_SVE_AES2) then EndOfDecode(Decode_UNDEF);
constant integer m = UInt(Zm);
constant integer dn = UInt(Zdn:'0');
integer index = UInt(i2);
constant integer nreg = 2;
```

#### Execute (A64.sve.sve_intx_crypto.sve_crypto_binary_multi2.aesdimc_mz_zzi_2x1)

```
if IsFeatureImplemented(FEAT_SSVE_AES) then
    CheckSVEEnabled();
else
    CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
if VL == 128 then index = 0;
if VL == 256 then index = index MOD 2;
constant integer segments = VL DIV 128;
constant bits(VL) operand2 = Z[m, VL];
array [0..3] of bits(VL) results;

for r = 0 to nreg-1
    constant bits(VL) operand1 = Z[dn + r, VL];
    for s = 0 to segments-1
        constant integer keyindex = (s - (s MOD 4)) + index;
        constant bits(128) res = Elem[operand1, s, 128] EOR Elem[operand2, keyindex, 128];
        Elem[results[r], s, 128] = AESInvMixColumns(AESInvSubBytes(AESInvShiftRows(res)));


for r = 0 to nreg-1
    Z[dn + r, VL] = results[r];
```

### Variant: `Four registers`
- **Assembly**: `AESDIMC  { <Zdn1>.B-<Zdn4>.B }, { <Zdn1>.B-<Zdn4>.B }, <Zm>.Q[<index>]`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  18  16 15  12  10  9   4   1  |
|--------------------------------------------|
| 010 0010 1   00  1   i2  11  1   111 01  1   Zm  Zdn 00  |
```

#### Decode (A64.sve.sve_intx_crypto.sve_crypto_binary_multi4.aesdimc_mz_zzi_4x1)

```
if !IsFeatureImplemented(FEAT_SVE_AES2) then EndOfDecode(Decode_UNDEF);
constant integer m = UInt(Zm);
constant integer dn = UInt(Zdn:'00');
integer index = UInt(i2);
constant integer nreg = 4;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn1>` | `register (128-bit)` | `Zdn` | For the "Two registers" variant: is the name of the first scalable vector register of the destination and first source multi-vector group, encoded as  |
| `<Zdn1>` | `register (128-bit)` | `Zdn` | For the "Four registers" variant: is the name of the first scalable vector register of the destination and first source multi-vector group, encoded as |
| `<Zdn2>` | `register (128-bit)` | `Zdn` | Is the name of the second scalable vector register of the destination and first source multi-vector group, encoded as "Zdn" times 2 plus 1. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |
| `<index>` | `unknown` | `i2` | Is the round key index, in the range 0 to 3, encoded in the "i2" field. |
| `<Zdn4>` | `register (128-bit)` | `Zdn` | Is the name of the fourth scalable vector register of the destination and first source multi-vector group, encoded as "Zdn" times 4 plus 3. |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE_AES2)` |

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
- source: `aesdimc_mz_zzi.xml`
</details>