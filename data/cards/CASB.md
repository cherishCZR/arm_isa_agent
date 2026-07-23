## CASB
_ARM A64 Instruction_

**Title**: CASB, CASAB, CASALB, CASLB -- A64 | **Class**: `general` | **XML ID**: `CASB`

**Architecture**: `FEAT_LSE` (ARMv8.1)

**Summary**: Compare and swap byte in memory

**Description**:
This instruction
reads an 8-bit byte
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

For a CASB or CASAB instruction, when <Ws>
or <Xs> specifies the same register as <Wt> or <Xt>,
this signals to the memory system that an additional subsequent CASB,
CASAB, CASALB, or CASLB
access to the specified location is likely to occur in the near future. The memory system can respond by
taking actions that are expected to enable the subsequent CASB,
CASAB, CASALB, or CASLB access to succeed when it does occur.

A code sequence starting with a CASB or CASAB instruction for which
<Ws> or <Xs> specifies the same register as <Wt>
or <Xt>, and ending with a subsequent CASB, CASAB,
CASALB, or CASLB to the same location, exhibits the following
properties for best performance when the location may be accessed concurrently, on one or more other PEs:

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `No offset (CASB_C32_comswap)` (CASB)
- **Condition**: `L == 0 && o0 == 0`
- **Assembly**: `CASB  <Ws>, <Wt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`0`, `o0`=`0`
- **Bit Pattern**: `???????????????0??????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 00  0010001 L   1   Rs  o0  11111 Rn  Rt  |
```

#### Decode (A64.ldst.comswap.CASB_C32_comswap)

```
if !IsFeatureImplemented(FEAT_LSE) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant boolean acquire = L == '1';
constant boolean release = o0 == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.comswap.CASB_C32_comswap)

```
bits(64) address;
bits(8) comparevalue;
bits(8) newvalue;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescAtomicOp(MemAtomicOp_CAS, acquire, release,
                                                          tagchecked, privileged);
comparevalue = X[s, 8];
newvalue = X[t, 8];

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant bits(8) data = MemAtomic(address, comparevalue, newvalue, accdesc);
X[s, 32] = ZeroExtend(data, 32);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSE)` |

### Variant: `No offset (CASAB_C32_comswap)` (CASAB)
- **Condition**: `L == 1 && o0 == 0`
- **Assembly**: `CASAB  <Ws>, <Wt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`1`, `o0`=`0`
- **Bit Pattern**: `???????????????0??????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 00  0010001 L   1   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASALB_C32_comswap)` (CASALB)
- **Condition**: `L == 1 && o0 == 1`
- **Assembly**: `CASALB  <Ws>, <Wt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`1`, `o0`=`1`
- **Bit Pattern**: `???????????????1??????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 00  0010001 L   1   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASLB_C32_comswap)` (CASLB)
- **Condition**: `L == 0 && o0 == 1`
- **Assembly**: `CASLB  <Ws>, <Wt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`0`, `o0`=`1`
- **Bit Pattern**: `???????????????1??????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 00  0010001 L   1   Rs  o0  11111 Rn  Rt  |
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
- source: `casb.xml`
</details>