## RCWSCLR
_ARM A64 Instruction_

**Title**: RCWSCLR, RCWSCLRA, RCWSCLRAL, RCWSCLRL -- A64 | **Class**: `general` | **XML ID**: `RCWSCLR`

**Architecture**: `FEAT_THE` (ARMv8.9)

**Summary**: Read check write software atomic bit clear on doubleword in memory

**Description**:
This instruction atomically loads
a 64-bit doubleword from memory, performs a bitwise AND with the complement of the value
held in a register on it, and conditionally stores the result back to memory.
Storing of the result back to memory is conditional on RCW Checks and RCWS Checks.
The value initially loaded from memory is returned in the destination register.
This instruction updates the condition flags based on the result of the update of memory.

### Variant: `Integer (RCWSCLR_64_memop)` (RCWSCLR)
- **Condition**: `A == 0 && R == 0`
- **Assembly**: `RCWSCLR  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  26 25  23 22 21 20  15 14  11   9   4  |
|--------------------------------------------|
| 0   1   111 0   00  A   R   1   Rs  1   001 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop.RCWSCLR_64_memop)

```
if !IsFeatureImplemented(FEAT_THE) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant boolean soft = TRUE;

constant boolean acquire = A == '1' && Rt != '11111';
constant boolean release = R == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.memop.RCWSCLR_64_memop)

```
if IsD128Enabled(PSTATE.EL) then UNDEFINED;

bits(64) address;
constant bits(64) newdata = X[s, 64];
bits(64) readdata;
bits(4) nzcv;

constant AccessDescriptor accdesc = CreateAccDescRCW(MemAtomicOp_BIC, soft, acquire, release,
                                                     tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant bits(64) compdata = bits(64) UNKNOWN;    // Irrelevant when not executing CAS
(nzcv, readdata) = MemAtomicRCW(address, compdata, newdata, accdesc);

PSTATE.<N,Z,C,V> = nzcv;
X[t, 64] = readdata;    // Return the old value when t!=31
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_THE)` |

### Variant: `Integer (RCWSCLRA_64_memop)` (RCWSCLRA)
- **Condition**: `A == 1 && R == 0`
- **Assembly**: `RCWSCLRA  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  26 25  23 22 21 20  15 14  11   9   4  |
|--------------------------------------------|
| 0   1   111 0   00  A   R   1   Rs  1   001 00  Rn  Rt  |
```

### Variant: `Integer (RCWSCLRAL_64_memop)` (RCWSCLRAL)
- **Condition**: `A == 1 && R == 1`
- **Assembly**: `RCWSCLRAL  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  26 25  23 22 21 20  15 14  11   9   4  |
|--------------------------------------------|
| 0   1   111 0   00  A   R   1   Rs  1   001 00  Rn  Rt  |
```

### Variant: `Integer (RCWSCLRL_64_memop)` (RCWSCLRL)
- **Condition**: `A == 0 && R == 1`
- **Assembly**: `RCWSCLRL  <Xs>, <Xt>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  26 25  23 22 21 20  15 14  11   9   4  |
|--------------------------------------------|
| 0   1   111 0   00  A   R   1   Rs  1   001 00  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xs>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the general-purpose register to be stored, encoded in the "Rs" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `rcwsclr.xml`
</details>