## LDADDB
_ARM A64 Instruction_

**Title**: LDADDB, LDADDAB, LDADDALB, LDADDLB -- A64 | **Class**: `general` | **XML ID**: `LDADDB`

**Architecture**: `FEAT_LSE` (ARMv8.1)

**Summary**: Atomic add on byte in memory

**Description**:
This instruction
atomically loads an 8-bit byte from memory, adds the value held in a register
to it, and stores the result back to memory.
The value initially loaded from memory is returned in the destination register.

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Integer (LDADDB_32_memop)` (No memory ordering)
- **Condition**: `A == 0 && R == 0`
- **Assembly**: `LDADDB  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 0   00  A   R   1   Rs  0   000 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop.LDADDB_32_memop)

```
if !IsFeatureImplemented(FEAT_LSE) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);

constant boolean acquire = A == '1' && Rt != '11111';
constant boolean release = R == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.memop.LDADDB_32_memop)

```
bits(64) address;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescAtomicOp(MemAtomicOp_ADD, acquire, release,
                                                          tagchecked, privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant bits(8) comparevalue = bits(8) UNKNOWN; // Irrelevant when not executing CAS
constant bits(8) value = X[s, 8];
constant bits(8) data = MemAtomic(address, comparevalue, value, accdesc);

if t != 31 then
    X[t, 32] = ZeroExtend(data, 32);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSE)` |

### Variant: `Integer (LDADDAB_32_memop)` (Acquire)
- **Condition**: `A == 1 && R == 0`
- **Assembly**: `LDADDAB  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 0   00  A   R   1   Rs  0   000 00  Rn  Rt  |
```

### Variant: `Integer (LDADDALB_32_memop)` (Acquire-release)
- **Condition**: `A == 1 && R == 1`
- **Assembly**: `LDADDALB  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 0   00  A   R   1   Rs  0   000 00  Rn  Rt  |
```

### Variant: `Integer (LDADDLB_32_memop)` (Release)
- **Condition**: `A == 0 && R == 1`
- **Assembly**: `LDADDLB  <Ws>, <Wt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  15 14  11   9   4  |
|-----------------------------------------|
| 00  111 0   00  A   R   1   Rs  0   000 00  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the general-purpose register holding the data value to be operated on with the contents of the memory location, encoded in the " |
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ldaddb.xml`
</details>