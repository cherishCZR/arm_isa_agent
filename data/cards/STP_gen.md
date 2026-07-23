## STP
_ARM A64 Instruction_

**Title**: STP -- A64 | **Class**: `general` | **XML ID**: `STP_gen`

**Summary**: Store pair of registers

**Description**:
This instruction calculates an
address from a base register value and an immediate offset,
and stores two 32-bit words or
two 64-bit doublewords to the calculated address,
from two registers.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Post-index (STP_32_ldstpair_post)` (32-bit)
- **Condition**: `opc == 00`
- **Assembly**: `STP  <Wt1>, <Wt2>, [<Xn|SP>], #<imm>`
- **Fixed bits**: `opc`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| x0  101 0   001 0   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_post.STP_32_ldstpair_post)

```
constant boolean wback = TRUE;
constant boolean postindex = TRUE;
```

#### Postdecode (A64.ldst.ldstpair_post.STP_32_ldstpair_post)

```
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant boolean nontemporal = FALSE;
constant integer scale = 2 + UInt(opc<1>);
constant integer datasize = 8 << scale;
constant bits(64) offset = LSL(SignExtend(imm7, 64), scale);
constant boolean tagchecked = wback || n != 31;

boolean rt_unknown = FALSE;
if wback && (t == n || t2 == n) && n != 31 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_WBOVERLAPST);
    assert c IN {Constraint_NONE, Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_NONE       rt_unknown = FALSE;   // Value stored is pre-writeback
        when Constraint_UNKNOWN    rt_unknown = TRUE;    // Value stored is UNKNOWN
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.ldstpair_post.STP_32_ldstpair_post)

```
bits(64) address;
bits(64) address2;
bits(datasize) data1;
bits(datasize) data2;
constant integer dbytes = datasize DIV 8;

constant boolean privileged = PSTATE.EL != EL0;
constant boolean ispair = IsFeatureImplemented(FEAT_LSE2);

constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_STORE, nontemporal, privileged,
                                                     tagchecked, ispair);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

if !postindex then
    address = AddressAdd(address, offset, accdesc);

if rt_unknown && t == n then
    data1 = bits(datasize) UNKNOWN;
else
    data1 = X[t, datasize];
if rt_unknown && t2 == n then
    data2 = bits(datasize) UNKNOWN;
else
    data2 = X[t2, datasize];

if accdesc.ispair then
    constant bits(2*datasize) full_data = (if BigEndian(accdesc.acctype) then data1:data2
                                                 else data2:data1);
    Mem[address, 2 * dbytes, accdesc] = full_data;
else
    address2 = AddressIncrement(address, dbytes, accdesc);
    Mem[address , dbytes, accdesc] = data1;
    Mem[address2, dbytes, accdesc] = data2;

if wback then
    if postindex then
        address = AddressAdd(address, offset, accdesc);
    if n == 31 then
        SP[64] = address;
    else
        X[n, 64] = address;
```

### Variant: `Post-index (STP_64_ldstpair_post)` (64-bit)
- **Condition**: `opc == 10`
- **Assembly**: `STP  <Xt1>, <Xt2>, [<Xn|SP>], #<imm>`
- **Fixed bits**: `opc`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| x0  101 0   001 0   imm7 Rt2 Rn  Rt  |
```

### Variant: `Pre-index (STP_32_ldstpair_pre)` (32-bit)
- **Condition**: `opc == 00`
- **Assembly**: `STP  <Wt1>, <Wt2>, [<Xn|SP>, #<imm>]!`
- **Fixed bits**: `opc`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| x0  101 0   011 0   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_pre.STP_32_ldstpair_pre)

```
constant boolean wback = TRUE;
constant boolean postindex = FALSE;
```

### Variant: `Pre-index (STP_64_ldstpair_pre)` (64-bit)
- **Condition**: `opc == 10`
- **Assembly**: `STP  <Xt1>, <Xt2>, [<Xn|SP>, #<imm>]!`
- **Fixed bits**: `opc`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| x0  101 0   011 0   imm7 Rt2 Rn  Rt  |
```

### Variant: `Signed offset (STP_32_ldstpair_off)` (32-bit)
- **Condition**: `opc == 00`
- **Assembly**: `STP  <Wt1>, <Wt2>, [<Xn|SP>{, #<imm>}]`
- **Fixed bits**: `opc`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| x0  101 0   010 0   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_off.STP_32_ldstpair_off)

```
constant boolean wback = FALSE;
constant boolean postindex = FALSE;
```

### Variant: `Signed offset (STP_64_ldstpair_off)` (64-bit)
- **Condition**: `opc == 10`
- **Assembly**: `STP  <Xt1>, <Xt2>, [<Xn|SP>{, #<imm>}]`
- **Fixed bits**: `opc`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| x0  101 0   010 0   imm7 Rt2 Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt1>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Wt2>` | `register (32-bit)` | `Rt2` | Is the 32-bit name of the second general-purpose register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `imm7` | For the "32-bit Post-index" and "32-bit Pre-index" variants: is the signed immediate byte offset, a multiple of 4 in the range -256 to 252, encoded in |
| `<imm>` | `immediate` | `imm7` | For the "64-bit Post-index" and "64-bit Pre-index" variants: is the signed immediate byte offset, a multiple of 8 in the range -512 to 504, encoded in |
| `<imm>` | `immediate` | `imm7` | For the "32-bit Signed offset" variant: is the optional signed immediate byte offset, a multiple of 4 in the range -256 to 252, defaulting to 0 and en |
| `<imm>` | `immediate` | `imm7` | For the "64-bit Signed offset" variant: is the optional signed immediate byte offset, a multiple of 8 in the range -512 to 504, defaulting to 0 and en |
| `<Xt1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xt2>` | `register (64-bit)` | `Rt2` | Is the 64-bit name of the second general-purpose register to be transferred, encoded in the "Rt2" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- offset-type: `off7s_s`
- source: `stp_gen.xml`
</details>