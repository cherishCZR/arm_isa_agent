## LDNP
_ARM A64 Instruction_

**Title**: LDNP -- A64 | **Class**: `general` | **XML ID**: `LDNP_gen`

**Summary**: Load pair of registers, with non-temporal hint

**Description**:
This instruction calculates an
address from a base register value and an immediate offset,
loads two 32-bit words or
two 64-bit doublewords from memory,
and writes them to
two registers.

For information about addressing modes, see
Load/Store addressing modes.
For information about non-temporal pair instructions, see
Load/Store non-temporal pair.

### Variant: `Signed offset (LDNP_32_ldstnapair_offs)` (32-bit)
- **Condition**: `opc == 00`
- **Assembly**: `LDNP  <Wt1>, <Wt2>, [<Xn|SP>{, #<imm>}]`
- **Fixed bits**: `opc`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| x0  101 0   000 1   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstnapair_offs.LDNP_32_ldstnapair_offs)

```
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant boolean nontemporal = TRUE;
constant integer scale = 2 + UInt(opc<1>);
constant integer datasize = 8 << scale;
constant bits(64) offset = LSL(SignExtend(imm7, 64), scale);
constant boolean tagchecked = n != 31;

boolean rt_unknown = FALSE;
if t == t2 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_LDPOVERLAP);
    assert c IN {Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_UNKNOWN    rt_unknown = TRUE;    // Result is UNKNOWN
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.ldstnapair_offs.LDNP_32_ldstnapair_offs)

```
bits(64) address;
bits(64) address2;
constant integer dbytes = datasize DIV 8;
bits(datasize) data1;
bits(datasize) data2;
constant boolean privileged = PSTATE.EL != EL0;
constant boolean ispair = IsFeatureImplemented(FEAT_LSE2);
constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_LOAD, nontemporal, privileged,
                                                     tagchecked, ispair);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);

if accdesc.ispair then
    constant bits(2*datasize) full_data = Mem[address, 2 * dbytes, accdesc];
    if BigEndian(accdesc.acctype) then
        data2 = full_data<(datasize-1):0>;
        data1 = full_data<(2*datasize-1):datasize>;
    else
        data1 = full_data<(datasize-1):0>;
        data2 = full_data<(2*datasize-1):datasize>;
else
    address2 = AddressIncrement(address, dbytes, accdesc);
    data1 = Mem[address , dbytes, accdesc];
    data2 = Mem[address2, dbytes, accdesc];
if rt_unknown then
    data1 = bits(datasize) UNKNOWN;
    data2 = bits(datasize) UNKNOWN;
X[t, datasize]  = data1;
X[t2, datasize] = data2;
```

### Variant: `Signed offset (LDNP_64_ldstnapair_offs)` (64-bit)
- **Condition**: `opc == 10`
- **Assembly**: `LDNP  <Xt1>, <Xt2>, [<Xn|SP>{, #<imm>}]`
- **Fixed bits**: `opc`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| x0  101 0   000 1   imm7 Rt2 Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt1>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Wt2>` | `register (32-bit)` | `Rt2` | Is the 32-bit name of the second general-purpose register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `imm7` | For the "32-bit" variant: is the optional signed immediate byte offset, a multiple of 4 in the range -256 to 252, defaulting to 0 and encoded in the " |
| `<imm>` | `immediate` | `imm7` | For the "64-bit" variant: is the optional signed immediate byte offset, a multiple of 8 in the range -512 to 504, defaulting to 0 and encoded in the " |
| `<Xt1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xt2>` | `register (64-bit)` | `Rt2` | Is the 64-bit name of the second general-purpose register to be transferred, encoded in the "Rt2" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `signed-scaled-offset`
- isa: `A64`
- offset-type: `off7s_s`
- source: `ldnp_gen.xml`
</details>