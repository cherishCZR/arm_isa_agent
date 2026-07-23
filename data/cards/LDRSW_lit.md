## LDRSW
_ARM A64 Instruction_

**Title**: LDRSW (literal) -- A64 | **Class**: `general` | **XML ID**: `LDRSW_lit`

**Summary**: Load register signed word (literal)

**Description**:
This instruction calculates an address
from the PC value and an immediate offset, loads a
word from memory, and
writes it to a register. For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Literal`
- **Assembly**: `LDRSW  <Xt>, <label>`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23   4  |
|--------------------------|
| 10  01  1   0   0   0   imm19 Rt  |
```

#### Decode (A64.ldst.loadlit.LDRSW_64_loadlit)

```
constant integer t = UInt(Rt);
constant boolean nontemporal = FALSE;
constant boolean tagchecked = FALSE;

constant bits(64) offset = SignExtend(imm19:'00', 64);
```

#### Execute (A64.ldst.loadlit.LDRSW_64_loadlit)

```
constant bits(64) address = PC64 + offset;
constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_LOAD, nontemporal, privileged,
                                                     tagchecked);

constant bits(32) data = Mem[address, 4, accdesc];
X[t, 64] = SignExtend(data, 64);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be loaded, encoded in the "Rt" field. |
| `<label>` | `label` | `imm19` | Is the program label from which the data is to be loaded. Its offset from the address of this instruction, in the range +/-1MB, is encoded as "imm19"  |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `literal`
- address-form-reg-type: `literal-64-reg`
- atomic-ops: `LDRSW-64-reg`
- isa: `A64`
- offset-type: `off19s`
- reg-type: `64-reg`
- source: `ldrsw_lit.xml`
</details>