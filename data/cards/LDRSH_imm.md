## LDRSH
_ARM A64 Instruction_

**Title**: LDRSH (immediate) -- A64 | **Class**: `general` | **XML ID**: `LDRSH_imm`

**Summary**: Load register signed halfword (immediate)

**Description**:
This instruction loads a halfword from
memory, sign-extends it to 32 bits or 64 bits, and writes the result
to a register.
The address that is used for the load is calculated from a
base register and an immediate offset.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Post-index (LDRSH_32_ldst_immpost)` (32-bit)
- **Condition**: `opc == 11`
- **Assembly**: `LDRSH  <Wt>, [<Xn|SP>], #<simm>`
- **Fixed bits**: `opc`=`1`
- **Bit Pattern**: `??????????????????????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 01  111 0   00  1x  0   imm9 01  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_immpost.LDRSH_32_ldst_immpost)

```
boolean wback = TRUE;
constant boolean postindex = TRUE;
constant bits(64) offset = SignExtend(imm9, 64);
```

#### Postdecode (A64.ldst.ldst_immpost.LDRSH_32_ldst_immpost)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer regsize = 64 >> UInt(opc<0>);
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;

Constraint c;
boolean wb_unknown = FALSE;
if wback && n == t && n != 31 then
    c = ConstrainUnpredictable(Unpredictable_WBOVERLAPLD);
    assert c IN {Constraint_WBSUPPRESS, Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_WBSUPPRESS wback = FALSE;       // Writeback is suppressed
        when Constraint_UNKNOWN    wb_unknown = TRUE;   // Writeback is UNKNOWN
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.ldst_immpost.LDRSH_32_ldst_immpost)

```
bits(64) address;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_LOAD, nontemporal, privileged,
                                                     tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

if !postindex then
    address = AddressAdd(address, offset, accdesc);

constant bits(16) data = Mem[address, 2, accdesc];
X[t, regsize] = SignExtend(data, regsize);

if wback then
    if wb_unknown then
        address = bits(64) UNKNOWN;
    elsif postindex then
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

### Variant: `Post-index (LDRSH_64_ldst_immpost)` (64-bit)
- **Condition**: `opc == 10`
- **Assembly**: `LDRSH  <Xt>, [<Xn|SP>], #<simm>`
- **Fixed bits**: `opc`=`0`
- **Bit Pattern**: `??????????????????????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 01  111 0   00  1x  0   imm9 01  Rn  Rt  |
```

### Variant: `Pre-index (LDRSH_32_ldst_immpre)` (32-bit)
- **Condition**: `opc == 11`
- **Assembly**: `LDRSH  <Wt>, [<Xn|SP>, #<simm>]!`
- **Fixed bits**: `opc`=`1`
- **Bit Pattern**: `??????????????????????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 01  111 0   00  1x  0   imm9 11  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_immpre.LDRSH_32_ldst_immpre)

```
boolean wback = TRUE;
constant boolean postindex = FALSE;
constant bits(64) offset = SignExtend(imm9, 64);
```

### Variant: `Pre-index (LDRSH_64_ldst_immpre)` (64-bit)
- **Condition**: `opc == 10`
- **Assembly**: `LDRSH  <Xt>, [<Xn|SP>, #<simm>]!`
- **Fixed bits**: `opc`=`0`
- **Bit Pattern**: `??????????????????????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  11   9   4  |
|--------------------------------|
| 01  111 0   00  1x  0   imm9 11  Rn  Rt  |
```

### Variant: `Unsigned offset (LDRSH_32_ldst_pos)` (32-bit)
- **Condition**: `opc == 11`
- **Assembly**: `LDRSH  <Wt>, [<Xn|SP>{, #<pimm>}]`
- **Fixed bits**: `opc`=`1`
- **Bit Pattern**: `??????????????????????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21   9   4  |
|--------------------------|
| 01  111 0   01  1x  imm12 Rn  Rt  |
```

#### Decode (A64.ldst.ldst_pos.LDRSH_32_ldst_pos)

```
boolean wback = FALSE;
constant boolean postindex = FALSE;
constant bits(64) offset = LSL(ZeroExtend(imm12, 64), 1);
```

### Variant: `Unsigned offset (LDRSH_64_ldst_pos)` (64-bit)
- **Condition**: `opc == 10`
- **Assembly**: `LDRSH  <Xt>, [<Xn|SP>{, #<pimm>}]`
- **Fixed bits**: `opc`=`0`
- **Bit Pattern**: `??????????????????????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21   9   4  |
|--------------------------|
| 01  111 0   01  1x  imm12 Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm9` | Is the signed immediate byte offset, in the range -256 to 255, encoded in the "imm9" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<pimm>` | `immediate` | `imm12` | Is the optional positive immediate byte offset, a multiple of 2 in the range 0 to 8190, defaulting to 0 and encoded in the "imm12" field as <pimm>/2. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ldrsh_imm.xml`
</details>