## MADDPT
_ARM A64 Instruction_

**Title**: MADDPT -- A64 | **Class**: `general` | **XML ID**: `MADDPT`

**Architecture**: `FEAT_CPA` (ARMv9.5)

**Summary**: Multiply-add checked pointer

**Description**:
This instruction multiplies two register values,
adds a third register value, and writes the result to the
destination register. The intermediate product is treated as the offset.

If the operation would have generated a result where the most significant 8 bits
of the result register differ from the most significant 8 bits of the base
register, then the result is modified such that it is likely to be non-canonical
when used as an address.

If the intermediate product cannot be correctly represented as a 64-bit
two's complement value, then the result is modified such that it is likely to be
non-canonical when used as an address.

### Variant: `Integer`
- **Assembly**: `MADDPT  <Xd>, <Xn>, <Xm>, <Xa>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28 27  24 23  20  15 14   9   4  |
|-----------------------------------|
| 1   00  1   101 1   011 Rm  0   Ra  Rn  Rd  |
```

#### Decode (A64.dpreg.dp_3src.MADDPT_64A_dp_3src)

```
if !IsFeatureImplemented(FEAT_CPA) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer a = UInt(Ra);
```

#### Execute (A64.dpreg.dp_3src.MADDPT_64A_dp_3src)

```
constant bits(64) operand1 = X[n, 64];
constant bits(64) operand2 = X[m, 64];
constant bits(64) operand3 = X[a, 64];

bits(64) result;

constant integer product = SInt(operand1) * SInt(operand2);

// Signed and unsigned twos complement arithmetic are equivalent if only a
// fixed number of bits are considered.
result = operand3 + product<63:0>;

constant boolean overflow = (product != SInt(product<63:0>));
result = PointerMultiplyAddCheck(result, operand3, overflow);

X[d, 64] = result;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_CPA)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<Xn>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first general-purpose source register holding the multiplicand, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register holding the multiplier, encoded in the "Rm" field. |
| `<Xa>` | `register (64-bit)` | `Ra` | Is the 64-bit name of the third general-purpose source register holding the addend, encoded in the "Ra" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `maddpt.xml`
</details>