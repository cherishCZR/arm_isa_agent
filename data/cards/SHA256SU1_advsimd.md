## SHA256SU1
_ARM A64 Instruction_

**Title**: SHA256SU1 -- A64 | **Class**: `advsimd` | **XML ID**: `SHA256SU1_advsimd`

**Architecture**: `FEAT_SHA256` (ARMv8.0)

**Summary**: SHA256 schedule update 1

**Description**:
SHA256 schedule update 1.

### Variant: `Advanced SIMD`
- **Assembly**: `SHA256SU1  <Vd>.4S, <Vn>.4S, <Vm>.4S`
**Encoding Diagram (32-bit)**:

```text
| 31  27  24 23  21 20  15 14  11   9   4  |
|-----------------------------------|
| 0101 111 0   00  0   Rm  0   110 00  Rn  Rd  |
```

#### Decode (A64.simd_dp.cryptosha3.SHA256SU1_VVV_cryptosha3)

```
if !IsFeatureImplemented(FEAT_SHA256) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.simd_dp.cryptosha3.SHA256SU1_VVV_cryptosha3)

```
AArch64.CheckFPAdvSIMDEnabled();

constant bits(128) operand1 = V[d, 128];
constant bits(128) operand2 = V[n, 128];
constant bits(128) operand3 = V[m, 128];
constant bits(128) T0 = operand3<31:0> : operand2<127:32>;

bits(64) T1;
bits(32) elt;
bits(128) result;

T1 = operand3<127:64>;
for e = 0 to 1
    elt = Elem[T1, e, 32];
    elt = ROR(elt, 17) EOR ROR(elt, 19) EOR LSR(elt, 10);
    elt = elt + Elem[operand1, e, 32] + Elem[T0, e, 32];
    Elem[result, e, 32] = elt;

T1 = result<63:0>;
for e = 2 to 3
    elt = Elem[T1, e - 2, 32];
    elt = ROR(elt, 17) EOR ROR(elt, 19) EOR LSR(elt, 10);
    elt = elt + Elem[operand1, e, 32] + Elem[T0, e, 32];
    Elem[result, e, 32] = elt;

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
- source: `sha256su1_advsimd.xml`
</details>