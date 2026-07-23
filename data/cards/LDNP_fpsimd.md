## LDNP
_ARM A64 Instruction_

**Title**: LDNP (SIMD&FP) -- A64 | **Class**: `fpsimd` | **XML ID**: `LDNP_fpsimd`

**Architecture**: `FEAT_FP` (ARMv8.0)

**Summary**: Load pair of SIMD&FP registers, with non-temporal hint

**Description**:
This instruction loads a pair of SIMD&FP registers
from memory, issuing a hint to the memory
system that the access is non-temporal.
The address that is used for the load is calculated from a base register value
and an optional immediate offset.

For information about non-temporal pair instructions, see
Load/Store SIMD and Floating-point non-temporal pair.

Depending on the settings in the CPACR_EL1,
  CPTR_EL2, and CPTR_EL3 registers,
  and the current Security state and Exception level,
  an attempt to execute the instruction might be trapped.

### Variant: `Signed offset (LDNP_S_ldstnapair_offs)` (32-bit)
- **Condition**: `opc == 00`
- **Assembly**: `LDNP  <St1>, <St2>, [<Xn|SP>{, #<imm>}]`
- **Fixed bits**: `opc`=`00`
- **Bit Pattern**: `??????????????????????????????00`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| opc 101 1   000 1   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstnapair_offs.LDNP_S_ldstnapair_offs)

```
// Empty.
```

#### Postdecode (A64.ldst.ldstnapair_offs.LDNP_S_ldstnapair_offs)

```
if !IsFeatureImplemented(FEAT_FP) then EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant boolean nontemporal = TRUE;
constant integer scale = 2 + (UInt(opc));
constant integer datasize = 8 << scale;
constant bits(64) offset = LSL(SignExtend(imm7, 64), scale);
constant boolean tagchecked = n != 31;
boolean rt_unknown = FALSE;

if t == t2 then
    constant Constraint c = ConstrainUnpredictable(Unpredictable_LDPOVERLAP);
    assert c IN {Constraint_UNKNOWN, Constraint_UNDEF, Constraint_NOP};
    case c of
        when Constraint_UNKNOWN    rt_unknown = TRUE;    // Result is UNKNOWN
        when Constraint_UNDEF      EndOfDecode(Decode_UNDEF);
        when Constraint_NOP        EndOfDecode(Decode_NOP);
```

#### Execute (A64.ldst.ldstnapair_offs.LDNP_S_ldstnapair_offs)

```
CheckFPEnabled64();
bits(64) address;
bits(64) address2;
constant integer dbytes = datasize DIV 8;

constant boolean privileged = PSTATE.EL != EL0;
constant AccessDescriptor accdesc = CreateAccDescASIMD(MemOp_LOAD, nontemporal,
                                                       tagchecked, privileged);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

address = AddressAdd(address, offset, accdesc);

address2 = AddressIncrement(address, dbytes, accdesc);
bits(datasize) data1 = Mem[address , dbytes, accdesc];
bits(datasize) data2 = Mem[address2, dbytes, accdesc];

if rt_unknown then
    data1 = bits(datasize) UNKNOWN;
    data2 = bits(datasize) UNKNOWN;

V[t, datasize]  = data1;
V[t2, datasize] = data2;
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP)` |

### Variant: `Signed offset (LDNP_D_ldstnapair_offs)` (64-bit)
- **Condition**: `opc == 01`
- **Assembly**: `LDNP  <Dt1>, <Dt2>, [<Xn|SP>{, #<imm>}]`
- **Fixed bits**: `opc`=`01`
- **Bit Pattern**: `??????????????????????????????10`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| opc 101 1   000 1   imm7 Rt2 Rn  Rt  |
```

### Variant: `Signed offset (LDNP_Q_ldstnapair_offs)` (128-bit)
- **Condition**: `opc == 10`
- **Assembly**: `LDNP  <Qt1>, <Qt2>, [<Xn|SP>{, #<imm>}]`
- **Fixed bits**: `opc`=`10`
- **Bit Pattern**: `??????????????????????????????01`
**Encoding Diagram (32-bit)**:

```text
| 31  29  26 25  22 21  14   9   4  |
|-----------------------------|
| opc 101 1   000 1   imm7 Rt2 Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<St1>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the first SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<St2>` | `register (32-bit)` | `Rt2` | Is the 32-bit name of the second SIMD&FP register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `imm7` | For the "32-bit" variant: is the optional signed immediate byte offset, a multiple of 4 in the range -256 to 252, defaulting to 0 and encoded in the " |
| `<imm>` | `immediate` | `imm7` | For the "64-bit" variant: is the optional signed immediate byte offset, a multiple of 8 in the range -512 to 504, defaulting to 0 and encoded in the " |
| `<imm>` | `immediate` | `imm7` | For the "128-bit" variant: is the optional signed immediate byte offset, a multiple of 16 in the range -1024 to 1008, defaulting to 0 and encoded in t |
| `<Dt1>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Dt2>` | `register (64-bit)` | `Rt2` | Is the 64-bit name of the second SIMD&FP register to be transferred, encoded in the "Rt2" field. |
| `<Qt1>` | `register (128-bit)` | `Rt` | Is the 128-bit name of the first SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Qt2>` | `register (128-bit)` | `Rt2` | Is the 128-bit name of the second SIMD&FP register to be transferred, encoded in the "Rt2" field. |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `signed-scaled-offset`
- isa: `A64`
- offset-type: `off7s_s`
- source: `ldnp_fpsimd.xml`
</details>