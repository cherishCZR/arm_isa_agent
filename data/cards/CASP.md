## CASP
_ARM A64 Instruction_

**Title**: CASP, CASPA, CASPAL, CASPL -- A64 | **Class**: `general` | **XML ID**: `CASP`

**Architecture**: `FEAT_LSE` (ARMv8.1)

**Summary**: Compare and swap pair of words or doublewords in memory

**Description**:
This instruction reads a pair
of 32-bit words or 64-bit doublewords from memory, and compares them
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
which are compared and loaded, that is <Ws> and
<W(s+1)>, or <Xs> and <X(s+1)>, are
restored to the values held in the registers before the instruction
was executed.

For a CASP or CASPA instruction, when <Ws>
or <Xs> specifies the same register as <Wt> or <Xt>,
this signals to the memory system that an additional subsequent CASP,
CASPA, CASPAL, or CASPL
access to the specified location is likely to occur in the near future. The memory system can respond by
taking actions that are expected to enable the subsequent CASP,
CASPA, CASPAL, or CASPL access to succeed when it does occur.

A code sequence starting with a CASP or CASPA instruction for which
<Ws> or <Xs> specifies the same register as <Wt>
or <Xt>, and ending with a subsequent CASP, CASPA,
CASPAL, or CASPL to the same location, exhibits the following
properties for best performance when the location may be accessed concurrently, on one or more other PEs:

For more information about memory ordering semantics, see Load-Acquire, Store-Release.

For information about addressing modes, see
Load/Store addressing modes.

### Variant: `No offset (CASP_CP32_comswappr)` (32-bit CASP)
- **Condition**: `sz == 0 && L == 0 && o0 == 0`
- **Assembly**: `CASP  <Ws>, <W(s+1)>, <Wt>, <W(t+1)>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `sz`=`0`, `L`=`0`, `o0`=`0`
- **Bit Pattern**: `???????????????0??????0???????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 0   sz  0010000 L   1   Rs  o0  11111 Rn  Rt  |
```

#### Decode (A64.ldst.comswappr.CASP_CP32_comswappr)

```
if !IsFeatureImplemented(FEAT_LSE) then EndOfDecode(Decode_UNDEF);
if Rs<0> == '1' || Rt<0> == '1' then EndOfDecode(Decode_UNDEF);
constant integer s = UInt(Rs);
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant integer datasize = 32 << UInt(sz);
constant boolean acquire = L == '1';
constant boolean release = o0 == '1';
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.comswappr.CASP_CP32_comswappr)

```
bits(64) address;
bits(2*datasize) comparevalue;
bits(2*datasize) newvalue;
bits(2*datasize) data;

constant bits(datasize) s1 = X[s, datasize];
constant bits(datasize) s2 = X[s+1, datasize];
constant bits(datasize) t1 = X[t, datasize];
constant bits(datasize) t2 = X[t+1, datasize];

constant boolean privileged = PSTATE.EL != EL0;
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
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LSE)` |
| 🚫 ENCODING_UNDEF | `Rs<0> != '1' && Rt<0> != '1'` |

### Variant: `No offset (CASPA_CP32_comswappr)` (32-bit CASPA)
- **Condition**: `sz == 0 && L == 1 && o0 == 0`
- **Assembly**: `CASPA  <Ws>, <W(s+1)>, <Wt>, <W(t+1)>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `sz`=`0`, `L`=`1`, `o0`=`0`
- **Bit Pattern**: `???????????????0??????1???????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 0   sz  0010000 L   1   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASPAL_CP32_comswappr)` (32-bit CASPAL)
- **Condition**: `sz == 0 && L == 1 && o0 == 1`
- **Assembly**: `CASPAL  <Ws>, <W(s+1)>, <Wt>, <W(t+1)>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `sz`=`0`, `L`=`1`, `o0`=`1`
- **Bit Pattern**: `???????????????1??????1???????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 0   sz  0010000 L   1   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASPL_CP32_comswappr)` (32-bit CASPL)
- **Condition**: `sz == 0 && L == 0 && o0 == 1`
- **Assembly**: `CASPL  <Ws>, <W(s+1)>, <Wt>, <W(t+1)>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `sz`=`0`, `L`=`0`, `o0`=`1`
- **Bit Pattern**: `???????????????1??????0???????0?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 0   sz  0010000 L   1   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASP_CP64_comswappr)` (64-bit CASP)
- **Condition**: `sz == 1 && L == 0 && o0 == 0`
- **Assembly**: `CASP  <Xs>, <X(s+1)>, <Xt>, <X(t+1)>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `sz`=`1`, `L`=`0`, `o0`=`0`
- **Bit Pattern**: `???????????????0??????0???????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 0   sz  0010000 L   1   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASPA_CP64_comswappr)` (64-bit CASPA)
- **Condition**: `sz == 1 && L == 1 && o0 == 0`
- **Assembly**: `CASPA  <Xs>, <X(s+1)>, <Xt>, <X(t+1)>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `sz`=`1`, `L`=`1`, `o0`=`0`
- **Bit Pattern**: `???????????????0??????1???????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 0   sz  0010000 L   1   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASPAL_CP64_comswappr)` (64-bit CASPAL)
- **Condition**: `sz == 1 && L == 1 && o0 == 1`
- **Assembly**: `CASPAL  <Xs>, <X(s+1)>, <Xt>, <X(t+1)>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `sz`=`1`, `L`=`1`, `o0`=`1`
- **Bit Pattern**: `???????????????1??????1???????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 0   sz  0010000 L   1   Rs  o0  11111 Rn  Rt  |
```

### Variant: `No offset (CASPL_CP64_comswappr)` (64-bit CASPL)
- **Condition**: `sz == 1 && L == 0 && o0 == 1`
- **Assembly**: `CASPL  <Xs>, <X(s+1)>, <Xt>, <X(t+1)>, [<Xn|SP>{, #0}]`
- **Fixed bits**: `sz`=`1`, `L`=`0`, `o0`=`1`
- **Bit Pattern**: `???????????????1??????0???????1?`
**Encoding Diagram (32-bit)**:

```text
| 31 30 29  22 21 20  15 14   9   4  |
|--------------------------------|
| 0   sz  0010000 L   1   Rs  o0  11111 Rn  Rt  |
```

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Ws>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the first general-purpose register to be compared and loaded, encoded in the "Rs" field. <Ws> must be an even-numbered register. |
| `<W(s+1)>` | `register (32-bit)` | `Rs` | Is the 32-bit name of the second general-purpose register to be compared and loaded. |
| `<Wt>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the first general-purpose register to be conditionally stored, encoded in the "Rt" field. <Wt> must be an even-numbered register |
| `<W(t+1)>` | `register (32-bit)` | `Rt` | Is the 32-bit name of the second general-purpose register to be conditionally stored. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |
| `<Xs>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the first general-purpose register to be compared and loaded, encoded in the "Rs" field. <Xs> must be an even-numbered register. |
| `<X(s+1)>` | `register (64-bit)` | `Rs` | Is the 64-bit name of the second general-purpose register to be compared and loaded. |
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose register to be conditionally stored, encoded in the "Rt" field. <Xt> must be an even-numbered register |
| `<X(t+1)>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the second general-purpose register to be conditionally stored. |

---
<details><summary>Metadata</summary>

- address-form: `base-register`
- isa: `A64`
- source: `casp.xml`
</details>