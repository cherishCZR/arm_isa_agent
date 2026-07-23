## PRFM
_ARM A64 Instruction_

**Title**: PRFM (literal) -- A64 | **Class**: `general` | **XML ID**: `PRFM_lit`

**Summary**: Prefetch memory (literal)

**Description**:
This instruction signals the memory system that data memory
accesses from a specified address are likely to occur in the near
future. The memory system can respond by taking actions that are
expected to speed up the memory accesses when they do occur, such as
making the cache line containing the specified address available at
the level of cache specified by the instruction.

The effect of a PRFM instruction is
IMPLEMENTATION DEFINED. For more information,
see Prefetch memory.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Literal`
- **Assembly**: `PRFM  (<prfop>|#<imm5>), <label>`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23   4  |
|--------------------------|
| 11  01  1   0   0   0   imm19 Rt  |
```

#### Decode (A64.ldst.loadlit.PRFM_P_loadlit)

```
constant integer t = UInt(Rt);

constant bits(64) offset = SignExtend(imm19:'00', 64);
```

#### Execute (A64.ldst.loadlit.PRFM_P_loadlit)

```
constant bits(64) address = PC64 + offset;

Prefetch(address, t<4:0>);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<prfop>` | `unknown` | `Rt` | Is the prefetch operation, defined as <type><target><policy>.           <type> is one of:                                       PLD               Pref |
| `<imm5>` | `immediate` | `Rt` | Is the prefetch operation encoding as an immediate, in the range 0 to 31, encoded in the "Rt" field. This syntax is only for encodings that are not ac |
| `<label>` | `label` | `imm19` | Is the program label from which the data is to be loaded. Its offset from the address of this instruction, in the range +/-1MB, is encoded as "imm19"  |

**<prfop> Value Table**:

| bitfield | symbol |
|---|---|
| 00000 |  |
| 00001 |  |
| 00010 |  |
| 00011 |  |
| 00100 |  |
| 00101 |  |
| 00110 |  |
| 00111 |  |
| 01000 |  |
| 01001 |  |
| 01010 |  |
| 01011 |  |
| 01100 |  |
| 01101 |  |
| 01110 |  |
| 01111 |  |
| 10000 |  |
| 10001 |  |
| 10010 |  |
| 10011 |  |
| 10100 |  |
| 10101 |  |
| 10110 |  |
| 10111 |  |

---
<details><summary>Metadata</summary>

- address-form: `literal`
- isa: `A64`
- offset-type: `off19s`
- source: `prfm_lit.xml`
</details>