## STLR
_ARM A64 Instruction_

**Title**: STLR -- A64 | **Class**: `general` | **XML ID**: `STLR`

**Architecture**: `FEAT_LRCPC3` (ARMv8.9)

**Summary**: Store-release register

**Description**:
This instruction stores a 32-bit word or
a 64-bit doubleword to a memory location,
from a register.
The instruction also has memory ordering
semantics as described in
Load-Acquire, Store-Release.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `No offset (STLR_SL32_ldstord)` (32-bit)
- **Condition**: `size == 10`
- **Assembly**: `STLR  <Wt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 1x  0010001 0   0   (1)(1)(1)(1)(1) 1   (1)(1)(1)(1)(1) Rn  Rt  |
```

#### Decode (A64.ldst.ldstord.STLR_SL32_ldstord)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant boolean wback = FALSE;
constant integer offset = 0;
constant boolean rt_unknown = FALSE;

constant integer elsize = 8 << UInt(size);
constant integer datasize = elsize;
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldstord.STLR_SL32_ldstord)

```
bits(64) address;
constant integer dbytes = datasize DIV 8;

constant AccessDescriptor accdesc = CreateAccDescAcqRel(MemOp_STORE, tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);
bits(datasize) data;
if rt_unknown then
    data = bits(datasize) UNKNOWN;
else
    data = X[t, datasize];
Mem[address, dbytes, accdesc] = data;
if wback then
    if n == 31 then
        SP[64] = address;
    else
        X[n, 64] = address;
```

### Variant: `No offset (STLR_SL64_ldstord)` (64-bit)
- **Condition**: `size == 11`
- **Assembly**: `STLR  <Xt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 1x  0010001 0   0   (1)(1)(1)(1)(1) 1   (1)(1)(1)(1)(1) Rn  Rt  |
```

### Variant: `Pre-index (STLR_32S_ldapstl_writeback)` (32-bit)
- **Condition**: `size == 10`
- **Assembly**: `STLR  <Wt>, [<Xn|SP>, #-4]!`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21   9   4  |
|--------------------|
| 1x  0110011 0   000000000010 Rn  Rt  |
```

#### Decode (A64.ldst.ldapstl_writeback.STLR_32S_ldapstl_writeback)

```
if !IsFeatureImplemented(FEAT_LRCPC3) then EndOfDecode(Decode_UNDEF);
constant boolean wback = TRUE;

constant integer t = UInt(Rt);
constant integer n = UInt(Rn);

constant integer datasize = 8 << UInt(size);
constant integer offset = -1 * (1 << UInt(size));
constant boolean tagchecked = TRUE;

boolean rt_unknown = FALSE;

if n == t && n != 31 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_WBOVERLAPST);
    assert c IN {Constraint_NONE, Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_NONE    rt_unknown = FALSE;   // value stored is original value
        when Constraint_UNKNOWN rt_unknown = TRUE;    // value stored is UNKNOWN
        when Constraint_UNDEF   EndOfDecode(Decode_UNDEF);
        when Constraint_NOP     EndOfDecode(Decode_NOP);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LRCPC3)` |

### Variant: `Pre-index (STLR_64S_ldapstl_writeback)` (64-bit)
- **Condition**: `size == 11`
- **Assembly**: `STLR  <Xt>, [<Xn|SP>, #-8]!`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21   9   4  |
|--------------------|
| 1x  0110011 0   000000000010 Rn  Rt  |
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

- isa: `A64`
- source: `stlr.xml`
</details>