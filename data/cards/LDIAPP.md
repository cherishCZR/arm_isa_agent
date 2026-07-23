## LDIAPP
_ARM A64 Instruction_

**Title**: LDIAPP -- A64 | **Class**: `general` | **XML ID**: `LDIAPP`

**Architecture**: `FEAT_LRCPC3` (ARMv8.9)

**Summary**: Load-Acquire RCpc ordered pair of registers

**Description**:
This instruction calculates an address from
a base register value and an optional offset, loads two 32-bit words or two 64-bit
doublewords from memory, and writes them to two registers.
For information on single-copy atomicity and alignment requirements,
see Requirements for single-copy atomicity and
Alignment of data accesses.
The instruction also has memory ordering
semantics, as described in
Load-Acquire, Load-AcquirePC, and Store-Release, except that:

For information about addressing modes, see Load/Store addressing modes.

### Variant: `Integer (LDIAPP_32LE_ldiappstilp)` (32-bit post-index)
- **Condition**: `size == 10 && opc2 == 0000`
- **Assembly**: `LDIAPP  <Wt1>, <Wt2>, [<Xn|SP>], #8`
- **Fixed bits**: `size`=`0`, `opc2`=`0`
- **Bit Pattern**: `????????????0?????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15  11   9   4  |
|-----------------------------|
| 1x  0110010 1   0   Rt2 000x 10  Rn  Rt  |
```

#### Decode (A64.ldst.ldiappstilp.LDIAPP_32LE_ldiappstilp)

```
if !IsFeatureImplemented(FEAT_LRCPC3) then EndOfDecode(Decode_UNDEF);
constant boolean ispair = TRUE;
constant boolean postindex = opc2<0> == '0';
boolean wback = opc2<0> == '0';
```

#### Postdecode (A64.ldst.ldiappstilp.LDIAPP_32LE_ldiappstilp)

```
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant integer scale = 2 + UInt(size<0>);
constant integer datasize = 8 << scale;
constant integer offset = if opc2<0> == '0' then (2 << scale) else 0;
constant boolean tagchecked = wback || n != 31;

boolean rt_unknown = FALSE;

boolean wb_unknown = FALSE;
if wback && (t == n || t2 == n) && n != 31 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_WBOVERLAPLD);
    assert c IN {Constraint_WBSUPPRESS, Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_WBSUPPRESS wback = FALSE;        // writeback is suppressed
        when Constraint_UNKNOWN    wb_unknown = TRUE;    // writeback is UNKNOWN
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);

if t == t2 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_LDPOVERLAP);
    assert c IN {Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_UNKNOWN rt_unknown = TRUE;    // result is UNKNOWN
        when Constraint_UNDEF   EndOfDecode(Decode_UNDEF);
        when Constraint_NOP     EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.ldiappstilp.LDIAPP_32LE_ldiappstilp)

```
bits(64) address;
bits(datasize) data1;
bits(datasize) data2;
constant integer dbytes = datasize DIV 8;
constant AccessDescriptor accdesc = CreateAccDescLDAcqPC(tagchecked, ispair);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

if !postindex then
    address = AddressAdd(address, offset, accdesc);

bits(2*datasize) full_data;
full_data = Mem[address, 2*dbytes, accdesc];
if BigEndian(accdesc.acctype) then
    data2 = full_data<(datasize-1):0>;
    data1 = full_data<(2*datasize-1):datasize>;
else
    data1 = full_data<(datasize-1):0>;
    data2 = full_data<(2*datasize-1):datasize>;

if rt_unknown then
    data1 = bits(datasize) UNKNOWN;
    data2 = bits(datasize) UNKNOWN;

X[t, datasize] = data1;
X[t2, datasize] = data2;

if wback then
    if wb_unknown then
        address = bits(64) UNKNOWN;
    elsif postindex then
        address = AddressAdd(address, offset, accdesc);
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

### Variant: `Integer (LDIAPP_32L_ldiappstilp)` (32-bit)
- **Condition**: `size == 10 && opc2 == 0001`
- **Assembly**: `LDIAPP  <Wt1>, <Wt2>, [<Xn|SP>]`
- **Fixed bits**: `size`=`0`, `opc2`=`1`
- **Bit Pattern**: `????????????1?????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15  11   9   4  |
|-----------------------------|
| 1x  0110010 1   0   Rt2 000x 10  Rn  Rt  |
```

### Variant: `Integer (LDIAPP_64LS_ldiappstilp)` (64-bit post-index)
- **Condition**: `size == 11 && opc2 == 0000`
- **Assembly**: `LDIAPP  <Xt1>, <Xt2>, [<Xn|SP>], #16`
- **Fixed bits**: `size`=`1`, `opc2`=`0`
- **Bit Pattern**: `????????????0?????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15  11   9   4  |
|-----------------------------|
| 1x  0110010 1   0   Rt2 000x 10  Rn  Rt  |
```

### Variant: `Integer (LDIAPP_64L_ldiappstilp)` (64-bit)
- **Condition**: `size == 11 && opc2 == 0001`
- **Assembly**: `LDIAPP  <Xt1>, <Xt2>, [<Xn|SP>]`
- **Fixed bits**: `size`=`1`, `opc2`=`1`
- **Bit Pattern**: `????????????1?????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15  11   9   4  |
|-----------------------------|
| 1x  0110010 1   0   Rt2 000x 10  Rn  Rt  |
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
- source: `ldiapp.xml`
</details>