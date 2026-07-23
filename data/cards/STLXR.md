## STLXR
_ARM A64 Instruction_

**Title**: STLXR -- A64 | **Class**: `general` | **XML ID**: `STLXR`

**Summary**: Store-release exclusive register

**Description**:
This instruction
stores a 32-bit word or a 64-bit doubleword to
memory if the PE has exclusive access to the
memory address, and returns a status
value of 0 if the
store was successful, or of 1 if no store was performed.
See
Synchronization and semaphores.
The memory access is atomic.
The instruction also has memory ordering
semantics as described in
Load-Acquire, Store-Release.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `No offset (STLXR_SR32_ldstexclr)` (32-bit)
- **Condition**: `size == 10`
- **Assembly**: `STLXR  <Ws>, <Wt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `size`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 1x  0010000 0   0   Rs  1   (1)(1)(1)(1)(1) Rn  Rt  |
```

#### Decode (A64.ldst.ldstexclr.STLXR_SR32_ldstexclr)

```
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);

constant integer elsize = 8 << UInt(size);
constant boolean acqrel = TRUE;
constant boolean tagchecked = n != 31;

boolean rt_unknown = FALSE;
boolean rn_unknown = FALSE;
if s == t then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_DATAOVERLAP);
    assert c IN {Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_UNKNOWN    rt_unknown = TRUE;    // store UNKNOWN value
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);
if s == n && n != 31 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_BASEOVERLAP);
    assert c IN {Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_UNKNOWN    rn_unknown = TRUE;    // address is UNKNOWN
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.ldstexclr.STLXR_SR32_ldstexclr)

```
bits(64) address;
bits(elsize) data;

constant integer dbytes = elsize DIV 8;
constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescExLDST(MemOp_STORE, acqrel,
                                                        tagchecked, privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
elsif rn_unknown then
    address = bits(64) UNKNOWN;
else
    address = X[n, 64];

if rt_unknown then
    data = bits(elsize) UNKNOWN;
else
    data = X[t, elsize];
bit status = '1';
// Check whether the Exclusives monitors are set to include the
// physical memory locations corresponding to virtual address
// range [address, address+dbytes-1].
// If AArch64.ExclusiveMonitorsPass() returns FALSE and the memory address,
// if accessed, would generate a synchronous Data Abort exception, it is
// IMPLEMENTATION DEFINED whether the exception is generated.
// It is a limitation of this model that synchronous Data Aborts are never
// generated in this case, as Mem[] is not called.

// If FEAT_SPE is implemented, it is also IMPLEMENTATION DEFINED whether or not the
// physical address packet is output when permitted and when
// AArch64.ExclusiveMonitorPass() returns FALSE for a Store Exclusive instruction.
// This behavior is not reflected here due to the previously stated limitation.
if AArch64.ExclusiveMonitorsPass(address, dbytes, accdesc) then
    // This atomic write will be rejected if it does not refer
    // to the same physical locations after address translation.
    Mem[address, dbytes, accdesc] = data;
    status = ExclusiveMonitorsStatus();
X[s, 32] = ZeroExtend(status, 32);
```

### Variant: `No offset (STLXR_SR64_ldstexclr)` (64-bit)
- **Condition**: `size == 11`
- **Assembly**: `STLXR  <Ws>, <Xt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `size`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31  29  22 21 20  15 14   9   4  |
|-----------------------------|
| 1x  0010000 0   0   Rs  1   (1)(1)(1)(1)(1) Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the general-purpose register into which the status result of the store exclusive is written, encoded in the "Rs" field. The valu |
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be transferred, encoded in the "Rt" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `base-register`
- isa: `A64`
- source: `stlxr.xml`
</details>