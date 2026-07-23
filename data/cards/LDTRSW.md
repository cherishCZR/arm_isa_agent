## LDTRSW
_ARM A64 Instruction_

**Title**: LDTRSW -- A64 | **Class**: `general` | **XML ID**: `LDTRSW`

**Summary**: Load register signed word (unprivileged)

**Description**:
This instruction loads a word from memory,
sign-extends it to 64 bits, and writes the result to a register.
The address that is used for the load
is calculated from a base register and an immediate offset.

Explicit Memory  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

For information about addressing modes, see Load/Store addressing modes.

### Variant: `Unscaled offset`
- **Assembly**: `LDTRSW  <Xt>, [<Xn|SP>{, #<simm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23  21 20  11   9   4  |
|--------------------------------------|
| 10  11  1   0   0   0   10  0   imm9 10  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_unpriv.LDTRSW_64_ldst_unpriv)

```
constant bits(64) offset = SignExtend(imm9, 64);
```

#### Postdecode (A64.ldst.ldst_unpriv.LDTRSW_64_ldst_unpriv)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);

constant integer datasize = 32;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldst_unpriv.LDTRSW_64_ldst_unpriv)

```
bits(64) address;

constant boolean privileged = AArch64.IsUnprivAccessPriv();
constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_LOAD, nontemporal, privileged,
                                                     tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);

constant bits(datasize) data = Mem[address, datasize DIV 8, accdesc];
X[t, 64] = SignExtend(data, 64);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm9` | Is the optional signed immediate byte offset, in the range -256 to 255, defaulting to 0 and encoded in the "imm9" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `base-plus-offset`
- datatype: `64`
- isa: `A64`
- offset-type: `off9s_u`
- source: `ldtrsw.xml`
</details>