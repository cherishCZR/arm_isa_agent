## ADR
_ARM A64 Instruction_

**Title**: ADR -- A64 | **Class**: `general` | **XML ID**: `ADR`

**Summary**: Form PC-relative address

**Description**:
This instruction adds an immediate value to the PC value to form a
PC-relative address, and writes the result to the destination register.

### Variant: `Literal`
- **Assembly**: `ADR  <Xd>, <label>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  25  23   4  |
|--------------------|
| 0   immlo 100 00  immhi Rd  |
```

#### Decode (A64.dpimm.pcreladdr.ADR_only_pcreladdr)

```
constant integer d = UInt(Rd);
constant bits(64) imm = SignExtend(immhi:immlo, 64);
```

#### Execute (A64.dpimm.pcreladdr.ADR_only_pcreladdr)

```
X[d, 64] = PC64 + imm;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<label>` | `label` | `immhi:immlo` | Is the program label whose address is to be calculated. Its offset from the address of this instruction, in the range +/-1MB, is encoded in "immhi:imm |

---
<details><summary>Metadata</summary>

- address-form: `literal`
- isa: `A64`
- offset-type: `off19s`
- source: `adr.xml`
</details>