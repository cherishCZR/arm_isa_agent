## LDAPURSB
_ARM A64 Instruction_

**Title**: LDAPURSB -- A64 | **Class**: `general` | **XML ID**: `LDAPURSB`

**Architecture**: `FEAT_LRCPC2` (ARMv8.4)

**Summary**: Load-acquire RCpc register signed byte (unscaled)

**Description**:
This instruction calculates an
address from a base register and an immediate offset, loads a signed
byte from memory, sign-extends it, and writes it to a register.

The instruction has memory ordering semantics as described in
Load-Acquire, Load-AcquirePC, and Store-Release,
except that:

This difference in memory ordering is not described in the pseudocode.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Unscaled offset (LDAPURSB_32_ldapstl_unscaled)` (32-bit)
- **Condition**: `opc == 11`
- **Assembly**: `LDAPURSB  <Wt>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `opc`=`1`
- **Bit Pattern**: `??????????????????????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  23  21 20  11   9   4  |
|--------------------------|
| 00  011001 1x  0   imm9 00  Rn  Rt  |
```

#### Decode (A64.ldst.ldapstl_unscaled.LDAPURSB_32_ldapstl_unscaled)

```
if !IsFeatureImplemented(FEAT_LRCPC2) then EndOfDecode(Decode_UNDEF);
constant bits(64) offset = SignExtend(imm9, 64);
```

#### Postdecode (A64.ldst.ldapstl_unscaled.LDAPURSB_32_ldapstl_unscaled)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer datasize = 8;
constant integer regsize = 64 >> UInt(opc<0>);
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldapstl_unscaled.LDAPURSB_32_ldapstl_unscaled)

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
X[t, regsize] = SignExtend(data, regsize);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LRCPC2)` |

### Variant: `Unscaled offset (LDAPURSB_64_ldapstl_unscaled)` (64-bit)
- **Condition**: `opc == 10`
- **Assembly**: `LDAPURSB  <Xt>, [<Xn|SP>{, #<simm>}]`
- **Fixed bits**: `opc`=`0`
- **Bit Pattern**: `??????????????????????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  23  21 20  11   9   4  |
|--------------------------|
| 00  011001 1x  0   imm9 00  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<simm>` | `immediate` | `imm9` | Is the optional signed immediate byte offset, in the range -256 to 255, defaulting to 0 and encoded in the "imm9" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `base-plus-offset`
- isa: `A64`
- offset-type: `off9s_u`
- source: `ldapursb.xml`
</details>