## RCWCASP
_ARM A64 Instruction_

**Title**: RCWCASP, RCWCASPA, RCWCASPAL, RCWCASPL -- A64 | **Class**: `general` | **XML ID**: `RCWCASP`

**Architecture**: `FEAT_D128 && FEAT_THE` (FEAT_D128 && FEAT_THE)

**Summary**: Read check write compare and swap quadword in memory

**Description**:
This instruction reads a 128-bit quadword
from memory, and compares it against the value held in a pair of registers. If the comparison
is equal, the value in a second pair of registers is conditionally written to memory.
Storing back to memory is conditional on RCW Checks. If the compare fails or the RCW Checks fail,
the architecture permits writing the value read from the location to memory.
If the write is performed, the read and the write occur atomically such that no other
modification of the memory location can take place between the read and the write.
This instruction updates the condition flags based on the result of the update of memory.

### Variant: `Integer (RCWCASP_C64_rcwcomswappr)` (RCWCASP)
- **Condition**: `A == 0 && R == 0`
- **Assembly**: `RCWCASP  <Xs>, <X(s+1)>, <Xt>, <X(t+1)>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`0`
- **Bit Pattern**: `??????????????????????00????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15   9   4  |
|--------------------------------|
| 0   0   011001 A   R   1   Rs  000011 Rn  Rt  |
```

#### Decode (A64.ldst.rcwcomswappr.RCWCASP_C64_rcwcomswappr)

```
if !IsFeatureImplemented(FEAT_D128) || !IsFeatureImplemented(FEAT_THE) then
    EndOfDecode(Decode_UNDEF);
if Rs<0> == '1' then EndOfDecode(Decode_UNDEF);
if Rt<0> == '1' then EndOfDecode(Decode_UNDEF);
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);

constant boolean acquire = A == '1';
constant boolean release = R == '1';
constant boolean soft = FALSE;
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.rcwcomswappr.RCWCASP_C64_rcwcomswappr)

```
if !IsD128Enabled(PSTATE.EL) then UNDEFINED;
bits(64) address;
bits(128) newdata;
bits(128) compdata;
bits(128) readdata;
bits(4) nzcv;

constant bits(64) s1 = X[s, 64];
constant bits(64) s2 = X[s+1, 64];
constant bits(64) t1 = X[t, 64];
constant bits(64) t2 = X[t+1, 64];

constant AccessDescriptor accdesc = CreateAccDescRCW(MemAtomicOp_CAS, soft, acquire, release,
                                                     tagchecked);

compdata = if BigEndian(accdesc.acctype) then s1:s2 else s2:s1;
newdata  = if BigEndian(accdesc.acctype) then t1:t2 else t2:t1;

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];

(nzcv, readdata) = MemAtomicRCW(address, compdata, newdata, accdesc);

PSTATE.<N,Z,C,V> = nzcv;
if BigEndian(accdesc.acctype) then
    X[s, 64]   = readdata<127:64>;
    X[s+1, 64] = readdata<63:0>;
else
    X[s, 64]   = readdata<63:0>;
    X[s+1, 64] = readdata<127:64>;
```

#### Constraints
_2× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_D128) && IsFeatureImplemented(FEAT_THE)` |
| 🚫 ENCODING_UNDEF | `Rs<0> != '1'` |
| 🚫 ENCODING_UNDEF | `Rt<0> != '1'` |

### Variant: `Integer (RCWCASPA_C64_rcwcomswappr)` (RCWCASPA)
- **Condition**: `A == 1 && R == 0`
- **Assembly**: `RCWCASPA  <Xs>, <X(s+1)>, <Xt>, <X(t+1)>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`0`
- **Bit Pattern**: `??????????????????????01????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15   9   4  |
|--------------------------------|
| 0   0   011001 A   R   1   Rs  000011 Rn  Rt  |
```

### Variant: `Integer (RCWCASPAL_C64_rcwcomswappr)` (RCWCASPAL)
- **Condition**: `A == 1 && R == 1`
- **Assembly**: `RCWCASPAL  <Xs>, <X(s+1)>, <Xt>, <X(t+1)>, [<Xn|SP>]`
- **Fixed bits**: `A`=`1`, `R`=`1`
- **Bit Pattern**: `??????????????????????11????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15   9   4  |
|--------------------------------|
| 0   0   011001 A   R   1   Rs  000011 Rn  Rt  |
```

### Variant: `Integer (RCWCASPL_C64_rcwcomswappr)` (RCWCASPL)
- **Condition**: `A == 0 && R == 1`
- **Assembly**: `RCWCASPL  <Xs>, <X(s+1)>, <Xt>, <X(t+1)>, [<Xn|SP>]`
- **Fixed bits**: `A`=`0`, `R`=`1`
- **Bit Pattern**: `??????????????????????10????????`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  23 22 21 20  15   9   4  |
|--------------------------------|
| 0   0   011001 A   R   1   Rs  000011 Rn  Rt  |
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

- isa: `A64`
- source: `rcwcasp.xml`
</details>