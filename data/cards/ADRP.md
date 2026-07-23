## ADRP
_ARM A64 Instruction_

**Title**: ADRP -- A64 | **Class**: `general` | **XML ID**: `ADRP`

**Summary**: Form PC-relative address to 4KB page

**Description**:
This instruction adds an immediate value that is
shifted left by 12 bits, to the PC value to form a PC-relative address,
with the bottom 12 bits masked out, and writes the result to the
destination register.

### Variant: `Literal`
- **Assembly**: `ADRP  <Xd>, <label>`
**Encoding Diagram (32-bit)**:

```text
| 31 30  28  25  23   4  |
|--------------------|
| 1   immlo 100 00  immhi Rd  |
```

#### Decode (A64.dpimm.pcreladdr.ADRP_only_pcreladdr)

```
constant integer d = UInt(Rd);
constant bits(64) imm = SignExtend(immhi:immlo:Zeros(12), 64);
```

#### Execute (A64.dpimm.pcreladdr.ADRP_only_pcreladdr)

```
constant bits(64) base = PC64<63:12>:Zeros(12);
X[d, 64] = base + imm;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | Is the 64-bit name of the general-purpose destination register, encoded in the "Rd" field. |
| `<label>` | `label` | `immhi:immlo` | Is the program label whose 4KB page address is to be calculated. Its offset from the page address of this instruction, in the range +/-4GB, is encoded |

---
<details><summary>Metadata</summary>

- address-form: `literal`
- isa: `A64`
- offset-type: `off19s`
- source: `adrp.xml`
</details>