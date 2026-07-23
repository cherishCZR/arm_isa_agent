## STNP
_ARM A64 Instruction_

**Title**: STNP -- A64 | **Class**: `general` | **XML ID**: `STNP_gen`

**Summary**: Store pair of registers, with non-temporal hint

**Description**:
This instruction
calculates an address from a base register value and an immediate offset,
and stores two 32-bit words or two 64-bit doublewords to the calculated address,
from two registers.
For information about addressing modes, see
Load/Store addressing modes.
For information about non-temporal pair instructions, see
Load/Store non-temporal pair.

### Variant: `Signed offset (STNP_32_ldstnapair_offs)` (32-bit)
- **Condition**: `opc == 00`
- **Assembly**: `STNP  <Wt1>, <Wt2>, [<Xn|SP>{, #<imm>}]`
- **Fixed bits**: `opc`=`0`
- **Bit Pattern**: `???????????????????????????????0`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| x0  101 0   000 0   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstnapair_offs.STNP_32_ldstnapair_offs)

```
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant boolean nontemporal = TRUE;
constant integer scale = 2 + UInt(opc<1>);
constant integer datasize = 8 << scale;
constant bits(64) offset = LSL(SignExtend(imm7, 64), scale);
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldstnapair_offs.STNP_32_ldstnapair_offs)

```
bits(64) address;
bits(64) address2;
constant integer dbytes = datasize DIV 8;
constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_STORE, nontemporal, privileged,
                                                     tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);
address2 = AddressIncrement(address, dbytes, accdesc);
Mem[address , dbytes, accdesc] = X[t,  datasize];
Mem[address2, dbytes, accdesc] = X[t2, datasize];
```

### Variant: `Signed offset (STNP_64_ldstnapair_offs)` (64-bit)
- **Condition**: `opc == 10`
- **Assembly**: `STNP  <Xt1>, <Xt2>, [<Xn|SP>{, #<imm>}]`
- **Fixed bits**: `opc`=`1`
- **Bit Pattern**: `???????????????????????????????1`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| x0  101 0   000 0   imm7 Rt2 Rn  Rt  |
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
- source: `stnp_gen.xml`
</details>