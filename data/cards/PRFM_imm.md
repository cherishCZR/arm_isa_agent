## PRFM
_ARM A64 Instruction_

**Title**: PRFM (immediate) -- A64 | **Class**: `general` | **XML ID**: `PRFM_imm`

**Summary**: Prefetch memory (immediate)

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

### Variant: `Unsigned offset`
- **Assembly**: `PRFM  (<prfop>|#<imm5>), [<Xn|SP>{, #<pimm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23  21   9   4  |
|--------------------------------|
| 11  11  1   0   0   1   10  imm12 Rn  Rt  |
```

#### Decode (A64.ldst.ldst_pos.PRFM_P_ldst_pos)

```
constant bits(64) offset = LSL(ZeroExtend(imm12, 64), 3);
constant integer n = UInt(Rn);
constant integer t = UInt(Rt);
constant boolean nontemporal = FALSE;
constant boolean tagchecked = FALSE;
```

#### Execute (A64.ldst.ldst_pos.PRFM_P_ldst_pos)

```
bits(64) address;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_PREFETCH, nontemporal, privileged,
                                                     tagchecked);

if n == 31 then
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);

Prefetch(address, t<4:0>);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<prfop>` | `unknown` | `Rt` | Is the prefetch operation, defined as <type><target><policy>.           <type> is one of:                                       PLD               Pref |
| `<imm5>` | `immediate` | `Rt` | Is the prefetch operation encoding as an immediate, in the range 0 to 31, encoded in the "Rt" field. This syntax is only for encodings that are not ac |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<pimm>` | `immediate` | `imm12` | Is the optional positive immediate byte offset, a multiple of 8 in the range 0 to 32760, defaulting to 0 and encoded in the "imm12" field as <pimm>/8. |

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
| 11000 |  |

---
<details><summary>Metadata</summary>

- address-form: `unsigned-scaled-offset`
- isa: `A64`
- offset-type: `off12u_s`
- source: `prfm_imm.xml`
</details>