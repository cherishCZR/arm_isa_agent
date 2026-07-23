## IRG
_ARM A64 Instruction_

**Title**: IRG -- A64 | **Class**: `general` | **XML ID**: `IRG`

**Architecture**: `FEAT_MTE` (ARMv8.5)

**Summary**: Insert random tag

**Description**:
This instruction inserts a random Logical Address Tag into the address in the
first source register, and writes the result to the destination register. Any
tags specified in the optional second source register or in GCR_EL1.Exclude
are excluded from the selection of the random Logical Address Tag.

### Variant: `Integer`
- **Assembly**: `IRG  <Xd|SP>, <Xn|SP>{, <Xm>}`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29 28 27  24  20  15   9   4  |
|--------------------------------|
| 1   0   0   1   101 0110 Rm  000100 Rn  Rd  |
```

#### Decode (A64.dpreg.dp_2src.IRG_64I_dp_2src)

```
if !IsFeatureImplemented(FEAT_MTE) then EndOfDecode(Decode_UNDEF);
constant integer d = UInt(Rd);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
```

#### Execute (A64.dpreg.dp_2src.IRG_64I_dp_2src)

```
constant bits(64) operand = if n == 31 then SP[64] else X[n, 64];
constant bits(64) exclude_reg = X[m, 64];
constant bits(16) exclude = exclude_reg<15:0> OR GCR_EL1.Exclude;
bits(4) rtag;

if AArch64.AllocationTagAccessIsEnabled(PSTATE.EL) then
    if GCR_EL1.RRND == '1' then
        if IsOnes(exclude) then
            rtag = '0000';
        else
            rtag = ChooseRandomNonExcludedTag(exclude);
    else
        constant bits(4) start_tag = RGSR_EL1.TAG;
        constant bits(4) offset = AArch64.RandomTag();

        rtag = AArch64.ChooseNonExcludedTag(start_tag, offset, exclude);

        RGSR_EL1.TAG = rtag;
else
    rtag = '0000';

constant bits(64) result = AArch64.AddressWithAllocationTag(operand, rtag);

if d == 31 then
    SP[64] = result;
else
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
| `<Xd\|SP>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the destination general-purpose register or stack pointer, encoded in the "Rd" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the first source general-purpose register or stack pointer, encoded in the "Rn" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | Is the 64-bit name of the second general-purpose source register, encoded in the "Rm" field. Defaults to XZR if absent. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `irg.xml`
</details>