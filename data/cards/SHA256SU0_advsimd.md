## SHA256SU0
_ARM A64 Instruction_

**Title**: SHA256SU0 -- A64 | **Class**: `advsimd` | **XML ID**: `SHA256SU0_advsimd`

**Architecture**: `FEAT_SHA256` (ARMv8.0)

**Summary**: SHA256 schedule update 0

**Description**:
SHA256 schedule update 0.

### Variant: `Advanced SIMD`
- **Assembly**: `SHA256SU0  <Vd>.4S, <Vn>.4S`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24 23  21  16  11   9   4  |
|-----------------------------|
| 0101 111 0   00  10100 00010 10  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptosha2.SHA256SU0_VV_cryptosha2)

```
if !IsFeatureImplemented(FEAT_SHA256) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
```

#### Execute (A64.simd_dp.cryptosha2.SHA256SU0_VV_cryptosha2)

```
AArch64.CheckFPAdvSIMDEnabled();

constant bits(128) operand1 = V[d, 128];
constant bits(128) operand2 = V[n, 128];
constant bits(128) T = operand2<31:0> : operand1<127:32>;
bits(128) result;
bits(32) elt;

for e = 0 to 3
    elt = Elem[T, e, 32];
    elt = ROR(elt, 7) EOR ROR(elt, 18) EOR LSR(elt, 3);
    Elem[result, e, 32] = elt + Elem[operand1, e, 32];
V[d, 128] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_SHA256)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Vd>` | `register (128-bit)` | `Rd` | Is the name of the SIMD&FP source and destination register, encoded in the "Rd" field. |
| `<Vn>` | `register (128-bit)` | `Rn` | Is the name of the second SIMD&FP source register, encoded in the "Rn" field. |

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
- source: `sha256su0_advsimd.xml`
</details>