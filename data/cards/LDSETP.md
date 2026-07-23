## LDSETP
_ARM A64 Instruction_

**Title**: LDSETP, LDSETPA, LDSETPAL, LDSETPL -- A64 | **Class**: `general` | **XML ID**: `LDSETP`

**Architecture**: `FEAT_LSE128` (ARMv9.4)

**Summary**: Atomic bit set on quadword in memory

**Description**:
This instruction atomically loads a 128-bit quadword from memory,
performs a bitwise OR with the value held in a pair of registers on it, and stores the result
back to memory. The value initially loaded from memory is returned in the same pair of
registers.

### Variant: `Integer (LDSETP_128_memop_128)` (LDSETP)
- **Condition**: `A == 0 && R == 0`
- **Assembly**: `LDSETP  <Xt1>, <Xt2>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   0   011001 A   R   1   Rt2 0   011 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop_128.LDSETP_128_memop_128)

```
if !IsFeatureImplemented(FEAT_LSE128) then EndOfDecode(Decode_UNDEF);
if Rt  == '11111' then EndOfDecode(Decode_UNDEF);
if Rt2 == '11111' then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant boolean acquire = A == '1';
constant boolean release = R == '1';
constant boolean tagchecked = n != 31;

boolean rt_unknown = FALSE;

if t == t2 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_LSE128OVERLAP);
    assert c IN {Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_UNKNOWN    rt_unknown = TRUE;    // result is UNKNOWN
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.memop_128.LDSETP_128_memop_128)

```
bits(64) address;
constant bits(64) value1 = X[t, 64];
constant bits(64) value2 = X[t2, 64];
bits(128) data;
bits(128) store_value;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescAtomicOp(MemAtomicOp_ORR, acquire, release,
                                                          tagchecked, privileged);
if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

store_value = if BigEndian(accdesc.acctype) then value1:value2 else value2:value1;

constant bits(128) comparevalue = bits(128) UNKNOWN; // Irrelevant when not executing CAS
data = MemAtomic(address, comparevalue, store_value, accdesc);

if rt_unknown then
    data = bits(128) UNKNOWN;

if BigEndian(accdesc.acctype) then
    X[t, 64]  = data<127:64>;
    X[t2, 64] = data<63:0>;
else
    X[t, 64]  = data<63:0>;
    X[t2, 64] = data<127:64>;
```

#### Constraints
_2× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSE128)` |
| 🚫 ENCODING_UNDEF | `Rt != '11111'` |
| 🚫 ENCODING_UNDEF | `Rt2 != '11111'` |

### Variant: `Integer (LDSETPA_128_memop_128)` (LDSETPA)
- **Condition**: `A == 1 && R == 0`
- **Assembly**: `LDSETPA  <Xt1>, <Xt2>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   0   011001 A   R   1   Rt2 0   011 00  Rn  Rt  |
```

### Variant: `Integer (LDSETPAL_128_memop_128)` (LDSETPAL)
- **Condition**: `A == 1 && R == 1`
- **Assembly**: `LDSETPAL  <Xt1>, <Xt2>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   0   011001 A   R   1   Rt2 0   011 00  Rn  Rt  |
```

### Variant: `Integer (LDSETPL_128_memop_128)` (LDSETPL)
- **Condition**: `A == 0 && R == 1`
- **Assembly**: `LDSETPL  <Xt1>, <Xt2>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15 14  11   9   4  |
|--------------------------------------|
| 0   0   011001 A   R   1   Rt2 0   011 00  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xt2>` | `register (64-bit)` | `Rt2` | Is the 64-bit name of the second general-purpose register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ldsetp.xml`
</details>