## STTRB
_ARM A64 Instruction_

**Title**: STTRB -- A64 | **Class**: `general` | **XML ID**: `STTRB`

**Summary**: Store register byte (unprivileged)

**Description**:
This instruction stores a byte from a 32-bit register to memory.
The address that is used for the store is calculated
from a base register and an immediate offset.

Explicit Memory  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

For information about addressing modes, see Load/Store addressing modes.

### Variant: `Unscaled offset`
- **Assembly**: `STTRB  <Wt>, [<Xn|SP>{, #<simm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23  21 20  11   9   4  |
|--------------------------------------|
| 00  11  1   0   0   0   00  0   imm9 10  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_unpriv.STTRB_32_ldst_unpriv)

```
constant bits(64) offset = SignExtend(imm9, 64);
```

#### Postdecode (A64.ldst.ldst_unpriv.STTRB_32_ldst_unpriv)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);

constant integer datasize = 8;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldst_unpriv.STTRB_32_ldst_unpriv)

```
bits(64) address;

constant boolean privileged = AArch64.IsUnprivAccessPriv();
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
- source: `sttrb.xml`
</details>