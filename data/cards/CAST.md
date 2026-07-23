## CAST
_ARM A64 Instruction_

**Title**: CAST, CASAT, CASALT, CASLT -- A64 | **Class**: `general` | **XML ID**: `CAST`

**Architecture**: `FEAT_LSUI` (ARMv9.6)

**Summary**: Compare and swap unprivileged

**Description**:
This instruction
reads a 64-bit doubleword from memory, and compares it against the value held in a
first register. If the comparison is equal, the value in a second register
is written to memory. If the comparison is not equal, the architecture permits writing
the value read from the location to memory.
If the write is performed, the read and write occur atomically such
that no other modification of the memory location can take place
between the read and write.

The architecture permits that the data read clears any exclusive
monitors associated with that location, even if the compare
subsequently fails.

If the instruction generates a synchronous Data Abort, the register
which is compared and loaded, that is <Xs>,
is restored to the value held in the register
before the instruction was executed.

Explicit Memory  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

For a CAST or CASAT instruction, when <Ws>
or <Xs> specifies the same register as <Wt> or <Xt>,
this signals to the memory system that an additional subsequent CAST,
CASAT, CASALT, or CASLT
access to the specified location is likely to occur in the near future. The memory system can respond by
taking actions that are expected to enable the subsequent CAST,
CASAT, CASALT, or CASLT access to succeed when it does occur.

A code sequence starting with a CAST or CASAT instruction for which
<Ws> or <Xs> specifies the same register as <Wt>
or <Xt>, and ending with a subsequent CAST, CASAT,
CASALT, or CASLT to the same location, exhibits the following
properties for best performance when the location may be accessed concurrently, on one or more other PEs:

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `No offset (CAST_C64_comswap_unpriv)` (CAST)
- **Condition**: `L == 0 && o0 == 0`
- **Assembly**: `CAST  <Xs>, <Xt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`0`, `o0`=`0`
- **Bit Pattern**: `???????????????0??????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 1   1   0010011 L   0   Rs  o0  11111 Rn  Rt  |
```

#### Decode (A64.ldst.comswap_unpriv.CAST_C64_comswap_unpriv)

```
if !IsFeatureImplemented(FEAT_LSUI) then EndOfDecode(Decode_UNDEF);
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant boolean acquire = L == '1';
constant boolean release = o0 == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.comswap_unpriv.CAST_C64_comswap_unpriv)

```
bits(64) address;
bits(64) comparevalue;
bits(64) newvalue;

constant boolean privileged = AArch64.IsUnprivAccessPriv();
constant AccessDescriptor accdesc = CreateAccDescAtomicOp(MemAtomicOp_CAS, acquire, release,
                                                          tagchecked, privileged);
comparevalue = X[s, 64];
newvalue = X[t, 64];

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

X[s, 64] = MemAtomic(address, comparevalue, newvalue, accdesc);
```

#### Constraints
_1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSUI)` |

### Variant: `No offset (CASAT_C64_comswap_unpriv)` (CASAT)
- **Condition**: `L == 1 && o0 == 0`
- **Assembly**: `CASAT  <Xs>, <Xt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`1`, `o0`=`0`
- **Bit Pattern**: `???????????????0??????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 1   1   0010011 L   0   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASALT_C64_comswap_unpriv)` (CASALT)
- **Condition**: `L == 1 && o0 == 1`
- **Assembly**: `CASALT  <Xs>, <Xt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`1`, `o0`=`1`
- **Bit Pattern**: `???????????????1??????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 1   1   0010011 L   0   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASLT_C64_comswap_unpriv)` (CASLT)
- **Condition**: `L == 0 && o0 == 1`
- **Assembly**: `CASLT  <Xs>, <Xt>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`0`, `o0`=`1`
- **Bit Pattern**: `???????????????1??????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 1   1   0010011 L   0   Rs  o0  11111 Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xs>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the general-purpose register to be compared and loaded, encoded in the "Rs" field. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the general-purpose register to be conditionally stored, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- address-form: `base-register`
- address-form-reg-type: `base-register-64-reg`
- isa: `A64`
- reg-type: `64-reg`
- source: `cast.xml`
</details>