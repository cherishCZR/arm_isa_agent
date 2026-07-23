## SUBP
_ARM A64 Instruction_

**Title**: SUBP -- A64 | **Class**: `general` | **XML ID**: `SUBP`

**Architecture**: `FEAT_MTE` (ARMv8.5)

**Summary**: Subtract pointer

**Description**:
This instruction subtracts the 56-bit address held in the second source
register from the 56-bit address held in the first source register,
sign-extends the result to 64 bits, and writes the result to the destination
register.

### Variant: `Integer`
- **Assembly**: `SUBP  <Xd>, <Xn|SP>, <Xm|SP>`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  20  15   9   4  |
|--------------------------------|
| 1   0   0   1   101 0110 Rm  000000 Rn  Rd  |
```

#### Decode (A64.dpreg.dp_2src.SUBP_64S_dp_2src)

```
if !IsFeatureImplemented(FEAT_MTE) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.dpreg.dp_2src.SUBP_64S_dp_2src)

```
bits(64) operand1 = if n == 31 then SP[64] else X[n, 64];
bits(64) operand2 = if m == 31 then SP[64] else X[m, 64];
operand1 = SignExtend(operand1<55:0>, 64);
operand2 = NOT(SignExtend(operand2<55:0>, 64));
bits(64) result;

(result, -) = AddWithCarry(operand1, operand2, '1');

X[d, 64] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_MTE)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first source general-purpose register or stack pointer, encoded in the "Rn" field. |
| `<Xm\|SP>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register or stack pointer, encoded in the "Rm" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `subp.xml`
</details>