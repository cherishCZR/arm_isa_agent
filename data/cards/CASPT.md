## CASPT
_ARM A64 Instruction_

**Title**: CASPT, CASPAT, CASPALT, CASPLT -- A64 | **Class**: `general` | **XML ID**: `CASPT`

**Architecture**: `FEAT_LSUI` (ARMv9.6)

**Summary**: Compare and swap pair unprivileged

**Description**:
This instruction
reads a pair of 64-bit doublewords from memory, and compares them
against the values held in the first pair of registers. If the
comparison is equal, the values in the second pair of registers are
written to memory. If the comparison is not equal, the architecture permits writing
the value read from the location to memory.
If the writes are performed, the reads and writes occur atomically such
that no other modification of the memory location can take place
between the reads and writes.

The architecture permits that the data read clears any exclusive
monitors associated with that location, even if the compare
subsequently fails.

If the instruction generates a synchronous Data Abort, the registers
which are compared and loaded, that is <Xs>
and <X(s+1)>, are
restored to the values held in the registers before the instruction
was executed.

Explicit Memory  effects produced by the instruction behave as if the instruction was
  executed at EL0 if the Effective value of
  PSTATE.UAO is 0 and either:

Otherwise, the Explicit Memory  effects operate with the restrictions determined by
  the Exception level at which the instruction is executed.

For a CASPT or CASPAT instruction, when <Ws>
or <Xs> specifies the same register as <Wt> or <Xt>,
this signals to the memory system that an additional subsequent CASPT,
CASPAT, CASPALT, or CASPLT
access to the specified location is likely to occur in the near future. The memory system can respond by
taking actions that are expected to enable the subsequent CASPT,
CASPAT, CASPALT, or CASPLT access to succeed when it does occur.

A code sequence starting with a CASPT or CASPAT instruction for which
<Ws> or <Xs> specifies the same register as <Wt>
or <Xt>, and ending with a subsequent CASPT, CASPAT,
CASPALT, or CASPLT to the same location, exhibits the following
properties for best performance when the location may be accessed concurrently, on one or more other PEs:

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `No offset (CASPT_CP64_comswappr_unpriv)` (CASPT)
- **Condition**: `L == 0 && o0 == 0`
- **Assembly**: `CASPT  <Xs>, <X(s+1)>, <Xt>, <X(t+1)>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`0`, `o0`=`0`
- **Bit Pattern**: `???????????????0??????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 0   1   0010011 L   0   Rs  o0  11111 Rn  Rt  |
```

#### Decode (A64.ldst.comswappr_unpriv.CASPT_CP64_comswappr_unpriv)

```
if !IsFeatureImplemented(FEAT_LSUI) then EndOfDecode(Decode_UNDEF);
if Rs<0> == '1' || Rt<0> == '1' then EndOfDecode(Decode_UNDEF);
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer datasize = 64;
constant boolean acquire = L == '1';
constant boolean release = o0 == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.comswappr_unpriv.CASPT_CP64_comswappr_unpriv)

```
bits(64) address;
bits(2*datasize) comparevalue;
bits(2*datasize) newvalue;
bits(2*datasize) data;

constant bits(datasize) s1 = X[s, datasize];
constant bits(datasize) s2 = X[s+1, datasize];
constant bits(datasize) t1 = X[t, datasize];
constant bits(datasize) t2 = X[t+1, datasize];

constant boolean privileged = AArch64.IsUnprivAccessPriv();
constant AccessDescriptor accdesc = CreateAccDescAtomicOp(MemAtomicOp_CAS, acquire, release,
                                                          tagchecked, privileged);

comparevalue = if BigEndian(accdesc.acctype) then s1:s2 else s2:s1;
newvalue     = if BigEndian(accdesc.acctype) then t1:t2 else t2:t1;
if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

data = MemAtomic(address, comparevalue, newvalue, accdesc);

if BigEndian(accdesc.acctype) then
    X[s, datasize]   = data<2*datasize-1:datasize>;
    X[s+1, datasize] = data<datasize-1:0>;
else
    X[s, datasize]   = data<datasize-1:0>;
    X[s+1, datasize] = data<2*datasize-1:datasize>;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSUI)` |
| 🚫 ENCODING_UNDEF | `Rs<0> != '1' && Rt<0> != '1'` |

### Variant: `No offset (CASPAT_CP64_comswappr_unpriv)` (CASPAT)
- **Condition**: `L == 1 && o0 == 0`
- **Assembly**: `CASPAT  <Xs>, <X(s+1)>, <Xt>, <X(t+1)>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`1`, `o0`=`0`
- **Bit Pattern**: `???????????????0??????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 0   1   0010011 L   0   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASPALT_CP64_comswappr_unpriv)` (CASPALT)
- **Condition**: `L == 1 && o0 == 1`
- **Assembly**: `CASPALT  <Xs>, <X(s+1)>, <Xt>, <X(t+1)>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`1`, `o0`=`1`
- **Bit Pattern**: `???????????????1??????1?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 0   1   0010011 L   0   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASPLT_CP64_comswappr_unpriv)` (CASPLT)
- **Condition**: `L == 0 && o0 == 1`
- **Assembly**: `CASPLT  <Xs>, <X(s+1)>, <Xt>, <X(t+1)>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `L`=`0`, `o0`=`1`
- **Bit Pattern**: `???????????????1??????0?????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 0   1   0010011 L   0   Rs  o0  11111 Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xs>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the first general-purpose register to be compared and loaded, encoded in the "Rs" field. <Xs> must be an even-numbered register. |
| `<X(s+1)>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the second general-purpose register to be compared and loaded. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose register to be conditionally stored, encoded in the "Rt" field. <Xt> must be an even-numbered register |
| `<X(t+1)>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the second general-purpose register to be conditionally stored. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- address-form: `base-register`
- address-form-reg-type: `base-register-pair-64`
- isa: `A64`
- reg-type: `pair-64`
- source: `caspt.xml`
</details>