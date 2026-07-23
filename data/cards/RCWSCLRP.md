## RCWSCLRP
_ARM A64 Instruction_

**Title**: RCWSCLRP, RCWSCLRPA, RCWSCLRPAL, RCWSCLRPL -- A64 | **Class**: `general` | **XML ID**: `RCWSCLRP`

**Architecture**: `FEAT_D128 && FEAT_THE` (FEAT_D128 && FEAT_THE)

**Summary**: Read check write software atomic bit clear on quadword in memory

**Description**:
This instruction atomically loads
a 128-bit quadword from memory, performs a bitwise AND with the complement of the value
held in a pair of registers on it, and conditionally stores the result back to memory.
Storing of the result back to memory is conditional on RCW Checks and RCWS Checks.
The value initially loaded from memory is returned in the same pair of registers.
This instruction updates the condition flags based on the result of the update of memory.

### Variant: `Integer (RCWSCLRP_128_memop_128)` (RCWSCLRP)
- **Condition**: `A == 0 && R == 0`
- **Assembly**: `RCWSCLRP  <Xt1>, <Xt2>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   1   011001 A   R   1   Rt2 1   001 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop_128.RCWSCLRP_128_memop_128)

```
if !IsFeatureImplemented(FEAT_D128) || !IsFeatureImplemented(FEAT_THE) then
    EndOfDecode(Decode_UNDEF);
if Rt  == '11111' then EndOfDecode(Decode_UNDEF);
if Rt2 == '11111' then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant boolean soft = TRUE;

constant boolean acquire = A == '1';
constant boolean release = R == '1';
constant boolean tagchecked = n != 31;

boolean rt_unknown = FALSE;

if t == t2 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_LSE128OVERLAP);
    assert c IN {Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_UNKNOWN rt_unknown = TRUE;    // result is UNKNOWN
        when Constraint_UNDEF   EndOfDecode(Decode_UNDEF);
        when Constraint_NOP     EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.memop_128.RCWSCLRP_128_memop_128)

```
if !IsD128Enabled(PSTATE.EL) then UNDEFINED;
bits(64) address;
bits(64) value1;
bits(64) value2;
bits(128) newdata;
bits(128) readdata;
bits(4) nzcv;

constant AccessDescriptor accdesc = CreateAccDescRCW(MemAtomicOp_BIC, soft, acquire, release,
                                                     tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

value1 = X[t, 64];
value2 = X[t2, 64];

newdata = if BigEndian(accdesc.acctype) then value1:value2 else value2:value1;

constant bits(128) compdata = bits(128) UNKNOWN;    // Irrelevant when not executing CAS
(nzcv, readdata) = MemAtomicRCW(address, compdata, newdata, accdesc);

PSTATE.<N,Z,C,V> = nzcv;
if rt_unknown then
    readdata = bits(128) UNKNOWN;

if BigEndian(accdesc.acctype) then
    X[t, 64] = readdata<127:64>;
    X[t2, 64] = readdata<63:0>;
else
    X[t, 64] = readdata<63:0>;
    X[t2, 64] = readdata<127:64>;
```

#### Constraints
_2× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_D128) && IsFeatureImplemented(FEAT_THE)` |
| 🚫 ENCODING_UNDEF | `Rt != '11111'` |
| 🚫 ENCODING_UNDEF | `Rt2 != '11111'` |

### Variant: `Integer (RCWSCLRPA_128_memop_128)` (RCWSCLRPA)
- **Condition**: `A == 1 && R == 0`
- **Assembly**: `RCWSCLRPA  <Xt1>, <Xt2>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   1   011001 A   R   1   Rt2 1   001 00  Rn  Rt  |
```

### Variant: `Integer (RCWSCLRPAL_128_memop_128)` (RCWSCLRPAL)
- **Condition**: `A == 1 && R == 1`
- **Assembly**: `RCWSCLRPAL  <Xt1>, <Xt2>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   1   011001 A   R   1   Rt2 1   001 00  Rn  Rt  |
```

### Variant: `Integer (RCWSCLRPL_128_memop_128)` (RCWSCLRPL)
- **Condition**: `A == 0 && R == 1`
- **Assembly**: `RCWSCLRPL  <Xt1>, <Xt2>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   1   011001 A   R   1   Rt2 1   001 00  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xt2>` | `register (64-bit)` | `Rt2` | Is the 64-bit name of the second general-purpose register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `rcwsclrp.xml`
</details>