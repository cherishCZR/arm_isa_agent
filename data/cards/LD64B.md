## LD64B
_ARM A64 Instruction_

**Title**: LD64B -- A64 | **Class**: `general` | **XML ID**: `LD64B`

**Architecture**: `FEAT_LS64` (ARMv8.7)

**Summary**: Single-copy atomic 64-byte Load

**Description**:
This instruction derives an address from a base register value, loads eight
64-bit doublewords from a memory location, and writes them to consecutive registers.
The load starts at register Xt, with the data being read as
X(t+7):X(t+6):X(t+5):X(t+4):X(t+3):X(t+2):X(t+1):Xt = Data<511:0>.
The data is loaded atomically and is required to be 64-byte aligned.

It is IMPLEMENTATION DEFINED which memory locations support this instruction.
A memory location that supports LD64B also supports
ST64B.
For more information, including about the memory types accessible and how the accesses are
performed, see Single-copy atomic 64-byte load/store.

### Variant: `Integer`
- **Assembly**: `LD64B  <Xt>, [<Xn|SP> {, #0}]`
**Encoding Diagram (32-bit)**:

```text
| 31  29  27 26 25 24 23 22 21 20  15 14  11   9   4  |
|-----------------------------------------------|
| 11  11  1   0   0   0   0   0   1   11111 1   101 00  Rn  Rt  |
```

#### Decode (A64.ldst.memop.LD64B_64L_memop)

```
if !IsFeatureImplemented(FEAT_LS64) then EndOfDecode(Decode_UNDEF);
if Rt<4:3> == '11' || Rt<0> == '1' then EndOfDecode(Decode_UNDEF);
constant boolean withstatus = FALSE;
constant integer t = UInt(Rt);
constant integer n = UInt(Rn);
constant boolean tagchecked = n != 31;
```

#### Execute (A64.ldst.memop.LD64B_64L_memop)

```
CheckLDST64BEnabled();

bits(512) data;
bits(64) address;
bits(64) value;

constant AccessDescriptor accdesc = CreateAccDescLS64(MemOp_LOAD, withstatus, tagchecked);

if n == 31 then
    CheckSPAlignment();
    address = SP[64];
else
    address = X[n, 64];
data = MemLoad64B(address, accdesc);

for i = 0 to 7
    value = data<63+64*i : 64*i>;
    if BigEndian(accdesc.acctype) then value = BigEndianReverse(value);
    X[t+i, 64] = value;
```

#### Constraints
_1× 🚫 ENCODING_UNDEF / 1× 🔒 FEATURE_GATE_

| Type | Condition |
|---|---|
| 🔒 FEATURE_GATE | `IsFeatureImplemented(FEAT_LS64)` |
| 🚫 ENCODING_UNDEF | `Rt<4:3> != '11' && Rt<0> != '1'` |

### Operands

| Symbol | Type | Field | Description |
|---|---|---|---|
| `<Xt>` | `register (64-bit)` | `Rt` | Is the 64-bit name of the first general-purpose register to be transferred, encoded in the "Rt" field. |
| `<Xn\|SP>` | `register (64-bit)` | `Rn` | Is the 64-bit name of the general-purpose base register or stack pointer, encoded in the "Rn" field. |

---
<details><summary>Metadata</summary>

- isa: `A64`
- source: `ld64b.xml`
</details>