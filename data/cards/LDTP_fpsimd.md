## LDTP
_ARM A64 Instruction_

**Title**: LDTP (SIMD&FP) -- A64 | **Class**: `fpsimd` | **XML ID**: `LDTP_fpsimd`

**Architecture**: `FEAT_FP && FEAT_LSUI` (FEAT_FP && FEAT_LSUI)

**Summary**: Load unprivileged pair of SIMD&FP registers

**Description**:
This instruction loads a pair of SIMD&FP registers
from memory.
The address that is used for the load is calculated from a base register value
and an optional immediate offset.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

Explicit Memory  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

### Variant: `Post-index`
- **Assembly**: `LDTP  <Qt1>, <Qt2>, [<Xn|SP>], #<imm>`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 11  10  1   1   0   01  1   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_post.LDTP_Q_ldstpair_post)

```
if !IsFeatureImplemented(FEAT_FP) || !IsFeatureImplemented(FEAT_LSUI) then
    EndOfDecode(Decode_UNDEF);

constant boolean wback = TRUE;
constant boolean postindex = TRUE;
```

#### Postdecode (A64.ldst.ldstpair_post.LDTP_Q_ldstpair_post)

```
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant boolean nontemporal = FALSE;
constant integer datasize = 128;
constant bits(64) offset = LSL(SignExtend(imm7, 64), 4);
constant boolean tagchecked = wback || n != 31;

boolean rt_unknown = FALSE;

if t == t2 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_LDPOVERLAP);
    assert c IN {Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_UNKNOWN    rt_unknown = TRUE;    // Result is UNKNOWN
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.ldstpair_post.LDTP_Q_ldstpair_post)

```
CheckFPEnabled64();
bits(64) address;
constant integer dbytes = datasize DIV 8;

constant boolean privileged = AArch64.IsUnprivAccessPriv();
constant boolean ispair = IsFeatureImplemented(FEAT_LS64WB) && datasize == 128;
constant AccessDescriptor accdesc = CreateAccDescASIMD(MemOp_LOAD, nontemporal,
                                                       tagchecked, privileged, ispair);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

if !postindex then
    address = AddressAdd(address, offset, accdesc);

bits(datasize) data1;
bits(datasize) data2;
if accdesc.ispair then
    constant bits(2*datasize) full_data = Mem[address, 2*dbytes, accdesc];
    if BigEndian(accdesc.acctype) then
        data2 = full_data<(datasize-1):0>;
        data1 = full_data<(2*datasize-1):datasize>;
    else
        data1 = full_data<(datasize-1):0>;
        data2 = full_data<(2*datasize-1):datasize>;
else
    constant bits(64) address2 = AddressIncrement(address, dbytes, accdesc);
    data1 = Mem[address , dbytes, accdesc];
    data2 = Mem[address2, dbytes, accdesc];

if rt_unknown then
    data1 = bits(datasize) UNKNOWN;
    data2 = bits(datasize) UNKNOWN;

V[t , datasize] = data1;
V[t2, datasize] = data2;

if wback then
    if postindex then
        address = AddressAdd(address, offset, accdesc);
    if n == 31 then
        SP[64] = address;
    else
        X[n, 64] = address;
```

### Variant: `Pre-index`
- **Assembly**: `LDTP  <Qt1>, <Qt2>, [<Xn|SP>, #<imm>]!`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 11  10  1   1   0   11  1   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_pre.LDTP_Q_ldstpair_pre)

```
if !IsFeatureImplemented(FEAT_FP) || !IsFeatureImplemented(FEAT_LSUI) then
    EndOfDecode(Decode_UNDEF);

constant boolean wback = TRUE;
constant boolean postindex = FALSE;
```

### Variant: `Signed offset`
- **Assembly**: `LDTP  <Qt1>, <Qt2>, [<Xn|SP>{, #<imm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 11  10  1   1   0   10  1   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstpair_off.LDTP_Q_ldstpair_off)

```
if !IsFeatureImplemented(FEAT_FP) || !IsFeatureImplemented(FEAT_LSUI) then
    EndOfDecode(Decode_UNDEF);

constant boolean wback = FALSE;
constant boolean postindex = FALSE;
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Qt1>` | `register (128-bit)` | `Rt` | Is the 128-bit name of the first SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Qt2>` | `register (128-bit)` | `Rt2` | Is the 128-bit name of the second SIMD&FP register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `imm7` | For the "Post-index" and "Pre-index" variants: is the signed immediate byte offset, a multiple of 16 in the range -1024 to 1008, encoded in the "imm7" |
| `<imm>` | `immediate` | `imm7` | For the "Signed offset" variant: is the optional signed immediate byte offset, a multiple of 16 in the range -1024 to 1008, defaulting to 0 and encode |

### Encoding Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP) && IsFeatureImplemented(FEAT_LSUI)` |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- atomic-ops: `LDTP-pair-quadwords`
- isa: `A64`
- offset-type: `off7s_s`
- reg-type: `pair-quadwords`
- source: `ldtp_fpsimd.xml`
</details>