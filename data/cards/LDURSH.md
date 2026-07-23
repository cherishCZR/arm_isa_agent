## LDURSH
_ARM A64 Instruction_

**Title**: LDURSH -- A64 | **Class**: `general` | **XML ID**: `LDURSH`

**Summary**: Load register signed halfword (unscaled)

**Description**:
This instruction calculates an
address from a base
register and an immediate offset, loads a signed halfword from memory,
sign-extends it, and writes it
to a register. For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Unscaled offset (LDURSH_32_ldst_unscaled)` (32-bit)
- **Condition**: `opc == 11`
- **Assembly**: `LDURSH  <Wt>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `opc`=`1`
- **Bit Pattern**: `??????????????????????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 01  111 0   00  1x  0   imm9 00  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_unscaled.LDURSH_32_ldst_unscaled)

```
constant bits(64) offset = SignExtend(imm9, 64);
```

#### Postdecode (A64.ldst.ldst_unscaled.LDURSH_32_ldst_unscaled)

```
constant integer n = UInt(Rn);
constant integer t = UInt(Rt);
constant integer datasize = 16;
constant integer regsize = 64 >> UInt(opc<0>);
constant boolean nontemporal = FALSE;
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldst_unscaled.LDURSH_32_ldst_unscaled)

```
bits(64) address;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_LOAD, nontemporal, privileged,
                                                     tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);

constant bits(datasize) data = Mem[address, datasize DIV 8, accdesc];
X[t, regsize] = SignExtend(data, regsize);
```

### Variant: `Unscaled offset (LDURSH_64_ldst_unscaled)` (64-bit)
- **Condition**: `opc == 10`
- **Assembly**: `LDURSH  <Xt>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `opc`=`0`
- **Bit Pattern**: `??????????????????????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 01  111 0   00  1x  0   imm9 00  Rn  Rt  |
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
- source: `ldursh.xml`
</details>