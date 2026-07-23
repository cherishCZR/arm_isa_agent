## STILP
_ARM A64 Instruction_

**Title**: STILP -- A64 | **Class**: `general` | **XML ID**: `STILP`

**Architecture**: `FEAT_LRCPC3` (ARMv8.9)

**Summary**: Store-release ordered pair of registers

**Description**:
This instruction calculates an address from a base register value and an optional offset,
and stores two 32-bit words or two
64-bit doublewords to the calculated address, from two registers.
For information on single-copy atomicity and alignment requirements,
see Requirements for single-copy atomicity and
Alignment of data accesses.
The instruction also has memory ordering
semantics, as described in
Load-Acquire, Load-AcquirePC, and Store-Release, with the additional requirement that:

For information about addressing modes, see Load/Store addressing modes.

### Variant: `Integer (STILP_32SE_ldiappstilp)` (32-bit pre-index)
- **Condition**: `size == 10 && opc2 == 0000`
- **Assembly**: `STILP  <Wt1>, <Wt2>, [<Xn|SP>, #-8]!`
- **Fixed bits**: `size`=`0`, `opc2`=`0`
- **Bit Pattern**: `????????????0?????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15  11   9   4  |
|-----------------------------|
| 1x  0110010 0   0   Rt2 000x 10  Rn  Rt  |
```

#### Decode (A64.ldst.ldiappstilp.STILP_32SE_ldiappstilp)

```
if !IsFeatureImplemented(FEAT_LRCPC3) then EndOfDecode(Decode_UNDEF);
constant boolean ispair = TRUE;
constant boolean wback = opc2<0> == '0';
```

#### Postdecode (A64.ldst.ldiappstilp.STILP_32SE_ldiappstilp)

```
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant integer scale = 2 + UInt(size<0>);
constant integer datasize = 8 << scale;
constant integer offset = if opc2<0> == '0' then -1 * (2 << scale) else 0;
constant boolean tagchecked = wback || n != 31;

boolean rt_unknown = FALSE;

if wback && (t == n || t2 == n) && n != 31 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_WBOVERLAPST);
    assert c IN {Constraint_NONE, Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_NONE    rt_unknown = FALSE;   // value stored is pre-writeback
        when Constraint_UNKNOWN rt_unknown = TRUE;    // value stored is UNKNOWN
        when Constraint_UNDEF   EndOfDecode(Decode_UNDEF);
        when Constraint_NOP     EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.ldiappstilp.STILP_32SE_ldiappstilp)

```
bits(64) address;
bits(datasize) data1;
bits(datasize) data2;
constant integer dbytes = datasize DIV 8;
AccessDescriptor accdesc = CreateAccDescAcqRel(MemOp_STORE, tagchecked, ispair);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);

if rt_unknown && t == n then
    data1 = bits(datasize) UNKNOWN;
else
    data1 = X[t, datasize];
if rt_unknown && t2 == n then
    data2 = bits(datasize) UNKNOWN;
else
    data2 = X[t2, datasize];

bits(2*datasize) full_data;
if BigEndian(accdesc.acctype) then
    full_data = data1:data2;
else
    full_data = data2:data1;
accdesc.highestaddressfirst = offset < 0;
Mem[address, 2*dbytes, accdesc] = full_data;

if wback then
    if n == 31 then
        SP[64] = address;
    else
        X[n, 64] = address;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LRCPC3)` |

### Variant: `Integer (STILP_32S_ldiappstilp)` (32-bit)
- **Condition**: `size == 10 && opc2 == 0001`
- **Assembly**: `STILP  <Wt1>, <Wt2>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `opc2`=`1`
- **Bit Pattern**: `????????????1?????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15  11   9   4  |
|-----------------------------|
| 1x  0110010 0   0   Rt2 000x 10  Rn  Rt  |
```

### Variant: `Integer (STILP_64SS_ldiappstilp)` (64-bit pre-index)
- **Condition**: `size == 11 && opc2 == 0000`
- **Assembly**: `STILP  <Xt1>, <Xt2>, [<Xn|SP>, #-16]!`
- **Fixed bits**: `size`=`1`, `opc2`=`0`
- **Bit Pattern**: `????????????0?????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15  11   9   4  |
|-----------------------------|
| 1x  0110010 0   0   Rt2 000x 10  Rn  Rt  |
```

### Variant: `Integer (STILP_64S_ldiappstilp)` (64-bit)
- **Condition**: `size == 11 && opc2 == 0001`
- **Assembly**: `STILP  <Xt1>, <Xt2>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `opc2`=`1`
- **Bit Pattern**: `????????????1?????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15  11   9   4  |
|-----------------------------|
| 1x  0110010 0   0   Rt2 000x 10  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt1>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Wt2>` | `register (32-bit)` | `Rt2` | Is the 32-bit name of the second general-purpose register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Xt1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xt2>` | `register (64-bit)` | `Rt2` | Is the 64-bit name of the second general-purpose register to be transferred, encoded in the "Rt2" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `stilp.xml`
</details>