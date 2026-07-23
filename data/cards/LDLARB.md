## LDLARB
_ARM A64 Instruction_

**Title**: LDLARB -- A64 | **Class**: `general` | **XML ID**: `LDLARB`

**Architecture**: `FEAT_LOR` (PROFILE_A)

**Summary**: Load LOAcquire register byte

**Description**:
This instruction loads a byte
from memory, zero-extends it and writes it to a register.
The instruction also has memory ordering
semantics as described in
Load LOAcquire, Store LORelease.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `No offset`
- **Assembly**: `LDLARB  <Wt>, [<Xn|SP>{, #0}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21 20  15 14   9   4  |
|-----------------------------------------|
| 00  00  1   0   0   01  1   0   (1)(1)(1)(1)(1) 0   (1)(1)(1)(1)(1) Rn  Rt  |
```

#### Decode (A64.ldst.ldstord.LDLARB_LR32_ldstord)

```
if !IsFeatureImplemented(FEAT_LOR) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldstord.LDLARB_LR32_ldstord)

```
bits(64) address;

constant AccessDescriptor accdesc = CreateAccDescLOR(MemOp_LOAD, tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

constant bits(8) data = Mem[address,  1, accdesc];
X[t, 32] = ZeroExtend(data, 32);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LOR)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `base-register`
- address-form-reg-type: `base-register-32-reg`
- atomic-ops: `LDLARB-32-reg`
- isa: `A64`
- reg-type: `32-reg`
- source: `ldlarb.xml`
</details>