## PRFUM
_ARM A64 Instruction_

**Title**: PRFUM -- A64 | **Class**: `general` | **XML ID**: `PRFUM`

**Summary**: Prefetch memory (unscaled offset)

**Description**:
This instruction signals the memory system that
data memory accesses from a specified address are likely to occur in
the near future. The memory system can respond by taking actions that are
expected to speed up the memory accesses when they do occur, such as
making the cache line containing the specified address available at
the level of cache specified by the instruction.

The effect of a PRFUM instruction is
IMPLEMENTATION DEFINED. For more information,
see Prefetch memory.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Unscaled offset`
- **Assembly**: `PRFUM  (<prfop>|#<imm5>), [<Xn|SP>{, #<simm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23  21 20  11   9   4  |
|--------------------------------------|
| 11  11  1   0   0   0   10  0   imm9 00  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_unscaled.PRFUM_P_ldst_unscaled)

```
constant bits(64) offset = SignExtend(imm9, 64);
constant integer n = UInt(Rn);
constant integer t = UInt(Rt);
constant boolean nontemporal = FALSE;
constant boolean tagchecked = FALSE;
```

#### Execute (A64.ldst.ldst_unscaled.PRFUM_P_ldst_unscaled)

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
| `<simm>` | `immediate` | `imm9` | Is the optional signed immediate byte offset, in the range -256 to 255, defaulting to 0 and encoded in the "imm9" field. |

**<prfop> Value Table**:

| bitfield | symbol |
|---|---|
| 00000 | PLDL1KEEP |
| 00001 | PLDL1STRM |
| 00010 | PLDL2KEEP |
| 00011 | PLDL2STRM |
| 00100 | PLDL3KEEP |
| 00101 | PLDL3STRM |
| 01000 | PLIL1KEEP |
| 01001 | PLIL1STRM |
| 01010 | PLIL2KEEP |
| 01011 | PLIL2STRM |
| 01100 | PLIL3KEEP |
| 01101 | PLIL3STRM |
| 10000 | PSTL1KEEP |
| 10001 | PSTL1STRM |
| 10010 | PSTL2KEEP |
| 10011 | PSTL2STRM |
| 10100 | PSTL3KEEP |
| 10101 | PSTL3STRM |

---
<details><summary>Metadata</summary>

- address-form: `base-plus-offset`
- isa: `A64`
- offset-type: `off9s_u`
- source: `prfum.xml`
</details>