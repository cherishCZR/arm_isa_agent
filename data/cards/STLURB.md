## STLURB
_ARM A64 Instruction_

**Title**: STLURB -- A64 | **Class**: `general` | **XML ID**: `STLURB`

**Architecture**: `FEAT_LRCPC2` (ARMv8.4)

**Summary**: Store-release register byte (unscaled)

**Description**:
This instruction calculates an
address from a base register value and an immediate offset,
and stores a byte to the calculated address, from a 32-bit register.

The instruction has memory ordering semantics as described in
Load-Acquire, Load-AcquirePC, and Store-Release

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Unscaled offset`
- **Assembly**: `STLURB  <Wt>, [<Xn|SP>{, #<simm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23  21 20  11   9   4  |
|--------------------------------------|
| 00  01  1   0   0   1   00  0   imm9 00  Rn  Rt  |
```

#### Decode (A64.ldst.ldapstl_unscaled.STLURB_32_ldapstl_unscaled)

```
if !IsFeatureImplemented(FEAT_LRCPC2) then EndOfDecode(Decode_UNDEF);
constant bits(64) offset = SignExtend(imm9, 64);
constant integer n = UInt(Rn);
constant integer t = UInt(Rt);

constant integer datasize = 8;
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldapstl_unscaled.STLURB_32_ldapstl_unscaled)

```
bits(64) address;

constant AccessDescriptor accdesc = CreateAccDescAcqRel(MemOp_STORE, tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);

Mem[address, datasize DIV 8, accdesc] = X[t, datasize];
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LRCPC2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm9` | Is the optional signed immediate byte offset, in the range -256 to 255, defaulting to 0 and encoded in the "imm9" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `base-plus-offset`
- datatype: `32`
- isa: `A64`
- offset-type: `off9s_u`
- source: `stlurb.xml`
</details>