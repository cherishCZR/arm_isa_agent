## SM4EKEY
_ARM A64 Instruction_

**Title**: SM4EKEY -- A64 | **Class**: `sve2` | **XML ID**: `sm4ekey_z_zz`

**Architecture**: `FEAT_SVE_SM4` (ARMv9.0)

**Summary**: SM4 key updates

**Description**:
The SM4EKEY instruction reads four rounds of
32-bit input key values from each 128-bit segment of
the first source vector, along with four rounds of
32-bit constants from the corresponding 128-bit
segment of the second source vector. The four rounds
of output key values are derived in accordance with
the SM4 standard, and placed in the corresponding
segments of the destination vector.
This instruction is unpredicated.

ID_AA64ZFR0_EL1.SM4 indicates whether this instruction is implemented.

This instruction is illegal when executed in Streaming SVE mode, unless FEAT_SME_FA64 is implemented and enabled.

**Attributes**: DIT-sensitive (condition: `FEAT_SVE2 is implemented or FEAT_SME is implemented`); SM Policy: `SM_0_only`

### Variant: `SVE2`
- **Assembly**: `SM4EKEY  <Zd>.S, <Zn>.S, <Zm>.S`
**Encoding Diagram (32-bit)**:

```text
| 31  28  24 23  21 20  15  12  10  9   4  |
|-----------------------------------|
| 010 0010 1   00  1   Zm  111 10  0   Zn  Zd  |
```

#### Decode (A64.sve.sve_intx_crypto.sve_crypto_binary_const.sm4ekey_z_zz_)

```
if !IsFeatureImplemented(FEAT_SVE_SM4) then EndOfDecode(Decode_UNDEF);
constant integer n = UInt(Zn);
constant integer m = UInt(Zm);
constant integer d = UInt(Zd);
```

#### Execute (A64.sve.sve_intx_crypto.sve_crypto_binary_const.sm4ekey_z_zz_)

```
CheckNonStreamingSVEEnabled();
constant integer VL = CurrentVL;
constant integer segments = VL DIV 128;
constant bits(VL) operand1 = Z[n, VL];
constant bits(VL) operand2 = Z[m, VL];
bits(VL) result;

for s = 0 to segments-1
    constant bits(128) source = Elem[operand2, s, 128];
    bits(32) intval;
    bits(32) const;
    bits(128) roundresult = Elem[operand1, s, 128];

    for index = 0 to 3
        const = Elem[source, index, 32];
        intval = roundresult<127:96> EOR roundresult<95:64> EOR roundresult<63:32> EOR const;
        for i = 0 to 3
            Elem[intval, i, 8] = Sbox(Elem[intval, i, 8]);

        intval = intval EOR ROL(intval, 13) EOR ROL(intval, 23);
        intval = intval EOR roundresult<31:0>;

        roundresult<31:0> = roundresult<63:32>;
        roundresult<63:32> = roundresult<95:64>;
        roundresult<95:64> = roundresult<127:96>;
        roundresult<127:96> = intval;

    Elem[result, s, 128] = roundresult;

Z[d, VL] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SVE_SM4)` |

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
- source: `sm4ekey_z_zz.xml`
</details>