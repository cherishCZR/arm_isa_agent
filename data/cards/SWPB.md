## SWPB
_ARM A64 Instruction_

**Title**: SWPB, SWPAB, SWPALB, SWPLB -- A64 | **Class**: `general` | **XML ID**: `SWPB`

**Architecture**: `FEAT_LSE` (ARMv8.1)

**Summary**: Swap byte in memory

**Description**:
This instruction
atomically loads an 8-bit byte from a memory location,
and stores the value held in a register back to the same memory location.
The value initially loaded from memory is returned in the destination register.

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Integer (SWPB_32_memop)` (SWPB)
- **Condition**: `A == 0 && R == 0`
- **Assembly**: `SWPB  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 0   00  A   R   1   Rs  1   000 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop.SWPB_32_memop)

```
if !IsFeatureImplemented(FEAT_LSE) then EndOfDecode(Decode_UNDEF);

constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);

constant boolean acquire = A == '1' && Rt != '11111';
constant boolean release = R == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.memop.SWPB_32_memop)

```
bits(64) address;
bits(8) data;
bits(8) store_value;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescAtomicOp(MemAtomicOp_SWP, acquire, release,
                                                          tagchecked, privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

store_value = X[s, 8];

constant bits(8) comparevalue = bits(8) UNKNOWN; // Irrelevant when not executing CAS
data = MemAtomic(address, comparevalue, store_value, accdesc);

X[t, 32] = ZeroExtend(data, 32);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSE)` |

### Variant: `Integer (SWPAB_32_memop)` (SWPAB)
- **Condition**: `A == 1 && R == 0`
- **Assembly**: `SWPAB  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 0   00  A   R   1   Rs  1   000 00  Rn  Rt  |
```

### Variant: `Integer (SWPALB_32_memop)` (SWPALB)
- **Condition**: `A == 1 && R == 1`
- **Assembly**: `SWPALB  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 0   00  A   R   1   Rs  1   000 00  Rn  Rt  |
```

### Variant: `Integer (SWPLB_32_memop)` (SWPLB)
- **Condition**: `A == 0 && R == 1`
- **Assembly**: `SWPLB  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 0   00  A   R   1   Rs  1   000 00  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the general-purpose register to be stored, encoded in the "Rs" field. |
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `swpb.xml`
</details>