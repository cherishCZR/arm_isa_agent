## LDRH
_ARM A64 Instruction_

**Title**: LDRH (register) -- A64 | **Class**: `general` | **XML ID**: `LDRH_reg`

**Summary**: Load register halfword (register)

**Description**:
This instruction calculates an address from a base
register value and an offset register value, loads a halfword from
memory, zero-extends it, and writes it to a
register. For information about addressing modes, see
Load/Store addressing modes.

### Variant: `32-bit`
- **Assembly**: `LDRH  <Wt>, [<Xn|SP>, (<Wm>|<Xm>){, <extend> {<amount>}}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23  21 20  15  12 11   9   4  |
|--------------------------------------------|
| 01  11  1   0   0   0   01  1   Rm  option S   10  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_regoff.LDRH_32_ldst_regoff)

```
if option<1> == '0' then EndOfDecode(Decode_UNDEF);             // sub-word index
constant ExtendType extend_type = DecodeRegExtend(option);
constant integer shift = if S == '1' then 1 else 0;
```

#### Postdecode (A64.ldst.ldst_regoff.LDRH_32_ldst_regoff)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant boolean nontemporal = FALSE;
constant boolean tagchecked = TRUE;
```

#### Execute (A64.ldst.ldst_regoff.LDRH_32_ldst_regoff)

```
constant bits(64) offset = ExtendReg(m, extend_type, shift, 64);
bits(64) address;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_LOAD, nontemporal, privileged,
                                                     tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);

constant bits(16) data = Mem[address, 2, accdesc];
X[t, 32] = ZeroExtend(data, 32);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `option<1> != '0'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | When option<0> is set to 0, is the 32-bit name of the general-purpose index register, encoded in the "Rm" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | When option<0> is set to 1, is the 64-bit name of the general-purpose index register, encoded in the "Rm" field. |
| `<extend>` | `shift` | `option` | Is the index extend/shift specifier, defaulting to LSL, and which must be omitted for the LSL option when <amount> is omitted, |
| `<amount>` | `unknown` | `S` | Is the index shift amount, optional only when <extend> is not LSL. Where it is permitted to be optional, it defaults to #0. It is |

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
| 1 | #1 |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- datatype: `32`
- isa: `A64`
- offset-type: `off-reg`
- source: `ldrh_reg.xml`
</details>