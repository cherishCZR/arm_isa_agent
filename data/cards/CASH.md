## CASH
_ARM A64 Instruction_

**Title**: CASH, CASAH, CASALH, CASLH -- A64 | **Class**: `general` | **XML ID**: `CASH`

**Architecture**: `FEAT_LSE` (ARMv8.1)

**Summary**: Compare and swap halfword in memory

**Description**:
This instruction
reads a 16-bit halfword
from memory, and compares it against the value held in a first
register. If the comparison is equal, the value in a second register
is written to memory. If the comparison is not equal, the architecture permits writing
the value read from the location to memory.
If the write is performed, the read and write occur atomically such
that no other modification of the memory location can take place
between the read and write.

The architecture permits that the data read clears any exclusive
monitors associated with that location, even if the compare
subsequently fails.

If the instruction generates a synchronous Data Abort, the register
which is compared and loaded, that is <Ws>, is restored to
the values held in the register before the instruction was executed.

For a CASH or CASAH instruction, when <Ws>
or <Xs> specifies the same register as <Wt> or <Xt>,
this signals to the memory system that an additional subsequent CASH,
CASAH, CASALH, or CASLH
access to the specified location is likely to occur in the near future. The memory system can respond by
taking actions that are expected to enable the subsequent CASH,
CASAH, CASALH, or CASLH access to succeed when it does occur.

A code sequence starting with a CASH or CASAH instruction for which
<Ws> or <Xs> specifies the same register as <Wt>
or <Xt>, and ending with a subsequent CASH, CASAH,
CASALH, or CASLH to the same location, exhibits the following
properties for best performance when the location may be accessed concurrently, on one or more other PEs:

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `No offset (CASH_C32_comswap)` (CASH)
- **Condition**: `L == 0 && o0 == 0`
- **Assembly**: `CASH  <Ws>, <Wt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`0`, `o0`=`0`
- **Bit Pattern**: `???????????????0??????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 01  0010001 L   1   Rs  o0  11111 Rn  Rt  |
```

#### Decode (A64.ldst.comswap.CASH_C32_comswap)

```
if !IsFeatureImplemented(FEAT_LSE) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant boolean acquire = L == '1';
constant boolean release = o0 == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.comswap.CASH_C32_comswap)

```
bits(64) address;
bits(16) comparevalue;
bits(16) newvalue;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescAtomicOp(MemAtomicOp_CAS, acquire, release,
                                                          tagchecked, privileged);
comparevalue = X[s, 16];
newvalue = X[t, 16];

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant bits(16) data = MemAtomic(address, comparevalue, newvalue, accdesc);
X[s, 32] = ZeroExtend(data, 32);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSE)` |

### Variant: `No offset (CASAH_C32_comswap)` (CASAH)
- **Condition**: `L == 1 && o0 == 0`
- **Assembly**: `CASAH  <Ws>, <Wt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`1`, `o0`=`0`
- **Bit Pattern**: `???????????????0??????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 01  0010001 L   1   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASALH_C32_comswap)` (CASALH)
- **Condition**: `L == 1 && o0 == 1`
- **Assembly**: `CASALH  <Ws>, <Wt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`1`, `o0`=`1`
- **Bit Pattern**: `???????????????1??????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 01  0010001 L   1   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASLH_C32_comswap)` (CASLH)
- **Condition**: `L == 0 && o0 == 1`
- **Assembly**: `CASLH  <Ws>, <Wt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`0`, `o0`=`1`
- **Bit Pattern**: `???????????????1??????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 01  0010001 L   1   Rs  o0  11111 Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the general-purpose register to be compared and loaded, encoded in the "Rs" field. |
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be conditionally stored, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- address-form: `base-register`
- isa: `A64`
- source: `cash.xml`
</details>