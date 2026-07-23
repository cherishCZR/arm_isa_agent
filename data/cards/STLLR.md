## STLLR
_ARM A64 Instruction_

**Title**: STLLR -- A64 | **Class**: `general` | **XML ID**: `STLLR`

**Architecture**: `FEAT_LOR` (PROFILE_A)

**Summary**: Store LORelease register

**Description**:
This instruction stores a 32-bit word or
a 64-bit doubleword to a memory location,
from a register.
The instruction also has memory ordering
semantics as described in
Load LOAcquire, Store LORelease.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `No offset (STLLR_SL32_ldstord)` (32-bit)
- **Condition**: `size == 10`
- **Assembly**: `STLLR  <Wt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 1x  0010001 0   0   (1)(1)(1)(1)(1) 0   (1)(1)(1)(1)(1) Rn  Rt  |
```

#### Decode (A64.ldst.ldstord.STLLR_SL32_ldstord)

```
if !IsFeatureImplemented(FEAT_LOR) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer elsize = 8 << UInt(size);
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldstord.STLLR_SL32_ldstord)

```
bits(64) address;
constant integer dbytes = elsize DIV 8;

constant AccessDescriptor accdesc = CreateAccDescLOR(MemOp_STORE, tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

Mem[address, dbytes, accdesc] = X[t, elsize];
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LOR)` |

### Variant: `No offset (STLLR_SL64_ldstord)` (64-bit)
- **Condition**: `size == 11`
- **Assembly**: `STLLR  <Xt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 1x  0010001 0   0   (1)(1)(1)(1)(1) 0   (1)(1)(1)(1)(1) Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `base-register`
- isa: `A64`
- source: `stllr.xml`
</details>