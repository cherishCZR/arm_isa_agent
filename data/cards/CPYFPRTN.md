## CPYFPRTN
_ARM A64 Instruction_

**Title**: CPYFPRTN, CPYFMRTN, CPYFERTN -- A64 | **Class**: `general` | **XML ID**: `CPYFPRTN`

**Architecture**: `FEAT_MOPS` (ARMv8.8)

**Summary**: Memory copy forward-only, reads unprivileged, reads and writes non-temporal

**Description**:
These instructions copy a requested number of bytes in memory from a source address to a
destination address in a forward direction. The prologue, main, and epilogue instructions
are expected to be run in succession and to appear consecutively in memory:
CPYFPRTN, then CPYFMRTN, and then CPYFERTN.

CPYFPRTN performs some preconditioning of the arguments suitable for using the
CPYFMRTN instruction, and copies an IMPLEMENTATION DEFINED portion of the requested
number of bytes. CPYFMRTN copies a further IMPLEMENTATION DEFINED portion of the
remaining bytes. CPYFERTN copies any final remaining bytes.

For more information on exceptions specific to memory copy instructions,
see Memory Copy and Memory Set exceptions.

The memory copy performed by these instructions is in the forward direction only, so the
instructions are suitable for a memory copy only where there is no overlap between the
source and destination locations, or where the source address is greater than the
destination address.

The architecture supports two algorithms for the memory copy: option A and option B.
Which algorithm is used is IMPLEMENTATION DEFINED.

For CPYFPRTN:

On completion of CPYFPRTN, option A:

On completion of CPYFPRTN, option B:

For CPYFMRTN, option A, when PSTATE.C = 0:

For CPYFMRTN, option B, when PSTATE.C = 1:

For CPYFERTN, option A, when PSTATE.C = 0:

For CPYFERTN, option B, when PSTATE.C = 1:

Explicit Memory Read  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory Read  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

### Variant: `Integer (CPYFPRTN_CPY_memcms)` (Prologue)
- **Condition**: `op1 == 00`
- **Assembly**: `CPYFPRTN  [<Xd>]!, [<Xs>]!, <Xn>!`
- **Fixed bits**: `op1`=`00`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  11   9   4  |
|-----------------------------------|
| sz  011 0   01  op1 0   Rs  1110 01  Rn  Rd  |
```

#### Decode (A64.ldst.memcms.CPYFPRTN_CPY_memcms)

```
if !IsFeatureImplemented(FEAT_MOPS) || sz != '00' then EndOfDecode(Decode_UNDEF);

CPYParams memcpy;
memcpy.d = UInt(Rd);
memcpy.s = UInt(Rs);
memcpy.n = UInt(Rn);
constant bits(4) options = op2;
constant boolean rnontemporal = options<3> == '1';
constant boolean wnontemporal = options<2> == '1';
case op1 of
    when '00' memcpy.stage = MOPSStage_Prologue;
    when '01' memcpy.stage = MOPSStage_Main;
    when '10' memcpy.stage = MOPSStage_Epilogue;
    otherwise SEE "Memory Copy and Memory Set";
```

#### Execute (A64.ldst.memcms.CPYFPRTN_CPY_memcms)

```
CheckMOPSEnabled();

CheckCPYConstrainedUnpredictable(memcpy.n, memcpy.d, memcpy.s);

memcpy.nzcv        = PSTATE.<N,Z,C,V>;
memcpy.toaddress   = X[memcpy.d, 64];
memcpy.fromaddress = X[memcpy.s, 64];
memcpy.cpysize     = SInt(X[memcpy.n, 64]);
memcpy.implements_option_a = CPYFOptionA();

constant boolean rprivileged = (if options<1> == '1' then AArch64.IsUnprivAccessPriv()
                                else PSTATE.EL != EL0);
constant boolean wprivileged = (if options<0> == '1' then AArch64.IsUnprivAccessPriv()
                                else PSTATE.EL != EL0);

constant AccessDescriptor raccdesc = CreateAccDescMOPS(MemOp_LOAD,  rprivileged, rnontemporal);
constant AccessDescriptor waccdesc = CreateAccDescMOPS(MemOp_STORE, wprivileged, wnontemporal);

if memcpy.stage == MOPSStage_Prologue then
    if memcpy.cpysize<63> == '1' then memcpy.cpysize = ArchMaxMOPSBlockSize;

    if memcpy.implements_option_a then
        memcpy.nzcv = '0000';
        // Copy in the forward direction offsets the arguments.
        memcpy.toaddress   = memcpy.toaddress   + memcpy.cpysize;
        memcpy.fromaddress = memcpy.fromaddress + memcpy.cpysize;
        memcpy.cpysize     = 0 - memcpy.cpysize;
    else
        memcpy.nzcv = '0010';

memcpy.stagecpysize = MemCpyStageSize(memcpy);

if memcpy.stage != MOPSStage_Prologue then
    CheckMemCpyParams(memcpy, options);

integer copied;
boolean iswrite;
AddressDescriptor memaddrdesc;
PhysMemRetStatus  memstatus;
memcpy.forward = TRUE;
boolean fault  = FALSE;
MOPSBlockSize B;

if memcpy.implements_option_a then
    while memcpy.stagecpysize != 0 && !fault do
        // IMP DEF selection of the block size that is worked on. While many
        // implementations might make this constant, that is not assumed.
        B = CPYSizeChoice(memcpy);
        assert B <= -1 * memcpy.stagecpysize;

        (copied, iswrite, memaddrdesc, memstatus) = MemCpyBytes(memcpy.toaddress   + memcpy.cpysize,
                                                                memcpy.fromaddress + memcpy.cpysize,
                                                                memcpy.forward, B,
                                                                raccdesc, waccdesc);
        if copied != B then
            fault = TRUE;
        else
            memcpy.cpysize      = memcpy.cpysize + B;
            memcpy.stagecpysize = memcpy.stagecpysize + B;
else
    while memcpy.stagecpysize > 0 && !fault do
        // IMP DEF selection of the block size that is worked on. While many
        // implementations might make this constant, that is not assumed.
        B = CPYSizeChoice(memcpy);
        assert B <= memcpy.stagecpysize;

        (copied, iswrite, memaddrdesc, memstatus) = MemCpyBytes(memcpy.toaddress,
                                                                memcpy.fromaddress,
                                                                memcpy.forward, B,
                                                                raccde
... (truncated)
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_MOPS) && sz == '00'` |

### Variant: `Integer (CPYFMRTN_CPY_memcms)` (Main)
- **Condition**: `op1 == 01`
- **Assembly**: `CPYFMRTN  [<Xd>]!, [<Xs>]!, <Xn>!`
- **Fixed bits**: `op1`=`01`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  11   9   4  |
|-----------------------------------|
| sz  011 0   01  op1 0   Rs  1110 01  Rn  Rd  |
```

### Variant: `Integer (CPYFERTN_CPY_memcms)` (Epilogue)
- **Condition**: `op1 == 10`
- **Assembly**: `CPYFERTN  [<Xd>]!, [<Xs>]!, <Xn>!`
- **Fixed bits**: `op1`=`10`
- **Bit Pattern**: `??????????????????????01????????`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  23  21 20  15  11   9   4  |
|-----------------------------------|
| sz  011 0   01  op1 0   Rs  1110 01  Rn  Rd  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xd>` | `register (64-bit)` | `Rd` | For the "Prologue" variant: is the 64-bit name of the general-purpose register that holds the destination address and is updated by the instruction, e |
| `<Xd>` | `register (64-bit)` | `Rd` | For the "Epilogue" and "Main" variants: is the 64-bit name of the general-purpose register that holds an encoding of the destination address, encoded  |
| `<Xs>` | `register (64-bit)` | `Rs` | For the "Prologue" variant: is the 64-bit name of the general-purpose register that holds the source address and is updated by the instruction, encode |
| `<Xs>` | `register (64-bit)` | `Rs` | For the "Epilogue" and "Main" variants: is the 64-bit name of the general-purpose register that holds an encoding of the source address, encoded in th |
| `<Xn>` | `register (64-bit)` | `Rn` | For the "Prologue" variant: is the 64-bit name of the general-purpose register that holds the number of bytes to be transferred and is updated by the  |
| `<Xn>` | `register (64-bit)` | `Rn` | For the "Main" variant: is the 64-bit name of the general-purpose register that holds an encoding of the number of bytes to be transferred, encoded in |
| `<Xn>` | `register (64-bit)` | `Rn` | For the "Epilogue" variant: is the 64-bit name of the general-purpose register that holds an encoding of the number of bytes to be transferred and is  |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `cpyfprtn.xml`
</details>