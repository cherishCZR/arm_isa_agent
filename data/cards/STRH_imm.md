## STRH
_ARM A64 Instruction_

**Title**: STRH (immediate) -- A64 | **Class**: `general` | **XML ID**: `STRH_imm`

**Summary**: Store register halfword (immediate)

**Description**:
This instruction stores the least significant
halfword of a 32-bit register to memory. The address that is used
for the store is calculated from a base register and an immediate offset.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Post-index`
- **Assembly**: `STRH  <Wt>, [<Xn|SP>], #<simm>`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23  21 20  11   9   4  |
|--------------------------------------|
| 01  11  1   0   0   0   00  0   imm9 01  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_immpost.STRH_32_ldst_immpost)

```
constant boolean wback = TRUE;
constant boolean postindex = TRUE;
constant bits(64) offset = SignExtend(imm9, 64);
```

#### Postdecode (A64.ldst.ldst_immpost.STRH_32_ldst_immpost)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;

Constraint c;
boolean rt_unknown = FALSE;
if wback && n == t && n != 31 then
    c = ConstrainUnpredictable(Unpredictable_WBOVERLAPST);
    assert c IN {Constraint_NONE, Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_NONE    rt_unknown = FALSE;    // Value stored is original value
        when Constraint_UNKNOWN rt_unknown = TRUE;     // Value stored is UNKNOWN
        when Constraint_UNDEF   EndOfDecode(Decode_UNDEF);
        when Constraint_NOP     EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.ldst_immpost.STRH_32_ldst_immpost)

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

if !postindex then
    address = AddressAdd(address, offset, accdesc);

bits(16) data;
if rt_unknown then
    data = bits(16) UNKNOWN;
else
    data = X[t, 16];

Mem[address, 2, accdesc] = data;

if wback then
    if postindex then
        address = AddressAdd(address, offset, accdesc);
    if n == 31 then
        SP[64] = address;
    else
        X[n, 64] = address;
```

#### Constraints
_1× ⚠ CONSTRAINED_UNPREDICTABLE_

| Type | Condition |
|---|---|
| ⚠ CONSTRAINED_UNPREDICTABLE | `wback && n == t && n != 31` |

### Variant: `Pre-index`
- **Assembly**: `STRH  <Wt>, [<Xn|SP>, #<simm>]!`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23  21 20  11   9   4  |
|--------------------------------------|
| 01  11  1   0   0   0   00  0   imm9 11  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_immpre.STRH_32_ldst_immpre)

```
constant boolean wback = TRUE;
constant boolean postindex = FALSE;
constant bits(64) offset = SignExtend(imm9, 64);
```

### Variant: `Unsigned offset`
- **Assembly**: `STRH  <Wt>, [<Xn|SP>{, #<pimm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23  21   9   4  |
|--------------------------------|
| 01  11  1   0   0   1   00  imm12 Rn  Rt  |
```

#### Decode (A64.ldst.ldst_pos.STRH_32_ldst_pos)

```
constant boolean wback = FALSE;
constant boolean postindex = FALSE;
constant bits(64) offset = LSL(ZeroExtend(imm12, 64), 1);
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm9` | Is the signed immediate byte offset, in the range -256 to 255, encoded in the "imm9" field. |
| `<pimm>` | `immediate` | `imm12` | Is the optional positive immediate byte offset, a multiple of 2 in the range 0 to 8190, defaulting to 0 and encoded in the "imm12" field as <pimm>/2. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- datatype: `32`
- isa: `A64`
- source: `strh_imm.xml`
</details>