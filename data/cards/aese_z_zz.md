## AESE
_ARM A64 Instruction_

**Title**: AESE (vectors) -- A64 | **Class**: `sve2` | **XML ID**: `aese_z_zz`

**Architecture**: `FEAT_SVE_AES` (ARMv9.0)

**Summary**: AES single round encryption

**Description**:
The AESE instruction reads a 16-byte state array
from each 128-bit segment of the first source vector
together with a round key from the corresponding
128-bit segment of the second source vector.
Each state array undergoes a single round of the
AddRoundKey(), ShiftRows() and
SubBytes() transformations in accordance with
the AES standard. Each updated state array is destructively placed in
the corresponding segment of the first source vector. This instruction is unpredicated.

ID_AA64ZFR0_EL1.AES indicates whether this instruction is implemented.

This instruction is legal when executed in Streaming SVE mode if one of the following is true:

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_or_SSVE_AES`

### Variant: `SVE2`
- **Assembly**: `AESE  <Zdn>.B, <Zdn>.B, <Zm>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  17 16 15  12  10  9   4  |
|-----------------------------------------|
| 010 0010 1   00  1   000 1   0   111 00  0   Zm  Zdn |
```

#### Decode (A64.sve.sve_intx_crypto.sve_crypto_binary_dest.aese_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE_AES) then EndOfDecode(Decode_UNDEF);
constant integer m = UInt(Zm);
constant integer dn = UInt(Zdn);
```

#### Execute (A64.sve.sve_intx_crypto.sve_crypto_binary_dest.aese_z_zz_)

```
if IsFeatureImplemented(FEAT_SSVE_AES) then
    CheckSVEEnabled();
else
    CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer segments = VL DIV 128;
constant bits(VL) operand1 = Z[dn, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

result = operand1 EOR operand2;
for s = 0 to segments-1
    Elem[result, s, 128] = AESSubBytes(AESShiftRows(Elem[result, s, 128]));

Z[dn, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE_AES)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the first source and destination scalable vector register, encoded in the "Zdn" field. |
| `<Zm>` | `register (128-bit)` | `Zm` | Is the name of the second source scalable vector register, encoded in the "Zm" field. |

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
- source: `aese_z_zz.xml`
</details>