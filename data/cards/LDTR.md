## LDTR
_ARM A64 Instruction_

**Title**: LDTR -- A64 | **Class**: `general` | **XML ID**: `LDTR`

**Summary**: Load register (unprivileged)

**Description**:
This instruction loads a word or doubleword from memory, and writes it
to a register. The address that is used for the load is calculated from a base register
and an immediate offset.

Explicit Memory  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

For information about addressing modes, see Load/Store addressing modes.

### Variant: `Unscaled offset (LDTR_32_ldst_unpriv)` (32-bit)
- **Condition**: `size == 10`
- **Assembly**: `LDTR  <Wt>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 1x  111 0   00  01  0   imm9 10  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_unpriv.LDTR_32_ldst_unpriv)

```
constant integer scale = UInt(size);
constant bits(64) offset = SignExtend(imm9, 64);
```

#### Postdecode (A64.ldst.ldst_unpriv.LDTR_32_ldst_unpriv)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);

constant integer datasize = 8 << scale;
constant integer regsize = if datasize == 64 then 64 else 32;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldst_unpriv.LDTR_32_ldst_unpriv)

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
X[t, regsize] = ZeroExtend(data, regsize);
```

### Variant: `Unscaled offset (LDTR_64_ldst_unpriv)` (64-bit)
- **Condition**: `size == 11`
- **Assembly**: `LDTR  <Xt>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 1x  111 0   00  01  0   imm9 10  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm9` | Is the optional signed immediate byte offset, in the range -256 to 255, defaulting to 0 and encoded in the "imm9" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `base-plus-offset`
- isa: `A64`
- offset-type: `off9s_u`
- source: `ldtr.xml`
</details>