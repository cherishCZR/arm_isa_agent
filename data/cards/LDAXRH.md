## LDAXRH
_ARM A64 Instruction_

**Title**: LDAXRH -- A64 | **Class**: `general` | **XML ID**: `LDAXRH`

**Summary**: Load-acquire exclusive register halfword

**Description**:
This instruction derives an address from a base register
value, loads a halfword from memory, zero-extends it and writes it to
a register. The memory access is atomic.
The PE marks the physical address being accessed as an exclusive access.
This exclusive access mark is checked by Store Exclusive instructions. See
Synchronization and semaphores.
The instruction also has memory ordering
semantics as described in
Load-Acquire, Store-Release.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `No offset`
- **Assembly**: `LDAXRH  <Wt>, [<Xn|SP>{, #0}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21 20  15 14   9   4  |
|-----------------------------------------|
| 01  00  1   0   0   00  1   0   (1)(1)(1)(1)(1) 1   (1)(1)(1)(1)(1) Rn  Rt  |
```

#### Decode (A64.ldst.ldstexclr.LDAXRH_LR32_ldstexclr)

```
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);

constant boolean acqrel = TRUE;
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.ldstexclr.LDAXRH_LR32_ldstexclr)

```
bits(64) address;
bits(16) data;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescExLDST(MemOp_LOAD, acqrel, tagchecked,
                                                        privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

AArch64.SetExclusiveMonitors(address, 2);

data = Mem[address, 2, accdesc];
X[t, 32] = ZeroExtend(data, 32);
```

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
- atomic-ops: `LDAXRH-32-reg`
- isa: `A64`
- reg-type: `32-reg`
- source: `ldaxrh.xml`
</details>