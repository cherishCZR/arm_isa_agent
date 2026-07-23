## SETPTN
_ARM A64 Instruction_

**Title**: SETPTN, SETMTN, SETETN -- A64 | **Class**: `general` | **XML ID**: `SETPTN`

**Architecture**: `FEAT_MOPS` (ARMv8.8)

**Summary**: Memory set, unprivileged and non-temporal

**Description**:
These instructions set a required number of bytes in memory to the value in the least significant
byte of the source data register. The prologue, main, and epilogue instructions are expected to
be run in succession and to appear consecutively in memory: SETPTN, then SETMTN,
and then SETETN.

SETPTN performs some preconditioning of the arguments suitable for using the
SETMTN instruction, and sets an IMPLEMENTATION DEFINED portion of the requested number
of bytes. SETMTN sets a further IMPLEMENTATION DEFINED portion of the remaining bytes.
SETETN sets any final remaining bytes.

For more information on exceptions specific to memory set instructions,
see Memory Copy and Memory Set exceptions.

The architecture supports two algorithms for the memory set: option A and option B. Which
algorithm is used is IMPLEMENTATION DEFINED.

For SETPTN:

On completion of SETPTN, option A:

On completion of SETPTN, option B:

For SETMTN, option A, when PSTATE.C = 0:

For SETMTN, option B, when PSTATE.C = 1:

For SETETN, option A, when PSTATE.C = 0:

For SETETN, option B, when PSTATE.C = 1:

Explicit Memory Write  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory Write  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

### Variant: `Integer (SETPTN_SET_memcms)` (Prologue)
- **Condition**: `op2 == 0011`
- **Assembly**: `SETPTN  [<Xd>]!, <Xn>!, <Xs>`
- **Fixed bits**: `op2`=`00`
- **Bit Pattern**: `??????????????00????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  11   9   4  |
|-----------------------------------|
| sz  011 0   01  11  0   Rs  xx11 01  Rn  Rd  |
```

#### Decode (A64.ldst.memcms.SETPTN_SET_memcms)

```
if !IsFeatureImplemented(FEAT_MOPS) || sz != '00' then EndOfDecode(Decode_UNDEF);

SETParams memset;
memset.d = UInt(Rd);
memset.s = UInt(Rs);
memset.n = UInt(Rn);
constant bits(2) options = op2<1:0>;
constant boolean nontemporal = options<1> == '1';

case op2<3:2> of
    when '00' memset.stage = MOPSStage_Prologue;
    when '01' memset.stage = MOPSStage_Main;
    when '10' memset.stage = MOPSStage_Epilogue;
    otherwise EndOfDecode(Decode_UNDEF);
```

#### Execute (A64.ldst.memcms.SETPTN_SET_memcms)

```
CheckMOPSEnabled();

CheckSETConstrainedUnpredictable(memset.n, memset.d, memset.s);

constant bits(8) data = X[memset.s, 8];
MOPSBlockSize B;

memset.is_setg = FALSE;
memset.nzcv = PSTATE.<N,Z,C,V>;
memset.toaddress = X[memset.d, 64];
if memset.stage == MOPSStage_Prologue then
    memset.setsize = UInt(X[memset.n, 64]);
else
    memset.setsize = SInt(X[memset.n, 64]);
memset.implements_option_a = SETOptionA();

constant boolean privileged = (if options<0> == '1' then AArch64.IsUnprivAccessPriv()
                               else PSTATE.EL != EL0);

constant AccessDescriptor accdesc = CreateAccDescMOPS(MemOp_STORE, privileged, nontemporal);

if memset.stage == MOPSStage_Prologue then
    if memset.setsize > ArchMaxMOPSBlockSize then
        memset.setsize = ArchMaxMOPSBlockSize;

    if memset.implements_option_a then
        memset.nzcv = '0000';
        memset.toaddress = memset.toaddress + memset.setsize;
        memset.setsize   = 0 - memset.setsize;
    else
        memset.nzcv = '0010';

memset.stagesetsize = MemSetStageSize(memset);

if memset.stage != MOPSStage_Prologue then
    CheckMemSetParams(memset, options);

AddressDescriptor memaddrdesc;
PhysMemRetStatus  memstatus;
integer memory_set;
boolean fault = FALSE;

if memset.implements_option_a then
    while memset.stagesetsize < 0 && !fault do
        // IMP DEF selection of the block size that is worked on. While many
        // implementations might make this constant, that is not assumed.
        B = SETSizeChoice(memset, 1);
        assert B <= -1 * memset.stagesetsize;

        (memory_set, memaddrdesc, memstatus) = MemSetBytes(memset.toaddress + memset.setsize,
                                                           data, B, accdesc);

        if memory_set != B then
            fault = TRUE;
        else
            memset.setsize      = memset.setsize      + B;
            memset.stagesetsize = memset.stagesetsize + B;

else
    while memset.stagesetsize > 0 && !fault do
        // IMP DEF selection of the block size that is worked on. While many
        // implementations might make this constant, that is not assumed.
        B = SETSizeChoice(memset, 1);
        assert B <= memset.stagesetsize;

        (memory_set, memaddrdesc, memstatus) = MemSetBytes(memset.toaddress, data, B, accdesc);

        if memory_set != B then
            fault = TRUE;
        else
            memset.toaddress    = memset.toaddress    + B;
            memset.setsize      = memset.setsize      - B;
            memset.stagesetsize = memset.stagesetsize - B;

UpdateSetRegisters(memset, fault, memory_set);

if fault then
    if IsFault(memaddrdesc) then
        AArch64.Abort(memaddrdesc.fault);
    else
        constant boolean iswrite = TRUE;
        HandleExternalAbort(memstatus, iswrite, memaddrdesc, B, accdesc);

if memset.stage == MOPSStage_Prologue then
    PSTATE.<N,Z,C,V> = memset.nzcv;
```

#### Constraints
_1× ↩ DECODE_FALLBACK / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_MOPS) && sz == '00'` |
| ↩ DECODE_FALLBACK | `matching encodings` |

### Variant: `Integer (SETMTN_SET_memcms)` (Main)
- **Condition**: `op2 == 0111`
- **Assembly**: `SETMTN  [<Xd>]!, <Xn>!, <Xs>`
- **Fixed bits**: `op2`=`01`
- **Bit Pattern**: `??????????????10????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  11   9   4  |
|-----------------------------------|
| sz  011 0   01  11  0   Rs  xx11 01  Rn  Rd  |
```

### Variant: `Integer (SETETN_SET_memcms)` (Epilogue)
- **Condition**: `op2 == 1011`
- **Assembly**: `SETETN  [<Xd>]!, <Xn>!, <Xs>`
- **Fixed bits**: `op2`=`10`
- **Bit Pattern**: `??????????????01????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  11   9   4  |
|-----------------------------------|
| sz  011 0   01  11  0   Rs  xx11 01  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | For the "Prologue" variant: is the 64-bit name of the general-purpose register that holds the destination address and is updated by the instruction, e |
| `<Xd>` | `register (64-bit)` | `Rd` | For the "Epilogue" and "Main" variants: is the 64-bit name of the general-purpose register that holds an encoding of the destination address and for o |
| `<Xn>` | `register (64-bit)` | `Rn` | For the "Prologue" variant: is the 64-bit name of the general-purpose register that holds the number of bytes to be set and is updated by the instruct |
| `<Xn>` | `register (64-bit)` | `Rn` | For the "Main" variant: is the 64-bit name of the general-purpose register that holds an encoding of the number of bytes to be set and is updated by t |
| `<Xn>` | `register (64-bit)` | `Rn` | For the "Epilogue" variant: is the 64-bit name of the general-purpose register that holds the number of bytes to be set and is set to zero on completi |
| `<Xs>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the general-purpose register that holds the source data, encoded in the "Rs" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `setptn.xml`
</details>