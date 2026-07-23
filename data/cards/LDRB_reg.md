## LDRB
_ARM A64 Instruction_

**Title**: LDRB (register) -- A64 | **Class**: `general` | **XML ID**: `LDRB_reg`

**Summary**: Load register byte (register)

**Description**:
This instruction calculates an address from a
base register value and an offset register value, loads a byte from
memory, zero-extends it, and writes it to a
register.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `32-bit (LDRB_32B_ldst_regoff)` (Extended register)
- **Condition**: `option != 011`
- **Assembly**: `LDRB  <Wt>, [<Xn|SP>, (<Wm>|<Xm>), <extend> {<amount>}]`
- **Fixed bits**: `option`=`ZNN`
- **Bit Pattern**: `????????????????????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  12 11   9   4  |
|--------------------------------------|
| 00  111 0   00  01  1   Rm  option S   10  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_regoff.LDRB_32B_ldst_regoff)

```
if option<1> == '0' then EndOfDecode(Decode_UNDEF);             // sub-word index
constant ExtendType extend_type = DecodeRegExtend(option);
constant integer shift = 0;
```

#### Postdecode (A64.ldst.ldst_regoff.LDRB_32B_ldst_regoff)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant boolean nontemporal = FALSE;
constant boolean tagchecked = TRUE;
```

#### Execute (A64.ldst.ldst_regoff.LDRB_32B_ldst_regoff)

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

constant bits(8) data = Mem[address, 1, accdesc];
X[t, 32] = ZeroExtend(data, 32);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `option<1> != '0'` |

### Variant: `32-bit (LDRB_32BL_ldst_regoff)` (Shifted register)
- **Condition**: `option == 011`
- **Assembly**: `LDRB  <Wt>, [<Xn|SP>, <Xm>{, LSL <amount>}]`
- **Fixed bits**: `option`=`011`
- **Bit Pattern**: `?????????????110????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  12 11   9   4  |
|--------------------------------------|
| 00  111 0   00  01  1   Rm  option S   10  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | When option<0> is set to 0, is the 32-bit name of the general-purpose index register, encoded in the "Rm" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | When option<0> is set to 1, is the 64-bit name of the general-purpose index register, encoded in the "Rm" field. |
| `<extend>` | `shift` | `option` | Is the index extend specifier, |
| `<amount>` | `unknown` | `S` | Is the index shift amount, it must be #0, encoded in "S" as 0 if omitted, or as 1 if present. |

**<extend> Value Table**:

| bitfield | symbol |
|---|---|
| 010 | UXTW |
| 110 | SXTW |
| 111 | SXTX |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- datatype: `32`
- isa: `A64`
- offset-type: `off-reg`
- source: `ldrb_reg.xml`
</details>