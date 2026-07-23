## SHA1M
_ARM A64 Instruction_

**Title**: SHA1M -- A64 | **Class**: `advsimd` | **XML ID**: `SHA1M_advsimd`

**Architecture**: `FEAT_SHA1` (ARMv8.0)

**Summary**: SHA1 hash update (majority)

**Description**:
SHA1 hash update (majority).

### Variant: `Advanced SIMD`
- **Assembly**: `SHA1M  <Qd>, <Sn>, <Vm>.4S`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24 23  21 20  15 14  11   9   4  |
|-----------------------------------|
| 0101 111 0   00  0   Rm  0   010 00  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptosha3.SHA1M_QSV_cryptosha3)

```
if !IsFeatureImplemented(FEAT_SHA1) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.simd_dp.cryptosha3.SHA1M_QSV_cryptosha3)

```
AArch64.CheckFPAdvSIMDEnabled();

bits(128) x = V[d, 128];
bits(32)  y = V[n, 32];    // Note: 32 not 128 bits wide
constant bits(128) w = V[m, 128];

for e = 0 to 3
    constant bits(32) t = SHAmajority(x<63:32>, x<95:64>, x<127:96>);
    y = y + ROL(x<31:0>, 5) + t + Elem[w, e, 32];
    x<63:32> = ROL(x<63:32>, 30);
    constant bits(160) yx = ROL(y:x, 32);
    (y, x) = (yx<159:128>, yx<127:0>);
V[d, 128] = x;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SHA1)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Qd>` | `register (128-bit)` | `Rd` | Is the 128-bit name of the SIMD&FP source and destination, encoded in the "Rd" field. |
| `<Sn>` | `register (32-bit)` | `Rn` | Is the 32-bit name of the second SIMD&FP source register, encoded in the "Rn" field. |
| `<Vm>` | `register (128-bit)` | `Rm` | Is the name of the third SIMD&FP source register, encoded in the "Rm" field. |

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
- source: `sha1m_advsimd.xml`
</details>