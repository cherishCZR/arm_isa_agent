## LDTNP
_ARM A64 Instruction_

**Title**: LDTNP (SIMD&FP) -- A64 | **Class**: `fpsimd` | **XML ID**: `LDTNP_fpsimd`

**Architecture**: `FEAT_FP && FEAT_LSUI` (FEAT_FP && FEAT_LSUI)

**Summary**: Load unprivileged pair of SIMD&FP registers, with non-temporal hint

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

Explicit Memory  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

### Variant: `Signed offset`
- **Assembly**: `LDTNP  <Qt1>, <Qt2>, [<Xn|SP>{, #<imm>}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24  22 21  14   9   4  |
|-----------------------------------|
| 11  10  1   1   0   00  1   imm7 Rt2 Rn  Rt  |
```

#### Decode (A64.ldst.ldstnapair_offs.LDTNP_Q_ldstnapair_offs)

```
if !IsFeatureImplemented(FEAT_FP) || !IsFeatureImplemented(FEAT_LSUI) then
    EndOfDecode(Decode_UNDEF);
constant integer t = UInt(Rt);
constant integer t2 = UInt(Rt2);
constant integer n = UInt(Rn);
constant boolean nontemporal = TRUE;
constant integer datasize = 128;
constant bits(64) offset = LSL(SignExtend(imm7, 64), 4);
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

#### Execute (A64.ldst.ldstnapair_offs.LDTNP_Q_ldstnapair_offs)

```
CheckFPEnabled64();
bits(64) address;
bits(64) address2;
constant integer dbytes = datasize DIV 8;

constant boolean privileged = AArch64.IsUnprivAccessPriv();
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
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_FP) && IsFeatureImplemented(FEAT_LSUI)` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Qt1>` | `register (128-bit)` | `Rt` | Is the 128-bit name of the first SIMD&FP register to be transferred, encoded in the "Rt" field. |
| `<Qt2>` | `register (128-bit)` | `Rt2` | Is the 128-bit name of the second SIMD&FP register to be transferred, encoded in the "Rt2" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<imm>` | `immediate` | `imm7` | Is the optional signed immediate byte offset, a multiple of 16 in the range -1024 to 1008, defaulting to 0 and encoded in the "imm7" field as <imm>/16 |

### Operational Notes

If PSTATE.DIT is 1, the timing of this instruction is insensitive to the value of the data being loaded or stored.

---
<details><summary>Metadata</summary>

- address-form: `signed-scaled-offset`
- address-form-reg-type: `signed-scaled-offset-pair-quadwords`
- atomic-ops: `LDNP-pair-quadwords`
- isa: `A64`
- offset-type: `off7s_s`
- reg-type: `pair-quadwords`
- source: `ldtnp_fpsimd.xml`
</details>