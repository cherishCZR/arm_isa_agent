## LDPSW
_ARM A64 Instruction_

**Title**: LDPSW -- A64 | **Class**: `general` | **XML ID**: `LDPSW`

**Summary**: Load pair of registers signed word

**Description**:
This instruction calculates an
address from a base register value and an immediate offset,
loads two 32-bit words from memory,
sign-extends them, and writes them to
two registers.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Post-index`
- **Assembly**: `LDPSW  <Xt1>, <Xt2>, [<Xn|SP>], #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 01  10  1   0   0   01  1   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_post.LDPSW_64_ldstpair_post)

```
boolean wback = TRUE;
constant boolean postindex = TRUE;
```

#### Postdecode (A64.ldst.ldstpair_post.LDPSW_64_ldstpair_post)

```
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant boolean nontemporal = FALSE;
constant integer scale = 2 + UInt(opc<1>);
constant integer datasize = 32;
constant bits(64) offset = LSL(SignExtend(imm7, 64), scale);
constant boolean tagchecked = wback || n != 31;

boolean rt_unknown = FALSE;
boolean wb_unknown = FALSE;

if wback && (t == n || t2 == n) && n != 31 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_WBOVERLAPLD);
    assert c IN {Constraint_WBSUPPRESS, Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_WBSUPPRESS wback = FALSE;        // Writeback is suppressed
        when Constraint_UNKNOWN    wb_unknown = TRUE;    // Writeback is UNKNOWN
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);

if t == t2 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_LDPOVERLAP);
    assert c IN {Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_UNKNOWN    rt_unknown = TRUE;    // Result is UNKNOWN
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.ldstpair_post.LDPSW_64_ldstpair_post)

```
bits(64) address;
bits(64) address2;
bits(datasize) data1;
bits(datasize) data2;
constant integer dbytes = datasize DIV 8;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_LOAD, nontemporal, privileged,
                                                     tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

if !postindex then
    address = AddressAdd(address, offset, accdesc);

address2 = AddressIncrement(address, dbytes, accdesc);
data1 = Mem[address , dbytes, accdesc];
data2 = Mem[address2, dbytes, accdesc];

if rt_unknown then
    data1 = bits(datasize) UNKNOWN;
    data2 = bits(datasize) UNKNOWN;

X[t,  64] = SignExtend(data1, 64);
X[t2, 64] = SignExtend(data2, 64);

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

### Variant: `Pre-index`
- **Assembly**: `LDPSW  <Xt1>, <Xt2>, [<Xn|SP>, #<imm>]!`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 01  10  1   0   0   11  1   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_pre.LDPSW_64_ldstpair_pre)

```
boolean wback = TRUE;
constant boolean postindex = FALSE;
```

### Variant: `Signed offset`
- **Assembly**: `LDPSW  <Xt1>, <Xt2>, [<Xn|SP>{, #<imm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 01  10  1   0   0   10  1   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_off.LDPSW_64_ldstpair_off)

```
boolean wback = FALSE;
constant boolean postindex = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xt2>` | `register (64-bit)` | `Rt2` | Is the 64-bit name of the second general-purpose register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `imm7` | For the "Post-index" and "Pre-index" variants: is the signed immediate byte offset, a multiple of 4 in the range -256 to 252, encoded in the "imm7" fi |
| `<imm>` | `immediate` | `imm7` | For the "Signed offset" variant: is the optional signed immediate byte offset, a multiple of 4 in the range -256 to 252, defaulting to 0 and encoded i |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- atomic-ops: `LDPSW-pair-64`
- isa: `A64`
- offset-type: `off7s_s`
- reg-type: `pair-64`
- source: `ldpsw.xml`
</details>