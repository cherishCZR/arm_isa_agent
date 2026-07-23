## LDAPURSW
_ARM A64 Instruction_

**Title**: LDAPURSW -- A64 | **Class**: `general` | **XML ID**: `LDAPURSW`

**Architecture**: `FEAT_LRCPC2` (ARMv8.4)

**Summary**: Load-acquire RCpc register signed word (unscaled)

**Description**:
This instruction calculates an
address from a base register and an immediate offset, loads a signed
word from memory, sign-extends it, and writes it to a register.

The instruction has memory ordering semantics as described in
Load-Acquire, Load-AcquirePC, and Store-Release,
except that:

This difference in memory ordering is not described in the pseudocode.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Unscaled offset`
- **Assembly**: `LDAPURSW  <Xt>, [<Xn|SP>{, #<simm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23  21 20  11   9   4  |
|--------------------------------------|
| 10  01  1   0   0   1   10  0   imm9 00  Rn  Rt  |
```

#### Decode (A64.ldst.ldapstl_unscaled.LDAPURSW_64_ldapstl_unscaled)

```
if !IsFeatureImplemented(FEAT_LRCPC2) then EndOfDecode(Decode_UNDEF);
constant bits(64) offset = SignExtend(imm9, 64);
```

#### Postdecode (A64.ldst.ldapstl_unscaled.LDAPURSW_64_ldapstl_unscaled)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer datasize = 32;
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldapstl_unscaled.LDAPURSW_64_ldapstl_unscaled)

```
bits(64) address;

constant AccessDescriptor accdesc = CreateAccDescLDAcqPC(tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);

constant bits(datasize) data = Mem[address, datasize DIV 8, accdesc];
X[t, 64] = SignExtend(data, 64);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LRCPC2)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm9` | Is the optional signed immediate byte offset, in the range -256 to 255, defaulting to 0 and encoded in the "imm9" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `base-plus-offset`
- datatype: `64`
- isa: `A64`
- offset-type: `off9s_u`
- source: `ldapursw.xml`
</details>