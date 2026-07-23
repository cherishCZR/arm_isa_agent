## PRFM
_ARM A64 Instruction_

**Title**: PRFM (register) -- A64 | **Class**: `general` | **XML ID**: `PRFM_reg`

**Summary**: Prefetch memory (register)

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

### Variant: `Integer`
- **Assembly**: `PRFM  (<prfop>|#<imm5>), [<Xn|SP>, (<Wm>|<Xm>){, <extend> {<amount>}}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23  21 20  15  12 11   9   4  |
|--------------------------------------------|
| 11  11  1   0   0   0   10  1   Rm  x1x S   10  Rn  ?   |
```

#### Decode (A64.ldst.ldst_regoff.PRFM_P_ldst_regoff)

```
if option<1> == '0' then EndOfDecode(Decode_UNDEF);             // sub-word index
constant ExtendType extend_type = DecodeRegExtend(option);
constant integer shift = if S == '1' then 3 else 0;
constant integer n = UInt(Rn);
constant integer t = UInt(Rt);
constant integer m = UInt(Rm);
constant boolean nontemporal = FALSE;
constant boolean tagchecked = FALSE;
```

#### Execute (A64.ldst.ldst_regoff.PRFM_P_ldst_regoff)

```
bits(64) address;

constant bits(64) offset = ExtendReg(m, extend_type, shift, 64);
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

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `option<1> != '0'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<prfop>` | `unknown` | `Rt` | Is the prefetch operation, defined as <type><target><policy>.           <type> is one of:                                       PLD               Pref |
| `<imm5>` | `immediate` | `Rt` | Is the prefetch operation encoding as an immediate, in the range 0 to 31, encoded in the "Rt" field. This syntax is only for encodings that are not ac |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | When option<0> is set to 0, is the 32-bit name of the general-purpose index register, encoded in the "Rm" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | When option<0> is set to 1, is the 64-bit name of the general-purpose index register, encoded in the "Rm" field. |
| `<extend>` | `shift` | `option` | Is the index extend/shift specifier, defaulting to LSL, and which must be omitted for the LSL option when <amount> is omitted, |
| `<amount>` | `unknown` | `S` | Is the index shift amount, optional only when <extend> is not LSL. Where it is permitted to be optional, it defaults to #0. It is |

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

**<extend> Value Table**:

| bitfield | symbol |
|---|---|
| 010 | UXTW |
| 011 | LSL |
| 110 | SXTW |
| 111 | SXTX |

**<amount> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | #0 |
| 1 | #3 |

---
<details><summary>Metadata</summary>

- isa: `A64`
- offset-type: `off-reg`
- source: `prfm_reg.xml`
</details>