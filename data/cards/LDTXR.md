## LDTXR
_ARM A64 Instruction_

**Title**: LDTXR -- A64 | **Class**: `general` | **XML ID**: `LDTXR`

**Architecture**: `FEAT_LSUI` (ARMv9.6)

**Summary**: Load unprivileged exclusive register

**Description**:
This instruction derives an address from a base register
value, loads a 32-bit word or a 64-bit doubleword from memory,
and writes it to
a register. The memory access is atomic.
The PE marks the physical address being accessed as an exclusive access.
This exclusive access mark is checked by Store Exclusive instructions. See
Synchronization and semaphores.

Explicit Memory  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `No offset (LDTXR_LR32_ldstexclr_unpriv)` (32-bit)
- **Condition**: `sz == 0`
- **Assembly**: `LDTXR  <Wt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `sz`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 1   sz  0010010 1   0   (1)(1)(1)(1)(1) 0   (1)(1)(1)(1)(1) Rn  Rt  |
```

#### Decode (A64.ldst.ldstexclr_unpriv.LDTXR_LR32_ldstexclr_unpriv)

```
if !IsFeatureImplemented(FEAT_LSUI) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);

constant integer elsize = 32 << UInt(sz);
constant integer regsize = if elsize == 64 then 64 else 32;
constant boolean acqrel = FALSE;
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldstexclr_unpriv.LDTXR_LR32_ldstexclr_unpriv)

```
bits(64) address;
bits(elsize) data;

constant integer dbytes = elsize DIV 8;
constant boolean privileged = AArch64.IsUnprivAccessPriv();
constant AccessDescriptor accdesc = CreateAccDescExLDST(MemOp_LOAD, acqrel, tagchecked,
                                                        privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

AArch64.SetExclusiveMonitors(address, dbytes);

data = Mem[address, dbytes, accdesc];
X[t, regsize] = ZeroExtend(data, regsize);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSUI)` |

### Variant: `No offset (LDTXR_LR64_ldstexclr_unpriv)` (64-bit)
- **Condition**: `sz == 1`
- **Assembly**: `LDTXR  <Xt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `sz`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 1   sz  0010010 1   0   (1)(1)(1)(1)(1) 0   (1)(1)(1)(1)(1) Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `base-register`
- isa: `A64`
- source: `ldtxr.xml`
</details>