## ADDPT
_ARM A64 Instruction_

**Title**: ADDPT -- A64 | **Class**: `general` | **XML ID**: `ADDPT`

**Architecture**: `FEAT_CPA` (ARMv9.5)

**Summary**: Add checked pointer

**Description**:
This instruction adds a base address register value and an optionally-shifted
register value, and writes the result to the destination register.
The optionally-shifted register value is treated as the offset.

If the operation would have generated a result where the most significant 8 bits
of the result register differ from the most significant 8 bits of the base
register, then the result is modified such that it is likely to be non-canonical
when used as an address.

### Variant: `Integer`
- **Assembly**: `ADDPT  <Xd|SP>, <Xn|SP>, <Xm>{, LSL #<amount>}`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  20  15  12   9   4  |
|-----------------------------------|
| 1   0   0   1   101 0000 Rm  001 imm3 Rn  Rd  |
```

#### Decode (A64.dpreg.addsub_pt.ADDPT_64_addsub_pt)

```
if !IsFeatureImplemented(FEAT_CPA) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer shift = UInt(imm3);
```

#### Execute (A64.dpreg.addsub_pt.ADDPT_64_addsub_pt)

```
bits(64) result;
constant bits(64) base = if n == 31 then SP[64] else X[n, 64];
constant bits(64) offset = LSL(X[m, 64], shift);

result = base + offset;
result = PointerAddCheck(result, base);

if d == 31 then
    SP[64] = result;
else
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
| `<Xd\|SP>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register or stack pointer, encoded in the "Rd" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first general-purpose source register or stack pointer, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register, encoded in the "Rm" field. |
| `<amount>` | `unknown` | `imm3` | Is the left shift amount, in the range 0 to 7, defaulting to 0, encoded in the "imm3" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `addpt.xml`
</details>