## STR
_ARM A64 Instruction_

**Title**: STR (immediate) -- A64 | **Class**: `general` | **XML ID**: `STR_imm_gen`

**Summary**: Store register (immediate)

**Description**:
This instruction stores a word or a doubleword from a
register to memory. The address that is used for the store is
calculated from a base register and an immediate offset.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Post-index (STR_32_ldst_immpost)` (32-bit)
- **Condition**: `size == 10`
- **Assembly**: `STR  <Wt>, [<Xn|SP>], #<simm>`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 1x  111 0   00  00  0   imm9 01  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_immpost.STR_32_ldst_immpost)

```
constant boolean wback = TRUE;
constant boolean postindex = TRUE;
constant integer scale = UInt(size);
constant bits(64) offset = SignExtend(imm9, 64);
```

#### Postdecode (A64.ldst.ldst_immpost.STR_32_ldst_immpost)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer datasize = 8 << scale;
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

#### Execute (A64.ldst.ldst_immpost.STR_32_ldst_immpost)

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

bits(datasize) data;
if rt_unknown then
    data = bits(datasize) UNKNOWN;
else
    data = X[t, datasize];

Mem[address, datasize DIV 8, accdesc] = data;

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

### Variant: `Post-index (STR_64_ldst_immpost)` (64-bit)
- **Condition**: `size == 11`
- **Assembly**: `STR  <Xt>, [<Xn|SP>], #<simm>`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 1x  111 0   00  00  0   imm9 01  Rn  Rt  |
```

### Variant: `Pre-index (STR_32_ldst_immpre)` (32-bit)
- **Condition**: `size == 10`
- **Assembly**: `STR  <Wt>, [<Xn|SP>, #<simm>]!`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 1x  111 0   00  00  0   imm9 11  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_immpre.STR_32_ldst_immpre)

```
constant boolean wback = TRUE;
constant boolean postindex = FALSE;
constant integer scale = UInt(size);
constant bits(64) offset = SignExtend(imm9, 64);
```

### Variant: `Pre-index (STR_64_ldst_immpre)` (64-bit)
- **Condition**: `size == 11`
- **Assembly**: `STR  <Xt>, [<Xn|SP>, #<simm>]!`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 1x  111 0   00  00  0   imm9 11  Rn  Rt  |
```

### Variant: `Unsigned offset (STR_32_ldst_pos)` (32-bit)
- **Condition**: `size == 10`
- **Assembly**: `STR  <Wt>, [<Xn|SP>{, #<pimm>}]`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21   9   4  |
|--------------------------|
| 1x  111 0   01  00  imm12 Rn  Rt  |
```

#### Decode (A64.ldst.ldst_pos.STR_32_ldst_pos)

```
constant boolean wback = FALSE;
constant boolean postindex = FALSE;
constant integer scale = UInt(size);
constant bits(64) offset = LSL(ZeroExtend(imm12, 64), scale);
```

### Variant: `Unsigned offset (STR_64_ldst_pos)` (64-bit)
- **Condition**: `size == 11`
- **Assembly**: `STR  <Xt>, [<Xn|SP>{, #<pimm>}]`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21   9   4  |
|--------------------------|
| 1x  111 0   01  00  imm12 Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm9` | Is the signed immediate byte offset, in the range -256 to 255, encoded in the "imm9" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<pimm>` | `immediate` | `imm12` | For the "32-bit" variant: is the optional positive immediate byte offset, a multiple of 4 in the range 0 to 16380, defaulting to 0 and encoded in the  |
| `<pimm>` | `immediate` | `imm12` | For the "64-bit" variant: is the optional positive immediate byte offset, a multiple of 8 in the range 0 to 32760, defaulting to 0 and encoded in the  |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `str_imm_gen.xml`
</details>