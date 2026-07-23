## LDRA
_ARM A64 Instruction_

**Title**: LDRAA, LDRAB -- A64 | **Class**: `N/A` | **XML ID**: `LDRA`

**Architecture**: `FEAT_PAuth` (ARMv8.3)

**Summary**: Load register, with pointer authentication

**Description**:
This instruction authenticates an address from a base register using
a modifier of zero and the specified key, adds an immediate offset
to the authenticated address, and loads a 64-bit doubleword from
memory at this resulting address into a register.

Key A is used for LDRAA. Key B is used for LDRAB.

If the authentication passes, the PE behaves the same as for an LDR instruction.
For information on behavior if the authentication fails, see
Faulting on pointer authentication.

The authenticated address is not written back to the base register,
unless the pre-indexed variant of the instruction is used. In this
case, the address that is written back to the base register does not
include the pointer authentication code.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `PAC (LDRAA_64_ldst_pac)` (Key A, offset)
- **Condition**: `M == 0 && W == 0`
- **Assembly**: `LDRAA  <Xt>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `M`=`0`, `W`=`0`
- **Bit Pattern**: `???????????0???????????0????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  11 10  9   4  |
|--------------------------------------|
| 11  111 0   00  M   S   1   imm9 W   1   Rn  Rt  |
```

#### Decode (A64.ldst.ldst_pac.LDRAA_64_ldst_pac)

```
if !IsFeatureImplemented(FEAT_PAuth) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
boolean wback = W == '1';
constant boolean use_key_a = M == '0';
constant bits(10) S10 = S:imm9;
constant bits(64) offset = LSL(SignExtend(S10, 64), 3);
constant boolean nontemporal = FALSE;
constant boolean tagchecked = wback || n != 31;

boolean wb_unknown = FALSE;
if wback && n == t && n != 31 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_WBOVERLAPLD);
    assert c IN {Constraint_WBSUPPRESS, Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_WBSUPPRESS wback = FALSE;       // writeback is suppressed
        when Constraint_UNKNOWN    wb_unknown = TRUE;   // writeback is UNKNOWN
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.ldst_pac.LDRAA_64_ldst_pac)

```
bits(64) address;
constant boolean privileged = PSTATE.EL != EL0;
constant boolean auth_then_branch = TRUE;

constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_LOAD, nontemporal, privileged,
                                                     tagchecked);
if n == 31 then
    address = SP[64];
else
    address = X[n, 64];

if use_key_a then
    address = AuthDA(address, X[31, 64], auth_then_branch);
else
    address = AuthDB(address, X[31, 64], auth_then_branch);

if n == 31 then
    CheckSPAlignment();

address = AddressAdd(address, offset, accdesc);
X[t, 64] = Mem[address, 8, accdesc];

if wback then
    if wb_unknown then
        address = bits(64) UNKNOWN;
    if n == 31 then
        SP[64] = address;
    else
        X[n, 64] = address;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_PAuth)` |

### Variant: `PAC (LDRAA_64W_ldst_pac)` (Key A, pre-indexed)
- **Condition**: `M == 0 && W == 1`
- **Assembly**: `LDRAA  <Xt>, [<Xn|SP>{, #<simm>}]!`
- **Fixed bits**: `M`=`0`, `W`=`1`
- **Bit Pattern**: `???????????1???????????0????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  11 10  9   4  |
|--------------------------------------|
| 11  111 0   00  M   S   1   imm9 W   1   Rn  Rt  |
```

### Variant: `PAC (LDRAB_64_ldst_pac)` (Key B, offset)
- **Condition**: `M == 1 && W == 0`
- **Assembly**: `LDRAB  <Xt>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `M`=`1`, `W`=`0`
- **Bit Pattern**: `???????????0???????????1????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  11 10  9   4  |
|--------------------------------------|
| 11  111 0   00  M   S   1   imm9 W   1   Rn  Rt  |
```

### Variant: `PAC (LDRAB_64W_ldst_pac)` (Key B, pre-indexed)
- **Condition**: `M == 1 && W == 1`
- **Assembly**: `LDRAB  <Xt>, [<Xn|SP>{, #<simm>}]!`
- **Fixed bits**: `M`=`1`, `W`=`1`
- **Bit Pattern**: `???????????1???????????1????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23 22 21 20  11 10  9   4  |
|--------------------------------------|
| 11  111 0   00  M   S   1   imm9 W   1   Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `S:imm9` | Is the optional signed immediate byte offset, a multiple of 8 in the range -4096 to 4088, defaulting to 0 and encoded in the "S:imm9" field as <simm>/ |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `base-plus-offset`
- isa: `A64`
- offset-type: `off9s_u`
- source: `ldra.xml`
</details>