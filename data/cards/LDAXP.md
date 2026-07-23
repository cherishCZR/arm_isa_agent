## LDAXP
_ARM A64 Instruction_

**Title**: LDAXP -- A64 | **Class**: `general` | **XML ID**: `LDAXP`

**Summary**: Load-acquire exclusive pair of registers

**Description**:
This instruction derives an address from
a base register value, loads two 32-bit words or two 64-bit
doublewords from memory, and writes them to two registers.
For information on single-copy atomicity and alignment requirements,
see Requirements for single-copy atomicity and
Alignment of data accesses.
The PE marks the physical address being accessed as an exclusive access.
This exclusive access mark is checked by Store Exclusive instructions. See
Synchronization and semaphores.
The instruction also has memory ordering
semantics, as described in
Load-Acquire, Store-Release.
For information about addressing modes, see
Load/Store addressing modes.

### Variant: `No offset (LDAXP_LP32_ldstexclp)` (32-bit)
- **Condition**: `sz == 0`
- **Assembly**: `LDAXP  <Wt1>, <Wt2>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `sz`=`0`
- **Bit Pattern**: `??????????????????????????????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 1   sz  0010000 1   1   (1)(1)(1)(1)(1) 1   Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstexclp.LDAXP_LP32_ldstexclp)

```
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);

constant integer elsize = 32 << UInt(sz);
constant integer datasize = elsize * 2;
constant boolean acqrel = TRUE;
constant boolean tagchecked = n != 31;

boolean rt_unknown = FALSE;
if t == t2 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_LDPOVERLAP);
    assert c IN {Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_UNKNOWN    rt_unknown = TRUE;    // result is UNKNOWN
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.ldstexclp.LDAXP_LP32_ldstexclp)

```
bits(64) address;
bits(datasize) data;

constant integer dbytes = datasize DIV 8;
constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescExLDST(MemOp_LOAD, acqrel, tagchecked,
                                                        privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

AArch64.SetExclusiveMonitors(address, dbytes);

if rt_unknown then
    // ConstrainedUNPREDICTABLE case
    X[t, datasize]  = bits(datasize) UNKNOWN;        // In this case t = t2
elsif elsize == 32 then
    // 32-bit load exclusive pair (atomic)
    data = Mem[address, dbytes, accdesc];
    if BigEndian(accdesc.acctype) then
        X[t, elsize]  = data<elsize +: elsize>;
        X[t2, elsize] = data<0 +: elsize>;
    else
        X[t, elsize]  = data<0 +: elsize>;
        X[t2, elsize] = data<elsize +: elsize>;
else // elsize == 64
    // 64-bit load exclusive pair (not atomic), but must be 128-bit aligned
    if !IsAligned(address, dbytes) then
        constant FaultRecord fault = AlignmentFault(accdesc, address);
        AArch64.Abort(fault);

    constant bits(64) address2 = AddressIncrement(address, 8, accdesc);
    X[t, 64]  = Mem[address , 8, accdesc];
    X[t2, 64] = Mem[address2, 8, accdesc];
```

### Variant: `No offset (LDAXP_LP64_ldstexclp)` (64-bit)
- **Condition**: `sz == 1`
- **Assembly**: `LDAXP  <Xt1>, <Xt2>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `sz`=`1`
- **Bit Pattern**: `??????????????????????????????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 1   sz  0010000 1   1   (1)(1)(1)(1)(1) 1   Rt2 Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Wt1>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Wt2>` | `register (32-bit)` | `Rt2` | Is the 32-bit name of the second general-purpose register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Xt1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xt2>` | `register (64-bit)` | `Rt2` | Is the 64-bit name of the second general-purpose register to be transferred, encoded in the "Rt2" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `base-register`
- isa: `A64`
- source: `ldaxp.xml`
</details>