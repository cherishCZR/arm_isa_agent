## SM4EKEY
_ARM A64 Instruction_

**Title**: SM4EKEY -- A64 | **Class**: `advsimd` | **XML ID**: `SM4EKEY_advsimd`

**Architecture**: `FEAT_SM4` (ARMv8.2)

**Summary**: SM4 key

**Description**:
This instruction takes an input as a 128-bit vector from the first source SIMD&FP register
and a 128-bit constant from the second SIMD&FP register. It derives four iterations
of the output key, in accordance with the SM4 standard, returning the 128-bit result
to the destination SIMD&FP register.

### Variant: `Advanced SIMD`
- **Assembly**: `SM4EKEY  <Vd>.4S, <Vn>.4S, <Vm>.4S`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24  22  20  15 14 13  11   9   4  |
|-----------------------------------|
| 1100 111 00  11  Rm  1   1   00  10  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptosha512_3.SM4EKEY_VVV4_cryptosha512_3)

```
if !IsFeatureImplemented(FEAT_SM4) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.simd_dp.cryptosha512_3.SM4EKEY_VVV4_cryptosha512_3)

```
AArch64.CheckFPAdvSIMDEnabled();

constant bits(128) Vm = V[m, 128];
bits(32) intval;
bits(32) const;
bits(128) roundresult;

roundresult = V[n, 128];
for index = 0 to 3
    const = Elem[Vm, index, 32];

    intval = roundresult<127:96> EOR roundresult<95:64> EOR roundresult<63:32> EOR const;

    for i = 0 to 3
        Elem[intval, i, 8] = Sbox(Elem[intval, i, 8]);

    intval = intval EOR ROL(intval, 13) EOR ROL(intval, 23);
    intval = intval EOR roundresult<31:0>;

    roundresult<31:0>   = roundresult<63:32>;
    roundresult<63:32>  = roundresult<95:64>;
    roundresult<95:64>  = roundresult<127:96>;
    roundresult<127:96> = intval;

V[d, 128] = roundresult;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SM4)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the first SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the second SIMD&FP source register, encoded in the "Rm" field. |

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
- source: `sm4ekey_advsimd.xml`
</details>