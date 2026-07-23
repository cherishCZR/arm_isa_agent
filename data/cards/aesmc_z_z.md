## AESMC
_ARM A64 Instruction_

**Title**: AESMC -- A64 | **Class**: `sve2` | **XML ID**: `aesmc_z_z`

**Architecture**: `FEAT_SVE_AES` (ARMv9.0)

**Summary**: AES mix columns

**Description**:
The AESMC instruction reads a 16-byte state array
from each 128-bit segment of the source register, and
performs a single round of the MixColumns()
transformation on each state array in accordance with
the AES standard. Each updated state array is destructively placed in
the corresponding segment of the first source vector. This instruction is unpredicated.

ID_AA64ZFR0_EL1.AES indicates whether this instruction is implemented.

This instruction is legal when executed in Streaming SVE mode if one of the following is true:

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_or_SSVE_AES`

### Variant: `SVE2`
- **Assembly**: `AESMC  <Zdn>.B, <Zdn>.B`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  17  15  12  10  9   4  |
|--------------------------------------|
| 010 0010 1   00  1   000 00  111 00  0   00000 Zdn |
```

#### Decode (A64.sve.sve_intx_crypto.sve_crypto_unary.aesmc_z_z_)

```
if !IsFeatureImplemented(FEAT_SVE_AES) then EndOfDecode(Decode_UNDEF);
constant integer dn = UInt(Zdn);
```

#### Execute (A64.sve.sve_intx_crypto.sve_crypto_unary.aesmc_z_z_)

```
if IsFeatureImplemented(FEAT_SSVE_AES) then
    CheckSVEEnabled();
else
    CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer segments = VL DIV 128;
constant bits(VL) operand = Z[dn, VL];
bits(VL) result;

for s = 0 to segments-1
    Elem[result, s, 128] = AESMixColumns(Elem[operand, s, 128]);

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
| `<Zdn>` | `register (128-bit)` | `Zdn` | Is the name of the source and destination scalable vector register, encoded in the "Zdn" field. |

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
- source: `aesmc_z_z.xml`
</details>