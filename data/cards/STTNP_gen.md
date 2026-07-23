## STTNP
_ARM A64 Instruction_

**Title**: STTNP -- A64 | **Class**: `general` | **XML ID**: `STTNP_gen`

**Architecture**: `FEAT_LSUI` (ARMv9.6)

**Summary**: Store unprivileged pair of registers, with non-temporal hint

**Description**:
This instruction
calculates an address from a base register value and an immediate offset,
and stores two 64-bit doublewords to the calculated address,
from two registers.
For information about addressing modes, see
Load/Store addressing modes.
For information about non-temporal pair instructions, see
Load/Store non-temporal pair.

Explicit Memory  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

### Variant: `Signed offset`
- **Assembly**: `STTNP  <Xt1>, <Xt2>, [<Xn|SP>{, #<imm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 11  10  1   0   0   00  0   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstnapair_offs.STTNP_64_ldstnapair_offs)

```
if !IsFeatureImplemented(FEAT_LSUI) then EndOfDecode(Decode_UNDEF);

constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant boolean nontemporal = TRUE;
constant integer datasize = 64;
constant bits(64) offset = LSL(SignExtend(imm7, 64), 3);
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldstnapair_offs.STTNP_64_ldstnapair_offs)

```
bits(64) address;
bits(64) address2;
constant integer dbytes = datasize DIV 8;
constant boolean privileged = AArch64.IsUnprivAccessPriv();
constant AccessDescriptor accdesc = CreateAccDescGPR(MemOp_STORE, nontemporal, privileged,
                                                     tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);
address2 = AddressIncrement(address, dbytes, accdesc);
Mem[address , dbytes, accdesc] = X[t,  datasize];
Mem[address2, dbytes, accdesc] = X[t2, datasize];
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSUI)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xt2>` | `register (64-bit)` | `Rt2` | Is the 64-bit name of the second general-purpose register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `imm7` | Is the optional signed immediate byte offset, a multiple of 8 in the range -512 to 504, defaulting to 0 and encoded in the "imm7" field as <imm>/8. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `signed-scaled-offset`
- address-form-reg-type: `signed-scaled-offset-pair-64`
- atomic-ops: `STTNP-pair-64`
- isa: `A64`
- offset-type: `off7s_s`
- reg-type: `pair-64`
- source: `sttnp_gen.xml`
</details>