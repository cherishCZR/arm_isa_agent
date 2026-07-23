## LDR
_ARM A64 Instruction_

**Title**: LDR (literal) -- A64 | **Class**: `general` | **XML ID**: `LDR_lit_gen`

**Summary**: Load register (literal)

**Description**:
This instruction calculates an address from the PC value and
an immediate offset, loads a word from memory, and writes it to a
register. For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Literal (LDR_32_loadlit)` (32-bit)
- **Condition**: `opc == 00`
- **Assembly**: `LDR  <Wt>, <label>`
- **Fixed bits**: `opc`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23   4  |
|--------------------|
| 0x  011 0   00  imm19 Rt  |
```

#### Decode (A64.ldst.loadlit.LDR_32_loadlit)

```
constant integer t = UInt(Rt);
constant integer size = 4 << UInt(opc<0>);
constant boolean nontemporal = FALSE;
constant boolean tagchecked = FALSE;

constant bits(64) offset = SignExtend(imm19:'00', 64);
```

#### Execute (A64.ldst.loadlit.LDR_32_loadlit)

```
constant bits(64) address = PC64 + offset;
constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_LOAD, nontemporal, privileged,
                                                     tagchecked);

X[t, size * 8] = Mem[address, size, accdesc];
```

### Variant: `Literal (LDR_64_loadlit)` (64-bit)
- **Condition**: `opc == 01`
- **Assembly**: `LDR  <Xt>, <label>`
- **Fixed bits**: `opc`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23   4  |
|--------------------|
| 0x  011 0   00  imm19 Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |
| `<label>` | `label` | `imm19` | Is the program label from which the data is to be loaded. Its offset from the address of this instruction, in the range +/-1MB, is encoded as "imm19"  |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `literal`
- isa: `A64`
- offset-type: `off19s`
- source: `ldr_lit_gen.xml`
</details>