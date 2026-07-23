## LDR
_ARM A64 Instruction_

**Title**: LDR (register) -- A64 | **Class**: `general` | **XML ID**: `LDR_reg_gen`

**Summary**: Load register (register)

**Description**:
This instruction calculates an address from a base register
value and an offset register value, loads a word from memory, and
writes it to a register. The offset register value can optionally be
shifted and extended. For information about addressing modes, see
Load/Store addressing modes.

### Variant: `Integer (LDR_32_ldst_regoff)` (32-bit)
- **Condition**: `size == 10`
- **Assembly**: `LDR  <Wt>, [<Xn|SP>, (<Wm>|<Xm>){, <extend> {<amount>}}]`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  12 11   9   4  |
|--------------------------------------|
| 1x  111 0   00  01  1   Rm  option S   10  Rn  Rt  |
```

#### Decode (A64.ldst.ldst_regoff.LDR_32_ldst_regoff)

```
if option<1> == '0' then EndOfDecode(Decode_UNDEF);             // sub-word index
constant ExtendType extend_type = DecodeRegExtend(option);
constant integer scale = UInt(size);
constant integer shift = if S == '1' then scale else 0;
```

#### Postdecode (A64.ldst.ldst_regoff.LDR_32_ldst_regoff)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer m = UInt(Rm);
constant integer datasize = 8 << scale;
constant integer regsize = if datasize == 64 then 64 else 32;
constant boolean nontemporal = FALSE;
constant boolean tagchecked = TRUE;
```

#### Execute (A64.ldst.ldst_regoff.LDR_32_ldst_regoff)

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

constant bits(datasize) data = Mem[address, datasize DIV 8, accdesc];
X[t, regsize] = ZeroExtend(data, regsize);
```

#### Constraints
_1× 🚫 ENCODING_UNDEF_

| Type | Condition |
|---|---|
| 🚫 ENCODING_UNDEF | `option<1> != '0'` |

### Variant: `Integer (LDR_64_ldst_regoff)` (64-bit)
- **Condition**: `size == 11`
- **Assembly**: `LDR  <Xt>, [<Xn|SP>, (<Wm>|<Xm>){, <extend> {<amount>}}]`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  12 11   9   4  |
|--------------------------------------|
| 1x  111 0   00  01  1   Rm  option S   10  Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Wm>` | `register (32-bit)` | `Rm` | When option<0> is set to 0, is the 32-bit name of the general-purpose index register, encoded in the "Rm" field. |
| `<Xm>` | `register (64-bit)` | `Rm` | When option<0> is set to 1, is the 64-bit name of the general-purpose index register, encoded in the "Rm" field. |
| `<extend>` | `shift` | `option` | Is the index extend/shift specifier, defaulting to LSL, and which must be omitted for the LSL option when <amount> is omitted, |
| `<amount>` | `unknown` | `S` | For the "32-bit" variant: is the index shift amount, optional only when <extend> is not LSL. Where it is permitted to be optional, it defaults to #0.  |
| `<amount>` | `unknown` | `S` | For the "64-bit" variant: is the index shift amount, optional only when <extend> is not LSL. Where it is permitted to be optional, it defaults to #0.  |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |

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
| 1 | #2 |

**<amount> Value Table**:

| bitfield | symbol |
|---|---|
| 0 | #0 |
| 1 | #3 |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- isa: `A64`
- offset-type: `off-reg`
- source: `ldr_reg_gen.xml`
</details>