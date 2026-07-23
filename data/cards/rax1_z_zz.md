## RAX1
_ARM A64 Instruction_

**Title**: RAX1 -- A64 | **Class**: `sve2` | **XML ID**: `rax1_z_zz`

**Architecture**: `FEAT_SVE_SHA3` (ARMv9.0)

**Summary**: Bitwise rotate left by 1 and exclusive-OR

**Description**:
Rotate each 64-bit element of the second source vector
left by 1 and exclusive-OR with the corresponding
elements of the first source vector. The results are
placed in the corresponding elements of the destination
vector.
This instruction is unpredicated.

ID_AA64ZFR0_EL1.SHA3 indicates whether this instruction is implemented.

This instruction is illegal when
      executed in Streaming SVE mode, unless FEAT_SME_FA64 is
      implemented and enabled, or FEAT_SME2p1 is implemented.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_or_SME2p1`

### Variant: `SVE2`
- **Assembly**: `RAX1  <Zd>.D, <Zn>.D, <Zm>.D`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12  10  9   4  |
|-----------------------------------|
| 010 0010 1   00  1   Zm  111 10  1   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_crypto.sve_crypto_binary_const.rax1_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE_SHA3) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_intx_crypto.sve_crypto_binary_const.rax1_z_zz_)

```
if IsFeatureImplemented(FEAT_SME2p1) then CheckSVEEnabled(); else CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer elements = VL DIV 64;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for e = 0 to elements-1
    constant bits(64) element1 = Elem[operand1, e, 64];
    constant bits(64) element2 = Elem[operand2, e, 64];
    Elem[result, e, 64] = element1 EOR ROL(element2, 1);
Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE_SHA3)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Zd>` | `register (128-bit)` | `Zd` | Is the name of the destination scalable vector register, encoded in the "Zd" field. |
| `<Zn>` | `register (128-bit)` | `Zn` | Is the name of the first source scalable vector register, encoded in the "Zn" field. |
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
- source: `rax1_z_zz.xml`
</details>