## SETGPTN
_ARM A64 Instruction_

**Title**: SETGPTN, SETGMTN, SETGETN -- A64 | **Class**: `general` | **XML ID**: `SETGPTN`

**Architecture**: `FEAT_MOPS && FEAT_MTE` (FEAT_MOPS && FEAT_MTE)

**Summary**: Memory set with tag setting, unprivileged and non-temporal

**Description**:
These instructions set a requested number of bytes in memory to the value in the least
significant byte of the source data register and store an Allocation Tag to memory for
each Tag Granule written. The Allocation Tag is calculated from the Logical Address Tag
in the register that holds the first address to be set. The prologue, main, and epilogue
instructions are expected to be run in succession and to appear consecutively in memory:
SETGPTN, then SETGMTN, and then SETGETN.

SETGPTN performs some preconditioning of the arguments suitable for using the
SETGMTN instruction, and sets an IMPLEMENTATION DEFINED portion of the requested number
of bytes. SETGMTN sets a further IMPLEMENTATION DEFINED portion of the remaining bytes.
SETGETN sets any final remaining bytes.

For more information on exceptions specific to memory set instructions,
see Memory Copy and Memory Set exceptions.

The architecture supports two algorithms for the memory set: option A and option B. Which
algorithm is used is IMPLEMENTATION DEFINED.

For SETGPTN:

On completion of SETGPTN, option A:

On completion of SETGPTN, option B:

For SETGMTN, option A, when PSTATE.C = 0:

For SETGMTN, option B, when PSTATE.C = 1:

For SETGETN, option A, when PSTATE.C = 0:

For SETGETN, option B, when PSTATE.C = 1:

Explicit Memory Write  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory Write  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

### Variant: `Integer (SETGPTN_SET_memcms)` (Prologue)
- **Condition**: `op2 == 0011`
- **Assembly**: `SETGPTN  [<Xd>]!, <Xn>!, <Xs>`
- **Fixed bits**: `op2`=`00`
- **Bit Pattern**: `??????????????00????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  11   9   4  |
|-----------------------------------|
| sz  011 1   01  11  0   Rs  xx11 01  Rn  Rd  |
```

#### Decode (A64.ldst.memcms.SETGPTN_SET_memcms)

```
if !IsFeatureImplemented(FEAT_MOPS) || !IsFeatureImplemented(FEAT_MTE) || sz != '00' then
    EndOfDecode(Decode_UNDEF);

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

#### Execute (A64.ldst.memcms.SETGPTN_SET_memcms)

```
CheckMOPSEnabled();

CheckSETConstrainedUnpredictable(memset.n, memset.d, memset.s);

constant bits(8) data = X[memset.s, 8];
MOPSBlockSize B;

memset.is_setg = TRUE;
memset.nzcv = PSTATE.<N,Z,C,V>;
memset.toaddress = X[memset.d, 64];
if memset.stage == MOPSStage_Prologue then
    memset.setsize = UInt(X[memset.n, 64]);
else
    memset.setsize = SInt(X[memset.n, 64]);
memset.implements_option_a = SETGOptionA();

constant boolean privileged = (if options<0> == '1' then AArch64.IsUnprivAccessPriv()
                               else PSTATE.EL != EL0);

constant AccessDescriptor accdesc = CreateAccDescSTGMOPS(privileged, nontemporal);

if memset.stage == MOPSStage_Prologue then
    if memset.setsize > ArchMaxMOPSSETGSize then
        memset.setsize = ArchMaxMOPSSETGSize;

    if ((memset.setsize != 0 && !IsAligned(memset.toaddress, TAG_GRANULE)) ||
            !IsAligned(memset.setsize<63:0>, TAG_GRANULE)) then
        constant FaultRecord fault = AlignmentFault(accdesc, memset.toaddress);
        AArch64.Abort(fault);

    if memset.implements_option_a then
        memset.nzcv = '0000';
        memset.toaddress = memset.toaddress + memset.setsize;
        memset.setsize   = 0 - memset.setsize;
    else
        memset.nzcv = '0010';

memset.stagesetsize = MemSetStageSize(memset);

if memset.stage != MOPSStage_Prologue then
    CheckMemSetParams(memset, options);

    bits(64) fault_address;
    if memset.implements_option_a then
        fault_address = memset.toaddress + memset.setsize;
    else
        fault_address = memset.toaddress;

    if (memset.setsize != 0 && (memset.stagesetsize != 0 || MemStageSetZeroSizeCheck()) &&
          !IsAligned(memset.toaddress, TAG_GRANULE)) then
        constant FaultRecord fault = AlignmentFault(accdesc, fault_address);
        AArch64.Abort(fault);
    if ((memset.stagesetsize != 0 || MemStageSetZeroSizeCheck()) &&
           !IsAligned(memset.setsize<63:0>, TAG_GRANULE)) then
        constant FaultRecord fault = AlignmentFault(accdesc, fault_address);
        AArch64.Abort(fault);

integer tagstep;
bits(4) tag;
bits(64) tagaddr;
AddressDescriptor memaddrdesc;
PhysMemRetStatus  memstatus;
integer memory_set;
boolean fault = FALSE;

if memset.implements_option_a then
    while memset.stagesetsize < 0 && !fault do
        // IMP DEF selection of the block size that is worked on. While many
        // implementations might make this constant, that is not assumed.
        B = SETSizeChoice(memset, TAG_GRANULE);
        assert B <= -1 * memset.stagesetsize && B<3:0> == '0000';

        (memory_set, memaddrdesc, memstatus) = MemSetBytes(memset.toaddress + memset.setsize,
                                                           data, B, accdesc);

        if memory_set != B then
            fault = TRUE;
        else
            tagstep = B DIV TAG_GRANULE;
            tag = AArch64.AllocationTagFromAddress(memset.toaddress + memset.setsize);

            while tagstep > 0 do
                tagaddr = memset.toad
... (truncated)
```

#### Constraints
_1× ↩ DECODE_FALLBACK / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_MOPS) && IsFeatureImplemented(FEAT_MTE) && sz == '00'` |
| ↩ DECODE_FALLBACK | `matching encodings` |

### Variant: `Integer (SETGMTN_SET_memcms)` (Main)
- **Condition**: `op2 == 0111`
- **Assembly**: `SETGMTN  [<Xd>]!, <Xn>!, <Xs>`
- **Fixed bits**: `op2`=`01`
- **Bit Pattern**: `??????????????10????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  11   9   4  |
|-----------------------------------|
| sz  011 1   01  11  0   Rs  xx11 01  Rn  Rd  |
```

### Variant: `Integer (SETGETN_SET_memcms)` (Epilogue)
- **Condition**: `op2 == 1011`
- **Assembly**: `SETGETN  [<Xd>]!, <Xn>!, <Xs>`
- **Fixed bits**: `op2`=`10`
- **Bit Pattern**: `??????????????01????????????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  11   9   4  |
|-----------------------------------|
| sz  011 1   01  11  0   Rs  xx11 01  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | For the "Prologue" variant: is the 64-bit name of the general-purpose register that holds an encoding of the destination address (an integer multiple  |
| `<Xd>` | `register (64-bit)` | `Rd` | For the "Epilogue" and "Main" variants: is the 64-bit name of the general-purpose register that holds an encoding of the destination address (an integ |
| `<Xn>` | `register (64-bit)` | `Rn` | For the "Prologue" variant: is the 64-bit name of the general-purpose register that holds the number of bytes to be set (an integer multiple of 16) an |
| `<Xn>` | `register (64-bit)` | `Rn` | For the "Main" variant: is the 64-bit name of the general-purpose register that holds an encoding of the number of bytes to be set (an integer multipl |
| `<Xn>` | `register (64-bit)` | `Rn` | For the "Epilogue" variant: is the 64-bit name of the general-purpose register that holds an encoding of the number of bytes to be set (an integer mul |
| `<Xs>` | `register (64-bit)` | `Rs` | For the "Main" and "Prologue" variants: is the 64-bit name of the general-purpose register that holds the source data in bits<7:0>, encoded in the "Rs |
| `<Xs>` | `register (64-bit)` | `Rs` | For the "Epilogue" variant: is the 64-bit name of the general-purpose register that holds the source data, encoded in the "Rs" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `setgptn.xml`
</details>