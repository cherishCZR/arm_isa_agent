## STURH
_ARM A64 Instruction_

**Title**: STURH -- A64 | **Class**: `general` | **XML ID**: `STURH`

**Summary**: Store register halfword (unscaled)

**Description**:
This instruction calculates an
address from a base register value and an immediate offset,
and stores a halfword to the calculated address,
from a 32-bit register.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Unscaled offset`
- **Assembly**: `STURH  <Wt>, [<Xn|SP>{, #<simm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23  21 20  11   9   4  |
|--------------------------------------|
| 01  11  1   0   0   0   00  0   imm9 00  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_unscaled.STURH_32_ldst_unscaled)

```
constant bits(64) offset = SignExtend(imm9, 64);
```

#### Postdecode (A64.ldst.ldst_unscaled.STURH_32_ldst_unscaled)

```
constant integer n = UInt(Rn);
constant integer t = UInt(Rt);
constant integer datasize = 16;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldst_unscaled.STURH_32_ldst_unscaled)

```
bits(64) address;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_STORE, nontemporal, privileged,
                                                     tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);

Mem[address, datasize DIV 8, accdesc] = X[t, datasize];
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm9` | Is the optional signed immediate byte offset, in the range -256 to 255, defaulting to 0 and encoded in the "imm9" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `base-plus-offset`
- datatype: `32`
- isa: `A64`
- offset-type: `off9s_u`
- source: `sturh.xml`
</details>