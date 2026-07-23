## STUR
_ARM A64 Instruction_

**Title**: STUR -- A64 | **Class**: `general` | **XML ID**: `STUR_gen`

**Summary**: Store register (unscaled)

**Description**:
This instruction calculates an address from a base register
value and an immediate offset, and stores a 32-bit word or
a 64-bit doubleword to the calculated address, from a register.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Unscaled offset (STUR_32_ldst_unscaled)` (32-bit)
- **Condition**: `size == 10`
- **Assembly**: `STUR  <Wt>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 1x  111 0   00  00  0   imm9 00  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_unscaled.STUR_32_ldst_unscaled)

```
constant integer scale = UInt(size);
constant bits(64) offset = SignExtend(imm9, 64);
```

#### Postdecode (A64.ldst.ldst_unscaled.STUR_32_ldst_unscaled)

```
constant integer n = UInt(Rn);
constant integer t = UInt(Rt);
constant integer datasize = 8 << scale;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldst_unscaled.STUR_32_ldst_unscaled)

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

### Variant: `Unscaled offset (STUR_64_ldst_unscaled)` (64-bit)
- **Condition**: `size == 11`
- **Assembly**: `STUR  <Xt>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 1x  111 0   00  00  0   imm9 00  Rn  Rt  |
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
- source: `stur_gen.xml`
</details>